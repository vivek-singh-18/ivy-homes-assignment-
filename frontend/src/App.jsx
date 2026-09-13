import { HashRouter as Router, Routes, Route, Link, useNavigate } from 'react-router-dom';
import Login from './pages/Login';
import Listings from './pages/Listings';
import ListingDetail from './pages/ListingDetail';
import Saved from './pages/Saved';
import Rentals from './pages/Rentals';
import Projects from './pages/Projects';
import Insights from './pages/Insights';

function Layout({ children }) {
  const navigate = useNavigate();
  const token = localStorage.getItem('access_token');

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-gray-100 text-gray-900">
      {token && (
        <nav className="bg-white shadow-md p-4 flex flex-wrap gap-4 items-center">
          <Link to="/" className="font-bold text-xl text-blue-600">Ivy Homes</Link>
          <Link to="/" className="hover:text-blue-500">Listings</Link>
          <Link to="/rentals" className="hover:text-blue-500">Rentals</Link>
          <Link to="/projects" className="hover:text-blue-500">Projects</Link>
          <Link to="/saved" className="hover:text-blue-500">Saved</Link>
          <Link to="/insights" className="hover:text-blue-500">Insights</Link>
          <div className="ml-auto">
            <button onClick={handleLogout} className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600">Logout</button>
          </div>
        </nav>
      )}
      <div className="p-4 md:p-6">{children}</div>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<Layout><Listings /></Layout>} />
        <Route path="/listing/:id" element={<Layout><ListingDetail /></Layout>} />
        <Route path="/saved" element={<Layout><Saved /></Layout>} />
        <Route path="/rentals" element={<Layout><Rentals /></Layout>} />
        <Route path="/projects" element={<Layout><Projects /></Layout>} />
        <Route path="/insights" element={<Layout><Insights /></Layout>} />
      </Routes>
    </Router>
  );
}

export default App;
