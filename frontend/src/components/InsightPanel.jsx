import React from 'react';
import { ThumbsUp, ThumbsDown, AlertTriangle, Lightbulb } from 'lucide-react';

export default function InsightPanel({ insight }) {
  if (!insight) return null;

  return (
    <div className="card">
      <h2 className="mb-4 flex items-center gap-2">
        <Lightbulb style={{ color: 'var(--accent-color)' }} />
        AI Product Insight
      </h2>
      
      <div className="mb-4" style={{ padding: '1rem', backgroundColor: 'var(--surface-elevated)', borderRadius: '6px', borderLeft: '4px solid var(--accent-color)' }}>
        <strong>Verdict: </strong>
        {insight.text_verdict || insight.verdict}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
        <div>
          <h4 className="flex items-center gap-2 mb-2 text-success">
            <ThumbsUp size={16} /> Pros
          </h4>
          <ul style={{ listStylePosition: 'inside', color: 'var(--text-secondary)' }}>
            {(insight.pros_summary || []).map((pro, i) => (
              <li key={i}>{pro}</li>
            ))}
            {(!insight.pros_summary || insight.pros_summary.length === 0) && <li>No notable pros found.</li>}
          </ul>
        </div>

        <div>
          <h4 className="flex items-center gap-2 mb-2 text-error">
            <ThumbsDown size={16} /> Cons
          </h4>
          <ul style={{ listStylePosition: 'inside', color: 'var(--text-secondary)' }}>
            {(insight.cons_summary || []).map((con, i) => (
              <li key={i}>{con}</li>
            ))}
            {(!insight.cons_summary || insight.cons_summary.length === 0) && <li>No notable cons found.</li>}
          </ul>
        </div>
      </div>
      
      {insight.common_complaints && insight.common_complaints.length > 0 && (
        <div className="mt-4">
          <h4 className="flex items-center gap-2 mb-2 text-error">
            <AlertTriangle size={16} /> Common Complaints
          </h4>
          <ul style={{ listStylePosition: 'inside', color: 'var(--text-secondary)' }}>
            {insight.common_complaints.map((c, i) => <li key={i}>{c}</li>)}
          </ul>
        </div>
      )}

      <div className="mt-4 flex justify-between items-center text-muted" style={{ fontSize: '0.85rem', borderTop: '1px solid var(--border-color)', paddingTop: '1rem' }}>
        <span>Confidence Score: {((insight.text_confidence || insight.confidence || 0) * 100).toFixed(0)}%</span>
        <span>Mode: {insight.text_insight_mode || 'unknown'}</span>
      </div>
    </div>
  );
}
