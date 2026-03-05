import { useState } from 'react';
import { predictApi } from '../api/client';

const INITIAL_FORM = { jumlah_penjualan: '', harga: '', diskon: '' };

const formatCurrency = (value) =>
  new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    maximumFractionDigits: 0,
  }).format(value);

const FIELDS = [
  { name: 'jumlah_penjualan', label: 'Jumlah Penjualan', placeholder: 'Contoh: 150', min: 0 },
  { name: 'harga', label: 'Harga (Rp)', placeholder: 'Contoh: 50000', min: 0 },
  { name: 'diskon', label: 'Diskon (%)', placeholder: 'Contoh: 10', min: 0, max: 100 },
];

export default function PredictForm() {
  const [form, setForm] = useState(INITIAL_FORM);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  const getErrorMsg = (err) => {
    const detail = err.response?.data?.detail;
    if (Array.isArray(detail)) return detail[0]?.msg || 'Terjadi kesalahan input';
    if (typeof detail === 'object') return detail.msg || JSON.stringify(detail);
    return detail || 'Prediksi gagal. Periksa koneksi atau model.';
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setResult(null);
    setLoading(true);

    try {
      const { data } = await predictApi.predict(
        parseInt(form.jumlah_penjualan),
        parseInt(form.harga),
        parseInt(form.diskon)
      );
      setResult(data);
    } catch (err) {
      setError(getErrorMsg(err));
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setForm(INITIAL_FORM);
    setResult(null);
    setError('');
  };

  const isLaris = result?.status === 'Laris';

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-start">
      {/* Form Card */}
      <div className="bg-white rounded-xl shadow-sm p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-1">🤖 Prediksi Status Produk</h2>
        <p className="text-gray-500 text-sm mb-5 leading-relaxed">
          Masukkan data produk untuk memprediksi apakah produk akan <strong>Laris</strong> atau <strong>Tidak Laris</strong>.
        </p>

        <form onSubmit={handleSubmit} className="space-y-4">
          {FIELDS.map(({ name, label, placeholder, min, max }) => (
            <div key={name} className="space-y-1.5">
              <label htmlFor={name} className="text-sm font-medium text-gray-700">
                {label}
              </label>
              <input
                id={name}
                name={name}
                type="number"
                min={min}
                max={max}
                value={form[name]}
                onChange={handleChange}
                placeholder={placeholder}
                required
                className="w-full px-3 py-2.5 border border-gray-300 rounded-lg text-sm outline-none
                           focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/10 transition"
              />
            </div>
          ))}

          {error && (
            <div className="bg-red-50 text-red-600 text-sm px-4 py-3 rounded-lg border border-red-200">
              {error}
            </div>
          )}

          <div className="flex gap-2 pt-2">
            <button
              type="submit"
              disabled={loading}
              className="px-5 py-2.5 bg-indigo-600 text-white rounded-lg text-sm font-medium
                         hover:bg-indigo-700 disabled:opacity-60 disabled:cursor-not-allowed transition"
            >
              {loading ? 'Memprediksi...' : '🔮 Prediksi'}
            </button>
            <button
              type="button"
              onClick={handleReset}
              className="px-5 py-2.5 border border-gray-300 text-gray-700 rounded-lg text-sm
                         hover:bg-gray-50 transition"
            >
              Reset
            </button>
          </div>
        </form>
      </div>

      {/* Result Card */}
      {result && (
        <div className={`rounded-xl p-6 border-2
          ${isLaris
            ? 'border-emerald-500 bg-gradient-to-b from-emerald-50 to-white'
            : 'border-red-500 bg-gradient-to-b from-red-50 to-white'
          }`}>
          <div className="flex items-center gap-3 mb-4">
            <span className="text-3xl">{isLaris ? '🔥' : '📉'}</span>
            <h2 className="text-lg font-semibold text-gray-900">Hasil Prediksi</h2>
          </div>

          <div className="text-center mb-5">
            <span className={`inline-block px-6 py-2 rounded-full text-xl font-bold
              ${isLaris ? 'bg-emerald-50 text-emerald-600' : 'bg-red-50 text-red-600'}`}>
              {result.status}
            </span>
          </div>

          <div className="grid grid-cols-2 gap-3">
            {[
              { label: 'Confidence', value: `${(result.confidence * 100).toFixed(1)}%` },
              { label: 'Jumlah Penjualan', value: result.input_data.jumlah_penjualan },
              { label: 'Harga', value: formatCurrency(result.input_data.harga) },
              { label: 'Diskon', value: `${result.input_data.diskon}%` },
            ].map(({ label, value }) => (
              <div key={label} className="p-3 bg-white/60 rounded-lg border border-gray-200">
                <span className="text-xs text-gray-500 uppercase tracking-wide">{label}</span>
                <p className="text-base font-semibold text-gray-800 mt-0.5">{value}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
