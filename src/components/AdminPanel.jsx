import { useState, useEffect } from 'react';

export default function AdminPanel({ onBack }) {
  const [tab, setTab] = useState('appointments');
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    fetch(`/api/admin/${tab}`)
      .then((r) => r.json())
      .then((json) => {
        setData(json[tab] || []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [tab]);

  return (
    <div className="min-h-screen bg-gray-50 p-4 md:p-8">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Admin Dashboard</h1>
            <p className="text-gray-500 text-sm">Eric's Auto Care</p>
          </div>
          <button
            onClick={onBack}
            className="text-sm text-indigo-600 hover:text-indigo-800 font-medium"
          >
            &larr; Back to Chat
          </button>
        </div>

        <div className="flex gap-2 mb-4">
          <button
            onClick={() => setTab('appointments')}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              tab === 'appointments'
                ? 'bg-indigo-600 text-white'
                : 'bg-white text-gray-700 border border-gray-200 hover:bg-gray-50'
            }`}
          >
            Appointments
          </button>
          <button
            onClick={() => setTab('inquiries')}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              tab === 'inquiries'
                ? 'bg-indigo-600 text-white'
                : 'bg-white text-gray-700 border border-gray-200 hover:bg-gray-50'
            }`}
          >
            Inquiries
          </button>
        </div>

        {loading ? (
          <p className="text-gray-500 text-sm">Loading...</p>
        ) : data.length === 0 ? (
          <div className="bg-white rounded-xl border border-gray-200 p-8 text-center text-gray-500">
            No {tab} yet.
          </div>
        ) : (
          <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="bg-gray-50 border-b border-gray-200">
                  <tr>
                    {tab === 'appointments' ? (
                      <>
                        <th className="text-left px-4 py-3 font-medium text-gray-600">Name</th>
                        <th className="text-left px-4 py-3 font-medium text-gray-600">Service</th>
                        <th className="text-left px-4 py-3 font-medium text-gray-600">Date</th>
                        <th className="text-left px-4 py-3 font-medium text-gray-600">Time</th>
                        <th className="text-left px-4 py-3 font-medium text-gray-600">Phone</th>
                        <th className="text-left px-4 py-3 font-medium text-gray-600">Created</th>
                      </>
                    ) : (
                      <>
                        <th className="text-left px-4 py-3 font-medium text-gray-600">Name</th>
                        <th className="text-left px-4 py-3 font-medium text-gray-600">Message</th>
                        <th className="text-left px-4 py-3 font-medium text-gray-600">Contact</th>
                        <th className="text-left px-4 py-3 font-medium text-gray-600">Created</th>
                      </>
                    )}
                  </tr>
                </thead>
                <tbody>
                  {data.map((row) => (
                    <tr key={row.id} className="border-b border-gray-100 hover:bg-gray-50">
                      {tab === 'appointments' ? (
                        <>
                          <td className="px-4 py-3 font-medium">{row.customer_name}</td>
                          <td className="px-4 py-3 capitalize">{row.service}</td>
                          <td className="px-4 py-3">{row.appointment_date}</td>
                          <td className="px-4 py-3">{row.appointment_time?.slice(0, 5)}</td>
                          <td className="px-4 py-3">{row.phone}</td>
                          <td className="px-4 py-3 text-gray-400">{new Date(row.created_at).toLocaleString()}</td>
                        </>
                      ) : (
                        <>
                          <td className="px-4 py-3 font-medium">{row.customer_name}</td>
                          <td className="px-4 py-3 max-w-xs truncate">{row.message}</td>
                          <td className="px-4 py-3">{row.contact}</td>
                          <td className="px-4 py-3 text-gray-400">{new Date(row.created_at).toLocaleString()}</td>
                        </>
                      )}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
