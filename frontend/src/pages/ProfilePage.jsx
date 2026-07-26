import { useState, useEffect } from 'react';
import { getMyProgress } from '../services/api';

export default function ProfilePage() {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      const data = await getMyProgress();
      setProfile(data);
    } catch (err) {
      console.error('Failed to load profile:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex-center" style={{ height: 'calc(100vh - 64px)' }}>
        <h3 style={{ color: 'var(--neon-cyan)' }}>LOADING DOSSIER...</h3>
      </div>
    );
  }

  if (!profile) return null;

  const { user, districts, recent_attempts } = profile;

  return (
    <div className="page-container animate-fadeIn">
      {/* Profile Header */}
      <div className="profile-header">
        <div className="profile-avatar">
          {user.username.charAt(0).toUpperCase()}
        </div>
        <div className="profile-info">
          <h2>{user.username}</h2>
          <div className="profile-rank">🎖️ {user.rank}</div>
          <div style={{ display: 'flex', gap: '2rem', marginTop: '0.75rem' }}>
            <div>
              <div style={{ fontSize: '1.5rem', fontFamily: 'var(--font-display)', fontWeight: 800, color: 'var(--neon-yellow)' }}>
                {user.reputation}
              </div>
              <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', fontFamily: 'var(--font-display)', letterSpacing: '0.1em' }}>
                REPUTATION
              </div>
            </div>
            <div>
              <div style={{ fontSize: '1.5rem', fontFamily: 'var(--font-display)', fontWeight: 800, color: 'var(--neon-green)' }}>
                {user.missions_completed}
              </div>
              <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', fontFamily: 'var(--font-display)', letterSpacing: '0.1em' }}>
                MISSIONS
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="grid-2">
        {/* District Progress */}
        <div>
          <h3 style={{ fontSize: '0.8rem', color: 'var(--text-muted)', letterSpacing: '0.15em', marginBottom: '1rem' }}>
            DISTRICT PROGRESS
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            {districts.map((d) => (
              <div key={d.district_id} className="glass-card" style={{ padding: '1rem' }}>
                <div className="flex-between" style={{ marginBottom: '0.5rem' }}>
                  <div>
                    <div style={{ fontFamily: 'var(--font-display)', fontSize: '0.8rem', fontWeight: 600 }}>
                      {d.district_name}
                    </div>
                    <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>{d.topic}</div>
                  </div>
                  <span style={{
                    fontFamily: 'var(--font-mono)', fontSize: '0.8rem',
                    color: d.is_unlocked ? 'var(--neon-green)' : 'var(--text-muted)',
                  }}>
                    {d.missions_completed}/{d.total_missions}
                  </span>
                </div>
                <div className="district-progress-bar">
                  <div
                    className="district-progress-fill"
                    style={{
                      width: `${(d.missions_completed / Math.max(1, d.total_missions)) * 100}%`,
                      background: d.is_unlocked ? 'var(--neon-green)' : 'var(--text-muted)',
                    }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Recent Attempts */}
        <div>
          <h3 style={{ fontSize: '0.8rem', color: 'var(--text-muted)', letterSpacing: '0.15em', marginBottom: '1rem' }}>
            RECENT OPERATIONS
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            {recent_attempts.map((a, i) => (
              <div key={i} className="glass-card" style={{ padding: '0.75rem 1rem' }}>
                <div className="flex-between">
                  <div>
                    <span style={{
                      fontFamily: 'var(--font-mono)', fontSize: '0.75rem',
                      color: 'var(--text-secondary)',
                    }}>
                      Mission #{a.mission_id}
                    </span>
                    <span style={{
                      marginLeft: '0.75rem',
                      fontFamily: 'var(--font-display)', fontSize: '0.65rem',
                      color: 'var(--text-muted)', letterSpacing: '0.05em',
                    }}>
                      {a.language.toUpperCase()}
                    </span>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                    <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                      {a.tests_passed}/{a.tests_total}
                    </span>
                    <span className={`status-${a.status}`} style={{
                      fontFamily: 'var(--font-display)', fontSize: '0.7rem',
                      fontWeight: 700, letterSpacing: '0.05em',
                    }}>
                      {a.status.toUpperCase()}
                    </span>
                  </div>
                </div>
              </div>
            ))}
            {recent_attempts.length === 0 && (
              <div style={{ color: 'var(--text-muted)', textAlign: 'center', padding: '2rem' }}>
                No operations yet. Start your first heist!
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
