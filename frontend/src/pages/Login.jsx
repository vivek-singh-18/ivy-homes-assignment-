import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

export default function Login() {
  const [email, setEmail] = useState('demo1@ivy.homes');
  const [password, setPassword] = useState('');
  const [apiKey, setApiKey] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const activeApiKey = apiKey || import.meta.env.VITE_IVY_API_KEY;
      const res = await axios.post('https://solve.ivy.homes/auth/login', {
        email, password
      }, {
        headers: { 'X-API-Key': activeApiKey }
      });
      
      localStorage.setItem('access_token', res.data.access_token);
      localStorage.setItem('refresh_token', res.data.refresh_token);
      if (apiKey) {
        localStorage.setItem('ivy_api_key', apiKey);
      }
      navigate('/');
    } catch (err) {
      setError('Login failed: ' + (err.response?.data?.message || err.message));
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-200">
      <form onSubmit={handleLogin} className="bg-white p-8 rounded shadow-md w-96 flex flex-col gap-4">
        <h2 className="text-2xl font-bold mb-4">Ivy Homes Login</h2>
        <p className="text-sm text-gray-600 mb-2">Since the API Key cannot be publicly hosted, please enter it below if you are testing the deployed build.</p>
        {error && <p className="text-red-500 text-sm">{error}</p>}
        <input className="border p-2 rounded" type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} required />
        <input className="border p-2 rounded" type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} required />
        <input className="border p-2 rounded" type="text" placeholder="API Key (e.g. IVY26-...)" value={apiKey} onChange={e => setApiKey(e.target.value)} />
        <button className="bg-blue-600 text-white p-2 rounded hover:bg-blue-700" type="submit">Login</button>
      </form>
    </div>
  );
}
