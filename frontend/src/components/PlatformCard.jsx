import React from 'react';
import { Trophy, Star, DollarSign, Activity } from 'lucide-react';

export default function PlatformCard({ scoreData, isBest }) {
  if (!scoreData) return null;

  return (
    <div className={`card ${isBest ? 'best-platform' : ''}`} style={isBest ? { borderColor: 'var(--accent-color)' } : {}}>
      {isBest && (
        <div className="flex items-center gap-2 mb-2" style={{ color: 'var(--accent-color)', fontWeight: 600 }}>
          <Trophy size={18} /> Top Recommendation
        </div>
      )}
      
      <h3 className="mb-1">{scoreData.platform}</h3>
      <p className="text-muted mb-4" style={{ fontSize: '0.9rem' }}>{scoreData.title}</p>
      
      <div className="grid gap-2" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
        <div className="flex items-center gap-2">
          <DollarSign size={16} className="text-muted" />
          <span>${scoreData.price || 'N/A'}</span>
        </div>
        <div className="flex items-center gap-2">
          <Star size={16} className="text-muted" />
          <span>{scoreData.rating ? `${scoreData.rating}/5` : 'No rating'}</span>
        </div>
        <div className="flex items-center gap-2">
          <Activity size={16} className="text-muted" />
          <span>Score: {(scoreData.final_score * 100).toFixed(0)}</span>
        </div>
      </div>
    </div>
  );
}
