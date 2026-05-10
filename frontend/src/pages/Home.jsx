import React, { useState } from 'react';
import SearchBar from '../components/SearchBar';
import PipelineStepper from '../components/PipelineStepper';
import PlatformCard from '../components/PlatformCard';
import InsightPanel from '../components/InsightPanel';
import { apiClient } from '../api/client';

export default function Home() {
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState(null);
  const [insight, setInsight] = useState(null);

  const handleSearch = async (query) => {
    setLoading(true);
    setStatus('DISCOVERING');
    setInsight(null);

    try {
      // 1. Create product (this kicks off Celery in the backend)
      const product = await apiClient.createProduct(query);
      
      // 2. Poll the status
      let currentStatus = product.status;
      let finalProduct = product;

      while (currentStatus !== 'READY' && currentStatus !== 'FAILED') {
        // wait 2 seconds
        await new Promise(resolve => setTimeout(resolve, 2000));
        finalProduct = await apiClient.getProduct(product.id);
        currentStatus = finalProduct.status;
        
        // Only update UI if status actually changed
        if (currentStatus === 'COLLECTING' || currentStatus === 'ANALYZING' || currentStatus === 'READY') {
          setStatus(currentStatus);
        }
      }

      if (currentStatus === 'FAILED') {
        setStatus('FAILED');
      } else {
        setStatus('READY');
        setInsight(finalProduct.insight);
      }
    } catch (err) {
      console.error(err);
      setStatus('FAILED');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <header className="mb-4 text-center">
        <h1 style={{ marginBottom: '0.5rem' }}>Product Intelligence</h1>
        <p className="text-muted">AI-powered market validation and review analysis.</p>
      </header>

      <SearchBar onSearch={handleSearch} disabled={loading} />
      
      {status && status !== 'READY' && status !== 'FAILED' && (
        <PipelineStepper status={status} />
      )}
      
      {status === 'FAILED' && <PipelineStepper status={status} />}

      {status === 'READY' && insight && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', animation: 'fadeIn 0.5s ease-in' }}>
          
          {insight.platform_scores && insight.platform_scores.length > 0 && (
            <div>
              <h2 className="mb-2">Recommended Platform</h2>
              <PlatformCard scoreData={insight.platform_scores[0]} isBest={true} />
            </div>
          )}

          <InsightPanel insight={insight} />
          
        </div>
      )}
      
      <style>{`
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
      `}</style>
    </div>
  );
}
