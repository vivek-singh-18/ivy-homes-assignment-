import { useState, useEffect } from 'react';
import api from '../api';

export default function Rentals() {
  const [rentals, setRentals] = useState([]);

  useEffect(() => {
    api.get(`/v1/rentals?limit=50`).then(res => setRentals(res.data.results));
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
