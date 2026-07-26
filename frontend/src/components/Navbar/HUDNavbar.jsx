import { useNavigate, useLocation } from 'react-router-dom';
import { logout } from '../../services/api';

export default function HUDNavbar({ user }) {
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate('/auth');
    window.location.reload();
  };

  const isActive = (path) => location.pathname === path ? 'active' : '';

  return (
    <nav className="hud-navbar">
      <div className="hud-logo" onClick={() => navigate('/map')}>
        CODEHEIST
      </div>

      {user && (
        <div className="hud-stats">
          <div className="hud-stat">
            <div>
              <div className="hud-stat-value">{user.rank || 'Street Punk'}</div>
              <div className="hud-stat-label">Rank</div>
            </div>
          </div>
          <div className="hud-stat">
            <div>
              <div className="hud-stat-value" style={{ color: 'var(--neon-yellow)' }}>
                ⭐ {user.reputation || 0}
              </div>
              <div className="hud-stat-label">Reputation</div>
            </div>
          </div>
          <div className="hud-stat">
            <div>
              <div className="hud-stat-value" style={{ color: 'var(--neon-green)' }}>
                🎯 {user.missions_completed || 0}
              </div>
              <div className="hud-stat-label">Missions</div>
            </div>
          </div>
        </div>
      )}

      <div className="hud-nav-links">
        <button className={`hud-nav-link ${isActive('/map')}`} onClick={() => navigate('/map')}>
          🗺️ Map
        </button>
        <button className={`hud-nav-link ${isActive('/leaderboard')}`} onClick={() => navigate('/leaderboard')}>
          🏆 Board
        </button>
        <button className={`hud-nav-link ${isActive('/profile')}`} onClick={() => navigate('/profile')}>
          👤 Profile
        </button>
        <button
          className="hud-nav-link"
          onClick={handleLogout}
          style={{ color: 'var(--neon-red)' }}
        >
          ⏻ Exit
        </button>
      </div>
    </nav>
  );
}
