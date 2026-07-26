import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getDistrict } from '../services/api';

export default function DistrictPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [district, setDistrict] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDistrict();
  }, [id]);

  const loadDistrict = async () => {
    try {
      const data = await getDistrict(id);
      setDistrict(data);
    } catch (err) {
      console.error('Failed to load district:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex-center" style={{ height: 'calc(100vh - 64px)' }}>
        <h3 style={{ color: 'var(--neon-cyan)' }}>LOADING MISSIONS...</h3>
      </div>
    );
  }

  if (!district) {
    return (
      <div className="flex-center" style={{ height: 'calc(100vh - 64px)' }}>
        <h3 style={{ color: 'var(--neon-red)' }}>DISTRICT NOT FOUND</h3>
      </div>
    );
  }

  return (
    <div className="page-container animate-fadeIn">
      {/* Header */}
      <div style={{
        display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '2rem',
      }}>
        <button
          className="btn btn-secondary btn-sm"
          onClick={() => navigate('/map')}
        >
          ← Back to Map
        </button>
      </div>

      <div style={{
        display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '0.5rem',
      }}>
        <span style={{ fontSize: '2.5rem' }}>{district.icon}</span>
        <div>
          <h1 style={{ color: district.color, fontSize: '1.8rem' }}>{district.name}</h1>
          <span className="badge badge-medium">{district.topic}</span>
        </div>
      </div>

      <p style={{
        color: 'var(--text-secondary)', fontSize: '0.95rem',
        maxWidth: '700px', marginBottom: '2rem', lineHeight: 1.7,
      }}>
        {district.description}
      </p>

      {/* Mission List */}
      <h3 style={{
        fontSize: '0.8rem', color: 'var(--text-muted)', letterSpacing: '0.15em',
        marginBottom: '1rem',
      }}>
        HEIST MISSIONS ({district.missions?.length || 0})
      </h3>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', maxWidth: '700px' }}>
        {district.missions?.map((m) => (
          <div
            key={m.id}
            className="mission-card"
            onClick={() => navigate(`/mission/${m.id}`)}
          >
            <span className="mission-order">#{String(m.order).padStart(2, '0')}</span>
            <div style={{ flex: 1 }}>
              <div className="mission-title">{m.title}</div>
              <div className="mission-subtitle">{m.subtitle}</div>
            </div>
            <span className={`badge badge-${m.difficulty.toLowerCase()}`}>
              {m.difficulty}
            </span>
            <span style={{
              fontFamily: 'var(--font-mono)', fontSize: '0.75rem',
              color: 'var(--neon-yellow)',
            }}>
              ⭐ {m.reputation_reward}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
