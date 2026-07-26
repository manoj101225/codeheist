import { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { isAuthenticated, getMyProgress } from './services/api';
import HUDNavbar from './components/Navbar/HUDNavbar';
import AuthPage from './pages/AuthPage';
import MapOverview from './pages/MapOverview';
import DistrictPage from './pages/DistrictPage';
import MissionPage from './pages/MissionPage';
import ProfilePage from './pages/ProfilePage';
import LeaderboardPage from './pages/LeaderboardPage';
import './index.css';

function App() {
  const [user, setUser] = useState(null);
  const [authChecked, setAuthChecked] = useState(false);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    if (isAuthenticated()) {
      try {
        const data = await getMyProgress();
        setUser(data.user);
      } catch {
        // Token expired or invalid
        localStorage.removeItem('codeheist_token');
      }
    }
    setAuthChecked(true);
  };

  const handleAuth = (userData) => {
    setUser(userData);
  };

  const handleMissionComplete = (result) => {
    if (user && result.reputation_gained) {
      setUser((prev) => ({
        ...prev,
        reputation: (prev.reputation || 0) + result.reputation_gained,
        missions_completed: (prev.missions_completed || 0) + 1,
      }));
    }
  };

  if (!authChecked) {
    return (
      <div className="flex-center" style={{ height: '100vh' }}>
        <div style={{ textAlign: 'center' }}>
          <h1 style={{
            fontFamily: 'var(--font-display)', fontSize: '3rem', fontWeight: 900,
            background: 'linear-gradient(135deg, #ff0040, #00f0ff)',
            WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
            marginBottom: '1rem',
          }}>
            CODEHEIST
          </h1>
          <p style={{ color: 'var(--text-muted)', fontFamily: 'var(--font-display)', fontSize: '0.8rem', letterSpacing: '0.2em' }}>
            INITIALIZING...
          </p>
        </div>
      </div>
    );
  }

  return (
    <BrowserRouter>
      {user && <HUDNavbar user={user} />}
      <Routes>
        <Route
          path="/auth"
          element={user ? <Navigate to="/map" /> : <AuthPage onAuth={handleAuth} />}
        />
        <Route
          path="/map"
          element={user ? <MapOverview /> : <Navigate to="/auth" />}
        />
        <Route
          path="/district/:id"
          element={user ? <DistrictPage /> : <Navigate to="/auth" />}
        />
        <Route
          path="/mission/:id"
          element={user ? <MissionPage onMissionComplete={handleMissionComplete} /> : <Navigate to="/auth" />}
        />
        <Route
          path="/profile"
          element={user ? <ProfilePage /> : <Navigate to="/auth" />}
        />
        <Route
          path="/leaderboard"
          element={user ? <LeaderboardPage /> : <Navigate to="/auth" />}
        />
        <Route
          path="*"
          element={<Navigate to={user ? '/map' : '/auth'} />}
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
