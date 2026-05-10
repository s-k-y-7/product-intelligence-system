import React, { useState } from 'react';
import { Search } from 'lucide-react';

export default function SearchBar({ onSearch, disabled }) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim() && !disabled) {
      onSearch(query);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mb-4">
      <div className="flex gap-2">
        <input
          type="text"
          className="input-field"
          placeholder="e.g. Samsung Galaxy S23"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          disabled={disabled}
        />
        <button type="submit" className="btn-primary flex items-center gap-2" disabled={disabled || !query.trim()}>
          <Search size={18} />
          Analyze
        </button>
      </div>
    </form>
  );
}
