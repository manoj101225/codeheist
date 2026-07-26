import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login, register } from '../services/api';

export default function AuthPage({ onAuth }) {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      let data;
      if (isLogin) {
        data = await login(username, password);
      } else {
        data = await register(username, email, password);
      }
      onAuth(data.user);
      navigate('/map');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h1 className="auth-title">CODEHEIST</h1>
        <p className="auth-subtitle">
          {isLogin ? 'Welcome back, operative.' : 'Join the criminal underworld.'}
        </p>

        {error && (
          <div style={{
            padding: '0.75rem 1rem',
            background: 'rgba(255, 0, 64, 0.1)',
            border: '1px solid rgba(255, 0, 64, 0.3)',
            borderRadius: 'var(--radius-md)',
            color: 'var(--neon-red)',
            fontSize: '0.85rem',
            marginBottom: '1rem',
            fontFamily: 'var(--font-mono)',
          }}>
            ⚠ {error}
          </div>
        )}

        <form className="auth-form" onSubmit={handleSubmit}>
          <div>
            <label htmlFor="username">Codename</label>
            <input
              id="username"
              className="input-field"
              type="text"
              placeholder="Enter your codename"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>

          {!isLogin && (
            <div>
              <label htmlFor="email">Encrypted Channel (Email)</label>
              <input
                id="email"
                className="input-field"
                type="email"
                placeholder="your@email.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
          )}

          <div>
            <label htmlFor="password">Passphrase</label>
            <input
              id="password"
              className="input-field"
              type="password"
              placeholder="Enter your passphrase"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <button
            type="submit"
            className="btn btn-primary btn-lg"
            disabled={loading}
            style={{ width: '100%', marginTop: '0.5rem' }}
          >
            {loading ? '⏳ Processing...' : isLogin ? '🔐 Infiltrate' : '🎯 Recruit Me'}
          </button>
        </form>

        <div className="auth-toggle">
          {isLogin ? (
            <>New operative? <span onClick={() => { setIsLogin(false); setError(''); }}>Register here</span></>
          ) : (
            <>Already recruited? <span onClick={() => { setIsLogin(true); setError(''); }}>Login here</span></>
          )}
        </div>
      </div>
    </div>
  );
}
