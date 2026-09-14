import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../api';

export default function Listings() {
  const [listings, setListings] = useState([]);
  const [page, setPage] = useState(0);
  const [hasMore, setHasMore] = useState(true);
  const limit = 50;
  const navigate = useNavigate();

  useEffect(() => {
    if(!localStorage.getItem('access_token')) return navigate('/login');
    fetchListings(0);
  }, []);

  const fetchListings = async (p) => {
    try {
      const res = await api.get(`/v1/listings?offset=${p * limit}&limit=${limit}`);
      const activeListings = res.data.results.filter(l => l.is_live);
      if (res.data.results.length < limit) setHasMore(false);
      
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
