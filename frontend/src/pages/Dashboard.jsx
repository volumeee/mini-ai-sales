import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import SalesTable from '../components/SalesTable';
import PredictForm from '../components/PredictForm';

const TABS = [
  { key: 'sales', label: '📋 Data Penjualan' },
  { key: 'predict', label: '🤖 Prediksi Produk' },
];

export default function Dashboard() {
  const { user, logout } = useAuth();
  const [activeTab, setActiveTab] = useState('sales');

  return (
    <div className="max-w-6xl mx-auto px-4 py-6">
      {/* Header */}
      <header className="flex items-center justify-between mb-6 pb-4 border-b border-gray-200">
        <div className="flex items-center gap-3">
          <span className="text-3xl">📊</span>
          <h1 className="text-xl font-bold text-gray-900">Sales Dashboard</h1>
        </div>
        <div className="flex items-center gap-3">
          <span className="px-3 py-1.5 bg-indigo-50 text-indigo-600 rounded-full text-xs font-medium">
            👤 {user?.username}
          </span>
          <button
            onClick={logout}
            className="px-3 py-1.5 border border-gray-300 text-gray-700 rounded-lg text-sm
                       hover:bg-gray-50 transition"
          >
            Logout
          </button>
        </div>
      </header>

      {/* Tabs */}
      <div className="flex gap-1 bg-gray-100 p-1 rounded-lg w-fit mb-6">
        {TABS.map(({ key, label }) => (
          <button
            key={key}
            onClick={() => setActiveTab(key)}
            className={`px-5 py-2 rounded-md text-sm font-medium transition
              ${activeTab === key
                ? 'bg-white text-indigo-600 shadow-sm'
                : 'text-gray-500 hover:text-gray-700'
              }`}
          >
            {label}
          </button>
        ))}
      </div>

      {/* Content */}
      <main>
        {activeTab === 'sales' ? <SalesTable /> : <PredictForm />}
      </main>
    </div>
  );
}
