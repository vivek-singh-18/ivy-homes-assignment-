import os

os.makedirs("frontend/src/pages", exist_ok=True)

with open("frontend/src/pages/Login.jsx", "w") as f:
    f.write("""import { useState } from 'react';
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
""")

with open("frontend/src/pages/Listings.jsx", "w") as f:
    f.write("""import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../api';

export default function Listings() {
  const [listings, setListings] = useState([]);
  const [page, setPage] = useState(0);
  const [hasMore, setHasMore] = useState(true);
  const limit = 50;
  const navigate = useNavigate();

  useEffect(() => {
    if(!localStorage.getItem('access_token')) navigate('/login');
    fetchListings(0);
  }, []);

  const fetchListings = async (p) => {
    try {
      const res = await api.get(`/v1/listings?offset=${p * limit}&limit=${limit}`);
      const activeListings = res.data.listings.filter(l => l.is_live);
      if (res.data.listings.length < limit) setHasMore(false);
      
      setListings(prev => p === 0 ? activeListings : [...prev, ...activeListings]);
    } catch (err) {
      console.error(err);
    }
  };

  const loadMore = () => {
    const next = page + 1;
    setPage(next);
    fetchListings(next);
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Active Listings</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {listings.map(l => (
          <Link to={`/listing/${l.listing_id}`} key={l.listing_id} className="bg-white p-4 rounded shadow hover:shadow-lg transition">
            <h2 className="text-xl font-semibold">{l.title}</h2>
            <p className="text-gray-600">{l.locality} - {l.bedroom} BHK</p>
            <p className="font-bold mt-2 text-blue-600">₹{l.price.toLocaleString()}</p>
          </Link>
        ))}
      </div>
      {hasMore && <button onClick={loadMore} className="mt-8 bg-blue-500 text-white px-4 py-2 rounded">Load More</button>}
    </div>
  );
}
""")

with open("frontend/src/pages/ListingDetail.jsx", "w") as f:
    f.write("""import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api';

export default function ListingDetail() {
  const { id } = useParams();
  const [listing, setListing] = useState(null);
  const [isSaved, setIsSaved] = useState(false);

  useEffect(() => {
    api.get(`/v1/listings/${id}`).then(res => setListing(res.data));
    const saved = JSON.parse(localStorage.getItem('saved_listings') || '[]');
    setIsSaved(saved.some(l => l.listing_id === id));
  }, [id]);

  const toggleSave = () => {
    let saved = JSON.parse(localStorage.getItem('saved_listings') || '[]');
    if (isSaved) {
      saved = saved.filter(l => l.listing_id !== id);
    } else {
      if(listing) saved.push(listing);
    }
    localStorage.setItem('saved_listings', JSON.stringify(saved));
    setIsSaved(!isSaved);
  };

  if (!listing) return <div>Loading...</div>;

  return (
    <div className="bg-white p-8 rounded shadow max-w-3xl mx-auto">
      <div className="flex justify-between items-start">
        <h1 className="text-3xl font-bold">{listing.title}</h1>
        <button onClick={toggleSave} className={`px-4 py-2 rounded text-white ${isSaved ? 'bg-red-500' : 'bg-green-500'}`}>
          {isSaved ? 'Unsave' : 'Save'}
        </button>
      </div>
      <p className="text-gray-500 text-lg">{listing.apartment_name}, {listing.locality}</p>
      
      <div className="grid grid-cols-2 gap-4 mt-6">
        <div><strong>Price:</strong> ₹{listing.price.toLocaleString()}</div>
        <div><strong>Type:</strong> {listing.property_type}</div>
        <div><strong>BHK:</strong> {listing.bedroom} Bed, {listing.bathroom} Bath</div>
        <div><strong>Area:</strong> {listing.carpet_area} sqft</div>
        <div><strong>Floor:</strong> {listing.floor} of {listing.total_floors}</div>
        <div><strong>Furnishing:</strong> {listing.furnishing}</div>
        <div><strong>Facing:</strong> {listing.facing_direction}</div>
        <div><strong>Posted By:</strong> {listing.posted_by_name} ({listing.posted_by})</div>
      </div>
      <div className="mt-6">
        <h3 className="font-bold text-xl mb-2">Description</h3>
        <p className="text-gray-700 whitespace-pre-wrap">{listing.description}</p>
      </div>
    </div>
  );
}
""")

with open("frontend/src/pages/Saved.jsx", "w") as f:
    f.write("""import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

export default function Saved() {
  const [saved, setSaved] = useState([]);

  useEffect(() => {
    setSaved(JSON.parse(localStorage.getItem('saved_listings') || '[]'));
  }, []);

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Saved Properties</h1>
      {saved.length === 0 ? <p>No saved properties.</p> : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {saved.map(l => (
            <Link to={`/listing/${l.listing_id}`} key={l.listing_id} className="bg-white p-4 rounded shadow hover:shadow-lg transition">
              <h2 className="text-xl font-semibold">{l.title}</h2>
              <p className="text-gray-600">{l.locality} - {l.bedroom} BHK</p>
              <p className="font-bold mt-2 text-blue-600">₹{l.price.toLocaleString()}</p>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
""")

with open("frontend/src/pages/Rentals.jsx", "w") as f:
    f.write("""import { useState, useEffect } from 'react';
import api from '../api';

export default function Rentals() {
  const [rentals, setRentals] = useState([]);

  useEffect(() => {
    api.get(`/v1/rentals?limit=50`).then(res => setRentals(res.data.rentals));
  }, []);

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Rentals</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {rentals.map(l => (
          <div key={l.listing_id} className="bg-white p-4 rounded shadow">
            <h2 className="text-xl font-semibold">{l.title}</h2>
            <p className="text-gray-600">{l.locality} - {l.bedroom} BHK</p>
            <p className="font-bold mt-2 text-blue-600">₹{l.price.toLocaleString()} / month</p>
          </div>
        ))}
      </div>
    </div>
  );
}
""")

with open("frontend/src/pages/Projects.jsx", "w") as f:
    f.write("""import { useState, useEffect } from 'react';
import api from '../api';

export default function Projects() {
  const [projects, setProjects] = useState([]);

  useEffect(() => {
    api.get(`/v1/projects`).then(res => setProjects(res.data.projects));
  }, []);

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Projects</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {projects.map(p => (
          <div key={p.project_id} className="bg-white p-6 rounded shadow">
            <h2 className="text-2xl font-semibold">{p.apartment_name}</h2>
            <p className="text-gray-600">{p.developer_name} • {p.locality}</p>
            <div className="mt-4 flex gap-4 text-sm text-gray-700">
              <div><strong>Status:</strong> {p.project_status}</div>
              <div><strong>Units:</strong> {p.total_units}</div>
              <div><strong>Towers:</strong> {p.total_towers}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
""")

with open("frontend/src/pages/Insights.jsx", "w") as f:
    f.write("""import { useEffect, useState } from 'react';

export default function Insights() {
  return (
    <div className="bg-white p-8 rounded shadow max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6 text-blue-700">Analytics Insights (Phase 3 Answers)</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <InsightBox title="Total Listing Records" value="4400" />
        <InsightBox title="Unique Properties" value="4362" />
        <InsightBox title="Active Listings" value="3477" />
        <InsightBox title="Total Monthly Rent (Kukatpally)" value="₹6,717,600" />
        <InsightBox title="Avg Price / Sqft (2BHK)" value="₹9,085.59" />
        <InsightBox title="Costliest Project" value="P20165 (₹9,980,000)" />
        <InsightBox title="Listings Last 7 Days" value="141" />
        <InsightBox title="Projects With Wrong Count" value="129" />
      </div>
    </div>
  );
}

function InsightBox({ title, value }) {
  return (
    <div className="border border-gray-200 p-4 rounded bg-gray-50 flex flex-col justify-center">
      <div className="text-gray-500 text-sm font-semibold uppercase">{title}</div>
      <div className="text-2xl font-bold mt-1 text-gray-800">{value}</div>
    </div>
  );
}
""")
