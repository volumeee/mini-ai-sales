import { useState, useEffect, useCallback } from 'react';
import { salesApi } from '../api/client';

const LIMIT = 20;

const formatCurrency = (value) =>
  new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    maximumFractionDigits: 0,
  }).format(value);

export default function SalesTable() {
  const [sales, setSales] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [total, setTotal] = useState(0);
  const [search, setSearch] = useState('');
  const [searchInput, setSearchInput] = useState('');

  const fetchSales = useCallback(async () => {
    setLoading(true);
    setError('');

    try {
      const { data } = await salesApi.getAll(page, LIMIT, search);
      setSales(data.data);
      setTotalPages(data.total_pages);
      setTotal(data.total);
    } catch (err) {
      setError(err.response?.data?.detail || 'Gagal memuat data penjualan');
    } finally {
      setLoading(false);
    }
  }, [page, search]);

  useEffect(() => {
    fetchSales();
  }, [fetchSales]);

  const handleSearch = (e) => {
    e.preventDefault();
    setPage(1);
    setSearch(searchInput);
  };

  const handleClearSearch = () => {
    setSearchInput('');
    setSearch('');
    setPage(1);
  };

  return (
    <div className="bg-white rounded-xl shadow-sm p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-gray-900">📋 Data Penjualan</h2>
        <span className="px-2.5 py-1 bg-indigo-50 text-indigo-600 rounded-full text-xs font-semibold">
          {total} produk
        </span>
      </div>

      {/* Search */}
      <form onSubmit={handleSearch} className="flex gap-2 mb-4">
        <input
          type="text"
          id="search-input"
          value={searchInput}
          onChange={(e) => setSearchInput(e.target.value)}
          placeholder="Cari product ID atau nama..."
          className="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm outline-none
                     focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/10 transition"
        />
        <button type="submit" className="px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700 transition">
          Cari
        </button>
        {search && (
          <button type="button" onClick={handleClearSearch} className="px-3 py-2 border border-gray-300 text-gray-600 rounded-lg text-sm hover:bg-gray-50 transition">
            ✕ Reset
          </button>
        )}
      </form>

      {/* Error */}
      {error && (
        <div className="bg-red-50 text-red-600 text-sm px-4 py-3 rounded-lg border border-red-200 mb-4">
          {error}
        </div>
      )}

      {/* Table */}
      <div className="overflow-x-auto border border-gray-200 rounded-lg">
        <table className="w-full text-sm">
          <thead className="bg-gray-50">
            <tr>
              {['Product ID', 'Nama Produk', 'Jumlah Penjualan', 'Harga', 'Diskon', 'Status'].map((h) => (
                <th key={h} className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider border-b border-gray-200">
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan="6" className="text-center py-8 text-gray-400">Loading...</td>
              </tr>
            ) : sales.length === 0 ? (
              <tr>
                <td colSpan="6" className="text-center py-8 text-gray-400">Tidak ada data</td>
              </tr>
            ) : (
              sales.map((item) => (
                <tr key={item.product_id} className="hover:bg-gray-50 transition-colors">
                  <td className="px-4 py-2.5 border-b border-gray-100">
                    <code className="px-1.5 py-0.5 bg-gray-100 rounded text-xs text-gray-600">{item.product_id}</code>
                  </td>
                  <td className="px-4 py-2.5 border-b border-gray-100 text-gray-700">{item.product_name}</td>
                  <td className="px-4 py-2.5 border-b border-gray-100 text-gray-700">{item.jumlah_penjualan}</td>
                  <td className="px-4 py-2.5 border-b border-gray-100 text-gray-700">{formatCurrency(item.harga)}</td>
                  <td className="px-4 py-2.5 border-b border-gray-100 text-gray-700">{item.diskon}%</td>
                  <td className="px-4 py-2.5 border-b border-gray-100">
                    <span className={`inline-block px-2.5 py-0.5 rounded-full text-xs font-semibold
                      ${item.status === 'Laris'
                        ? 'bg-emerald-50 text-emerald-600'
                        : 'bg-red-50 text-red-600'
                      }`}>
                      {item.status}
                    </span>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex items-center justify-center gap-4 mt-4 pt-4 border-t border-gray-200">
          <button
            onClick={() => setPage((p) => Math.max(1, p - 1))}
            disabled={page === 1}
            className="px-3 py-1.5 border border-gray-300 text-gray-700 rounded-lg text-sm hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition"
          >
            ← Prev
          </button>
          <span className="text-sm text-gray-500">
            Halaman {page} dari {totalPages}
          </span>
          <button
            onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
            disabled={page === totalPages}
            className="px-3 py-1.5 border border-gray-300 text-gray-700 rounded-lg text-sm hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition"
          >
            Next →
          </button>
        </div>
      )}
    </div>
  );
}
