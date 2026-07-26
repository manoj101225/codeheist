import { useState, useEffect } from 'react';
import { getLeaderboard } from '../services/api';

export default function LeaderboardPage() {
  const [leaders, setLeaders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadLeaderboard();
  }, []);

  const loadLeaderboard = async () => {
    try {
      const data = await getLeaderboard();
      setLeaders(data);
    } catch (err) {
      console.error('Failed to load leaderboard:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex-center" style={{ height: 'calc(100vh - 64px)' }}>
        <h3 style={{ color: 'var(--neon-cyan)' }}>LOADING MOST WANTED...</h3>
      </div>
    );
  }

  return (
    <div className="page-container animate-fadeIn">
      <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
        <h1 style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>
          <span style={{ color: 'var(--neon-yellow)' }}>🏆</span> CRIMINAL UNDERWORLD
        </h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
          The most notorious coders in the city
        </p>
      </div>

      <div style={{ maxWidth: '800px', margin: '0 auto' }}>
        <table className="leaderboard-table">
          <thead>
            <tr>
              <th>Rank</th>
              <th>Operative</th>
              <th>Title</th>
              <th>Missions</th>
              <th>Reputation</th>
            </tr>
          </thead>
          <tbody>
            {leaders.map((l) => (
              <tr key={l.rank}>
                <td>
                  <span className={`leaderboard-rank ${l.rank <= 3 ? `top-${l.rank}` : ''}`}>
                    {l.rank <= 3 ? ['🥇', '🥈', '🥉'][l.rank - 1] : `#${l.rank}`}
                  </span>
                </td>
                <td>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                    <div style={{
                      width: '32px', height: '32px', borderRadius: '50%',
                      background: 'linear-gradient(135deg, var(--neon-red), var(--neon-purple))',
                      display: 'flex', alignItems: 'center', justifyContent: 'center',
                      fontSize: '0.75rem', fontWeight: 800, fontFamily: 'var(--font-display)',
                    }}>
                      {l.username.charAt(0).toUpperCase()}
                    </div>
                    <span style={{ fontWeight: 600 }}>{l.username}</span>
                  </div>
                </td>
                <td>
                  <span style={{
                    fontFamily: 'var(--font-display)', fontSize: '0.7rem',
                    color: 'var(--neon-cyan)', letterSpacing: '0.05em',
                  }}>
                    {l.player_rank}
                  </span>
                </td>
                <td>
                  <span style={{ fontFamily: 'var(--font-mono)', color: 'var(--neon-green)' }}>
                    {l.missions_completed}
                  </span>
                </td>
                <td>
                  <span style={{
                    fontFamily: 'var(--font-display)', fontWeight: 700,
                    color: 'var(--neon-yellow)', fontSize: '1rem',
                  }}>
                    ⭐ {l.reputation}
                  </span>
                </td>
              </tr>
            ))}
            {leaders.length === 0 && (
              <tr>
                <td colSpan={5} style={{ textAlign: 'center', color: 'var(--text-muted)', padding: '3rem' }}>
                  No operatives on the board yet. Be the first!
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
