const API_BASE = 'http://localhost:8000/api';

function getToken() {
  return localStorage.getItem('codeheist_token');
}

function authHeaders() {
  const token = getToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

async function request(path, options = {}) {
  const { method = 'GET', body, auth = true } = options;
  const headers = {
    'Content-Type': 'application/json',
    ...(auth ? authHeaders() : {}),
  };

  const res = await fetch(`${API_BASE}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Request failed' }));
    throw new Error(err.detail || 'Request failed');
  }

  return res.json();
}

// Auth
export async function register(username, email, password) {
  const data = await request('/auth/register', {
    method: 'POST',
    body: { username, email, password },
    auth: false,
  });
  localStorage.setItem('codeheist_token', data.access_token);
  return data;
}

export async function login(username, password) {
  const form = new URLSearchParams();
  form.append('username', username);
  form.append('password', password);

  const res = await fetch(`${API_BASE}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: form,
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Login failed' }));
    throw new Error(err.detail || 'Login failed');
  }

  const data = await res.json();
  localStorage.setItem('codeheist_token', data.access_token);
  return data;
}

export function logout() {
  localStorage.removeItem('codeheist_token');
}

export function isAuthenticated() {
  return !!getToken();
}

// Districts
export function getDistricts() {
  return request('/districts/');
}

export function getDistrict(id) {
  return request(`/districts/${id}`);
}

// Missions
export function getMission(id) {
  return request(`/missions/${id}`);
}

export function getRecommendedMission() {
  return request('/missions/next/recommended');
}

// Submissions
export function submitCode(missionId, language, code) {
  return request('/submissions/', {
    method: 'POST',
    body: { mission_id: missionId, language, code },
  });
}

// Progress
export function getMyProgress() {
  return request('/progress/me');
}

// Leaderboard
export function getLeaderboard() {
  return request('/leaderboard/', { auth: false });
}

export function getMyRank() {
  return request('/leaderboard/me');
}
