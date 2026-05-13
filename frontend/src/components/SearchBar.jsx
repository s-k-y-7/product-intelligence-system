import React, { useState, useRef, useEffect } from 'react';
import { Search, Sparkles } from 'lucide-react';

export default function SearchBar({ onSearch, disabled }) {
  const [query, setQuery] = useState('');
  const [isFocused, setIsFocused] = useState(false);
  const containerRef = useRef(null);

  // Sample queries from the backend mock datasets
  const sampleQueries = [
    "Apple iPhone 15",
    "Samsung Galaxy S23",
    "OnePlus 11"
  ];

  // Close the popup if clicked outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (containerRef.current && !containerRef.current.contains(event.target)) {
        setIsFocused(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim() && !disabled) {
      onSearch(query);
      setIsFocused(false);
    }
  };

  const handleSampleClick = (sample) => {
    setQuery(sample);
    setIsFocused(false);
    if (!disabled) {
      onSearch(sample);
    }
  };

  return (
    <div className="dropdown-container mb-4" ref={containerRef}>
      <form onSubmit={handleSubmit}>
        <div className="flex gap-2">
          <input
            type="text"
            className="input-field"
            placeholder="e.g. Samsung Galaxy S23"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onFocus={() => setIsFocused(true)}
            disabled={disabled}
          />
          <button type="submit" className="btn-primary flex items-center gap-2" disabled={disabled || !query.trim()}>
            <Search size={18} />
            Analyze
          </button>
        </div>
      </form>
      
      {isFocused && (
        <div className="sample-queries-card">
          <div className="sample-queries-header">
            <div className="flex items-center gap-2">
              <Sparkles size={16} style={{color: 'var(--accent-color)'}} />
              <span>Try these sample queries</span>
            </div>
            <div 
              className="text-muted" 
              style={{ 
                marginTop: '0.4rem', 
                fontSize: '0.75rem', 
                textTransform: 'none', 
                letterSpacing: 'normal',
                fontWeight: 'normal',
                lineHeight: '1.4'
              }}
            >
              The platform is in development. We recommend using these queries as they are fully supported by our local mock datasets.
            </div>
          </div>
          <ul className="sample-queries-list">
            {sampleQueries.map((sample, idx) => (
              <li 
                key={idx}
                className="sample-query-item"
                onMouseDown={(e) => {
                  e.preventDefault(); // Prevent input from losing focus immediately
                  handleSampleClick(sample);
                }}
              >
                <Search size={16} style={{color: 'var(--text-secondary)'}} />
                <span>{sample}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
