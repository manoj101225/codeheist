import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { getDistricts } from '../services/api';

export default function MapOverview() {
  const [districts, setDistricts] = useState([]);
  const [selectedDistrict, setSelectedDistrict] = useState(null);
  const [loading, setLoading] = useState(true);
  const canvasRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    loadDistricts();
  }, []);

  useEffect(() => {
    if (districts.length > 0) {
      drawMap();
    }
  }, [districts, selectedDistrict]);

  const loadDistricts = async () => {
    try {
      const data = await getDistricts();
      setDistricts(data);
    } catch (err) {
      console.error('Failed to load districts:', err);
    } finally {
      setLoading(false);
    }
  };

  const drawMap = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const w = canvas.width = canvas.offsetWidth;
    const h = canvas.height = canvas.offsetHeight;

    // Clear
    ctx.fillStyle = '#0a0a0f';
    ctx.fillRect(0, 0, w, h);

    // Draw grid
    ctx.strokeStyle = 'rgba(0, 240, 255, 0.04)';
    ctx.lineWidth = 1;
    for (let x = 0; x < w; x += 40) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, h);
      ctx.stroke();
    }
    for (let y = 0; y < h; y += 40) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(w, y);
      ctx.stroke();
    }

    // Draw connections between districts
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.06)';
    ctx.lineWidth = 2;
    const sorted = [...districts].sort((a, b) => a.order - b.order);
    for (let i = 0; i < sorted.length - 1; i++) {
      const a = sorted[i];
      const b = sorted[i + 1];
      const ax = (a.x / 800) * w;
      const ay = (a.y / 600) * h;
      const bx = (b.x / 800) * w;
      const by = (b.y / 600) * h;
      ctx.beginPath();
      ctx.setLineDash([5, 10]);
      ctx.moveTo(ax, ay);
      ctx.lineTo(bx, by);
      ctx.stroke();
      ctx.setLineDash([]);
    }

    // Draw district nodes
    districts.forEach((d) => {
      const x = (d.x / 800) * w;
      const y = (d.y / 600) * h;
      const isSelected = selectedDistrict?.id === d.id;
      const radius = isSelected ? 35 : 28;

      // Glow effect
      if (d.is_unlocked) {
        const gradient = ctx.createRadialGradient(x, y, 0, x, y, radius * 2.5);
        gradient.addColorStop(0, d.color + '40');
        gradient.addColorStop(1, 'transparent');
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(x, y, radius * 2.5, 0, Math.PI * 2);
        ctx.fill();
      }

      // Node circle
      ctx.beginPath();
      ctx.arc(x, y, radius, 0, Math.PI * 2);
      if (d.is_unlocked) {
        ctx.fillStyle = d.color + '30';
        ctx.strokeStyle = d.color;
        ctx.lineWidth = isSelected ? 3 : 2;
      } else {
        ctx.fillStyle = 'rgba(40, 40, 60, 0.5)';
        ctx.strokeStyle = 'rgba(80, 80, 100, 0.3)';
        ctx.lineWidth = 1;
      }
      ctx.fill();
      ctx.stroke();

      // Icon
      ctx.font = `${isSelected ? 24 : 20}px sans-serif`;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(d.is_unlocked ? d.icon : '🔒', x, y);

      // Label
      ctx.font = `bold ${isSelected ? 12 : 10}px Orbitron, sans-serif`;
      ctx.fillStyle = d.is_unlocked ? d.color : 'rgba(100, 100, 120, 0.5)';
      ctx.textAlign = 'center';
      ctx.fillText(d.name.toUpperCase(), x, y + radius + 16);

      // Progress text
      if (d.is_unlocked) {
        ctx.font = '9px Rajdhani, sans-serif';
        ctx.fillStyle = 'rgba(200, 200, 220, 0.6)';
        ctx.fillText(
          `${d.missions_completed}/${d.total_missions} missions`,
          x, y + radius + 30
        );
      }
    });
  };

  const handleCanvasClick = (e) => {
    const canvas = canvasRef.current;
    const rect = canvas.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;
    const w = canvas.offsetWidth;
    const h = canvas.offsetHeight;

    for (const d of districts) {
      const x = (d.x / 800) * w;
      const y = (d.y / 600) * h;
      const dist = Math.hypot(mx - x, my - y);
      if (dist < 35) {
        setSelectedDistrict(d);
        return;
      }
    }
    setSelectedDistrict(null);
  };

  if (loading) {
    return (
      <div className="flex-center" style={{ height: 'calc(100vh - 64px)' }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🗺️</div>
          <h3 style={{ color: 'var(--neon-cyan)' }}>LOADING CITY MAP...</h3>
        </div>
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', height: 'calc(100vh - 64px)' }}>
      {/* Canvas Map */}
      <div style={{ flex: 1, position: 'relative' }}>
        <canvas
          ref={canvasRef}
          className="city-map-canvas"
          onClick={handleCanvasClick}
        />

        {/* Map legend */}
        <div style={{
          position: 'absolute', bottom: '1rem', left: '1rem',
          padding: '0.75rem 1rem',
          background: 'rgba(10, 10, 15, 0.85)',
          borderRadius: 'var(--radius-md)',
          border: '1px solid var(--border-subtle)',
          fontSize: '0.7rem',
          color: 'var(--text-muted)',
          fontFamily: 'var(--font-display)',
        }}>
          <div>🟢 Unlocked · 🔒 Locked · Click district to view missions</div>
        </div>
      </div>

      {/* Side Panel */}
      <div style={{
        width: '380px',
        background: 'var(--bg-secondary)',
        borderLeft: '1px solid var(--border-subtle)',
        padding: '1.5rem',
        overflowY: 'auto',
      }}>
        {selectedDistrict ? (
          <div className="animate-slideRight">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1rem' }}>
              <span style={{ fontSize: '2rem' }}>{selectedDistrict.icon}</span>
              <div>
                <h3 style={{ color: selectedDistrict.color, fontSize: '1rem' }}>
                  {selectedDistrict.name}
                </h3>
                <span className="badge badge-medium" style={{ marginTop: '0.25rem' }}>
                  {selectedDistrict.topic}
                </span>
              </div>
            </div>

            <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '1rem', lineHeight: 1.7 }}>
              {selectedDistrict.description}
            </p>

            {/* Progress */}
            <div style={{ marginBottom: '1.5rem' }}>
              <div className="flex-between" style={{ marginBottom: '0.5rem' }}>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontFamily: 'var(--font-display)' }}>
                  PROGRESS
                </span>
                <span style={{ fontSize: '0.85rem', color: selectedDistrict.color, fontWeight: 700 }}>
                  {selectedDistrict.missions_completed}/{selectedDistrict.total_missions}
                </span>
              </div>
              <div className="district-progress-bar">
                <div
                  className="district-progress-fill"
                  style={{
                    width: `${(selectedDistrict.missions_completed / Math.max(1, selectedDistrict.total_missions)) * 100}%`,
                    background: selectedDistrict.color,
                  }}
                />
              </div>
            </div>

            {selectedDistrict.is_unlocked ? (
              <button
                className="btn btn-primary"
                style={{ width: '100%' }}
                onClick={() => navigate(`/district/${selectedDistrict.id}`)}
              >
                🎯 Enter District
              </button>
            ) : (
              <div style={{
                padding: '1rem',
                background: 'rgba(255, 0, 64, 0.05)',
                border: '1px solid rgba(255, 0, 64, 0.2)',
                borderRadius: 'var(--radius-md)',
                textAlign: 'center',
                color: 'var(--neon-red)',
                fontSize: '0.85rem',
              }}>
                🔒 Complete more missions in previous districts to unlock
              </div>
            )}
          </div>
        ) : (
          <div style={{ textAlign: 'center', paddingTop: '3rem', color: 'var(--text-muted)' }}>
            <div style={{ fontSize: '3rem', marginBottom: '1rem', opacity: 0.5 }}>🗺️</div>
            <h4 style={{ marginBottom: '0.5rem' }}>SELECT A DISTRICT</h4>
            <p style={{ fontSize: '0.85rem' }}>Click on a district node to view its details and missions</p>
          </div>
        )}

        {/* District list */}
        <div style={{ marginTop: '2rem' }}>
          <h4 style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '1rem', letterSpacing: '0.1em' }}>
            ALL DISTRICTS
          </h4>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            {districts.map((d) => (
              <div
                key={d.id}
                className={`district-card ${!d.is_unlocked ? 'locked' : ''}`}
                style={{ '--district-color': d.color, padding: '0.75rem 1rem 0.75rem 1.25rem', cursor: d.is_unlocked ? 'pointer' : 'not-allowed' }}
                onClick={() => d.is_unlocked && setSelectedDistrict(d)}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                  <span style={{ fontSize: '1.25rem' }}>{d.is_unlocked ? d.icon : '🔒'}</span>
                  <div style={{ flex: 1 }}>
                    <div className="district-name" style={{ fontSize: '0.75rem' }}>{d.name}</div>
                    <div className="district-topic" style={{ fontSize: '0.7rem' }}>{d.topic}</div>
                  </div>
                  <span style={{
                    fontSize: '0.7rem', fontFamily: 'var(--font-mono)',
                    color: d.is_unlocked ? d.color : 'var(--text-muted)',
                  }}>
                    {d.missions_completed}/{d.total_missions}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
