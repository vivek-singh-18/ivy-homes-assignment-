import { useState, useEffect } from 'react';
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
