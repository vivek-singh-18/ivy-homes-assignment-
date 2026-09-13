import { useState, useEffect } from 'react';
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
