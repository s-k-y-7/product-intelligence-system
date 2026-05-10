const API_BASE = 'http://localhost:8000/api';

export const apiClient = {
  async createProduct(query) {
    const res = await fetch(`${API_BASE}/products/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query })
    });
    if (!res.ok) throw new Error('Failed to create product');
    return res.json();
  },

  async getProduct(productId) {
    const res = await fetch(`${API_BASE}/products/${productId}/`);
    if (!res.ok) throw new Error('Failed to fetch product');
    return res.json();
  },

  async discover(productId) {
    const res = await fetch(`${API_BASE}/products/${productId}/discover/`, {
      method: 'POST'
    });
    if (!res.ok) throw new Error('Discover failed');
    return res.json();
  },

  async collect(productId) {
    const res = await fetch(`${API_BASE}/products/${productId}/collect/`, {
      method: 'POST'
    });
    if (!res.ok) throw new Error('Collect failed');
    return res.json();
  },

  async analyze(productId) {
    const res = await fetch(`${API_BASE}/products/${productId}/analyze/`, {
      method: 'POST'
    });
    if (!res.ok) throw new Error('Analyze failed');
    return res.json();
  }
};
