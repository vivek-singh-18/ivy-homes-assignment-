import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

export default function Login() {
  const [email, setEmail] = useState('demo1@ivy.homes');
  const [password, setPassword] = useState(import.meta.env.VITE_DEMO_PASSWORD || '');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post('https://challenge-api.ivy.homes/auth/login', {
        email, password
      }, {
        headers: { 'X-API-Key': import.meta.env.VITE_IVY_API_KEY }
      });
      localStorage.setItem('access_token', res.data.access_token);
      localStorage.setItem('refresh_token', res.data.refresh_token);
      navigate('/');
    } catch (err) {
      setError('Login failed');
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-200">
      <form onSubmit={handleLogin} className="bg-white p-8 rounded shadow-md w-96 flex flex-col gap-4">
        <h2 className="text-2xl font-bold mb-4">Ivy Homes Login</h2>
        {error && <p className="text-red-500">{error}</p>}
        <input className="border p-2 rounded" type="email" value={email} onChange={e => setEmail(e.target.value)} required />
        <input className="border p-2 rounded" type="password" value={password} onChange={e => setPassword(e.target.value)} required />
        <button className="bg-blue-600 text-white p-2 rounded hover:bg-blue-700" type="submit">Login</button>
      </form>
    </div>
  );
}
