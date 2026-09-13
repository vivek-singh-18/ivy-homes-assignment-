import { useState, useEffect } from 'react';
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
