from dataclasses import dataclass
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List
from typing import Optional


@dataclass
class TextInsightRoutingConfig:
    simple_word_threshold: int = 800
    chunk_target_words: int = 900
    chunk_overlap_sentences: int = 2
    max_workers: int = 4
    max_map_retries: int = 2
    retry_backoff_seconds: float = 0.05
    max_failed_chunks_before_fallback: int = 1


class TextInsightOrchestrator:
    def __init__(self, config: Optional[TextInsightRoutingConfig] = None):
        self.config = config or TextInsightRoutingConfig()

    def generate(self, texts: List[str]) -> Dict[str, object]:
        merged_text = self._merge_texts(texts)
        word_count = self._word_count(merged_text)

        if word_count <= self.config.simple_word_threshold:
            result = self._run_simple(merged_text)
            result["mode"] = "simple"
            return result

        result = self._run_complex(merged_text)
        result["mode"] = result.get("mode", "complex_map")
        return result

    def _run_simple(self, text: str) -> Dict[str, object]:
        return self._llm_extract(text)

    def _run_complex(self, text: str) -> Dict[str, object]:
        sentences = self._split_sentences(text)
        chunks = self._build_chunks(sentences)

        if not chunks:
            return self._keyword_extract(text)

        map_outputs = self._map_chunks_parallel(chunks)
        failed_chunks = self._count_failed_chunks(map_outputs)

        # Graceful degradation: if too many chunks fail, use simple path.
        if failed_chunks > self.config.max_failed_chunks_before_fallback:
            fallback = self._run_simple(text)
            fallback["mode"] = "complex_fallback_simple"
            fallback["chunk_count"] = len(chunks)
            fallback["failed_chunk_count"] = failed_chunks
            fallback["map_outputs"] = []
            return fallback

        return self._merge_map_outputs(map_outputs)

    def _llm_extract(self, text: str) -> Dict[str, object]:
        from products.services.llm_client import GroqClient
        try:
            client = GroqClient()
            return client.extract_insight(text)
        except Exception as e:
            print(f"LLM extraction failed, falling back to keyword extraction: {e}")
            return self._keyword_extract(text)

    def _keyword_extract(self, text: str) -> Dict[str, object]:
        lowered = text.lower()
        pros: List[str] = []
        cons: List[str] = []

        if "good" in lowered or "excellent" in lowered:
            pros.append("positive feedback detected")

        if "bad" in lowered or "poor" in lowered:
            cons.append("negative feedback detected")

        return {
            "pros_summary": pros,
            "cons_summary": cons,
            "common_complaints": cons[:],
            "verdict": self._build_verdict(pros, cons),
            "confidence": 0.6 if (pros or cons) else 0.3,
        }

    def _build_verdict(self, pros: List[str], cons: List[str]) -> str:
        if pros and not cons:
            return "Mostly positive user sentiment."
        if cons and not pros:
            return "Mostly negative user sentiment."
        if pros and cons:
            return "Mixed user sentiment with both strengths and weaknesses."
        return "Insufficient signal in available text."

    def _merge_texts(self, texts: List[str]) -> str:
        safe_texts = [t for t in texts if isinstance(t, str) and t.strip()]
        return "\n\n".join(safe_texts)

    def _word_count(self, text: str) -> int:
        if not text.strip():
            return 0
        return len(text.split())

    def _split_sentences(self, text: str) -> List[str]:
        if not text.strip():
            return []

        raw_sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        return [s.strip() for s in raw_sentences if s and s.strip()]

    def _build_chunks(self, sentences: List[str]) -> List[Dict[str, object]]:
        chunks: List[Dict[str, object]] = []
        if not sentences:
            return chunks

        target = self.config.chunk_target_words
        overlap_count = self.config.chunk_overlap_sentences

        idx = 0
        chunk_id = 1

        while idx < len(sentences):
            current_sentences: List[str] = []
            current_words = 0
            start_idx = idx

            while idx < len(sentences):
                sentence = sentences[idx]
                sentence_words = self._word_count(sentence)

                if current_sentences and current_words + sentence_words > target:
                    break

                current_sentences.append(sentence)
                current_words += sentence_words
                idx += 1

            if not current_sentences:
                current_sentences.append(sentences[idx])
                idx += 1

            chunks.append(
                {
                    "chunk_id": "chunk_{0}".format(chunk_id),
                    "text": " ".join(current_sentences),
                    "start_sentence_index": start_idx,
                    "end_sentence_index": idx - 1,
                }
            )
            chunk_id += 1

            if idx < len(sentences) and overlap_count > 0:
                idx = max(start_idx + 1, idx - overlap_count)

        return chunks

    def _map_chunks_parallel(self, chunks: List[Dict[str, object]]) -> List[Dict[str, object]]:
        if not chunks:
            return []

        map_outputs: List[Dict[str, object]] = []
        workers = min(self.config.max_workers, len(chunks))

        with ThreadPoolExecutor(max_workers=workers) as executor:
            future_map = {
                executor.submit(self._map_single_chunk_with_retry, chunk): chunk["chunk_id"]
                for chunk in chunks
            }

            for future in as_completed(future_map):
                chunk_id = future_map[future]
                try:
                    map_outputs.append(future.result())
                except Exception:
                    map_outputs.append(
                        {
                            "chunk_id": chunk_id,
                            "pros_summary": [],
                            "cons_summary": [],
                            "common_complaints": [],
                            "verdict": "Chunk processing failed.",
                            "confidence": 0.0,
                            "processing_status": "failed",
                            "retry_count": self.config.max_map_retries,
                        }
                    )

        map_outputs.sort(key=lambda item: int(str(item["chunk_id"]).split("_")[-1]))
        return map_outputs

    def _map_single_chunk_with_retry(self, chunk: Dict[str, object]) -> Dict[str, object]:
        retries = self.config.max_map_retries
        attempt = 0

        while True:
            try:
                extracted = self._map_single_chunk(chunk)
                extracted["processing_status"] = "success"
                extracted["retry_count"] = attempt
                return extracted
            except Exception:
                if attempt >= retries:
                    raise

                attempt += 1
                time.sleep(self.config.retry_backoff_seconds * attempt)

    def _map_single_chunk(self, chunk: Dict[str, object]) -> Dict[str, object]:
        extracted = self._llm_extract(str(chunk["text"]))
        extracted["chunk_id"] = chunk["chunk_id"]
        return extracted

    def _merge_map_outputs(self, map_outputs: List[Dict[str, object]]) -> Dict[str, object]:
        pros: List[str] = []
        cons: List[str] = []
        complaints: List[str] = []
        confidences: List[float] = []
        success_count = 0
        failure_count = 0

        for item in map_outputs:
            pros.extend(item.get("pros_summary", []))
            cons.extend(item.get("cons_summary", []))
            complaints.extend(item.get("common_complaints", []))

            confidence = item.get("confidence")
            if isinstance(confidence, (int, float)):
                confidences.append(float(confidence))

            if item.get("processing_status") == "failed":
                failure_count += 1
            else:
                success_count += 1

        dedup_pros = sorted(set(pros))
        dedup_cons = sorted(set(cons))
        dedup_complaints = sorted(set(complaints))

        avg_confidence = 0.0
        if confidences:
            avg_confidence = round(sum(confidences) / len(confidences), 3)

        return {
            "pros_summary": dedup_pros,
            "cons_summary": dedup_cons,
            "common_complaints": dedup_complaints,
            "verdict": self._build_verdict(dedup_pros, dedup_cons),
            "confidence": avg_confidence,
            "chunk_count": len(map_outputs),
            "successful_chunk_count": success_count,
            "failed_chunk_count": failure_count,
            "map_outputs": map_outputs,
        }

    def _count_failed_chunks(self, map_outputs: List[Dict[str, object]]) -> int:
        failed = 0
        for item in map_outputs:
            if item.get("processing_status") == "failed":
                failed += 1
        return failed
