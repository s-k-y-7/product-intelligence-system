import React from 'react';
import { CheckCircle2, Circle, Loader2 } from 'lucide-react';

export default function PipelineStepper({ status }) {
  // status can be: null, 'DISCOVERING', 'COLLECTING', 'ANALYZING', 'READY', 'FAILED'
  
  if (!status) return null;

  const steps = [
    { key: 'DISCOVERING', label: 'Discovering Sources' },
    { key: 'COLLECTING', label: 'Collecting Data' },
    { key: 'ANALYZING', label: 'Generating Insights' }
  ];

  const getStepState = (stepIndex) => {
    const currentIndex = steps.findIndex(s => s.key === status);
    
    if (status === 'READY') return 'completed';
    if (status === 'FAILED') return 'failed';
    
    if (currentIndex > stepIndex) return 'completed';
    if (currentIndex === stepIndex) return 'current';
    return 'pending';
  };

  return (
    <div className="card mb-4">
      <h3 className="mb-4">Analysis Progress</h3>
      <div className="flex flex-col gap-4">
        {steps.map((step, idx) => {
          const state = getStepState(idx);
          return (
            <div key={step.key} className="flex items-center gap-4">
              {state === 'completed' && <CheckCircle2 className="text-success" size={24} />}
              {state === 'current' && <Loader2 className="text-accent animate-spin" size={24} style={{ color: 'var(--accent-color)' }} />}
              {state === 'pending' && <Circle className="text-muted" size={24} />}
              <span className={state === 'current' ? 'font-bold text-accent' : state === 'pending' ? 'text-muted' : ''} style={state === 'current' ? { color: 'var(--accent-color)' } : {}}>
                {step.label}
              </span>
            </div>
          );
        })}
      </div>
      {status === 'FAILED' && (
        <div className="mt-4 text-error font-bold">
          Pipeline failed. Please try again.
        </div>
      )}
    </div>
  );
}
