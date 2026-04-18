import { useState } from 'react';

function CropRecommendation() {
  const [formData, setFormData] = useState({
    nitrogen: '',
    phosphorus: '',
    potassium: '',
    temperature: '',
    humidity: '',
    ph: '',
    rainfall: ''
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await fetch('http://localhost:5000/api/crop-predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Error:', error);
      setResult({ error: 'Failed to get prediction' });
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-eco-cream py-20">
      <div className="max-w-2xl mx-auto px-6">
        <h1 className="text-4xl font-bold text-eco-green-dark mb-8">Crop Recommendation</h1>
        
        <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-lg p-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Nitrogen (N)</label>
              <input
                type="number"
                name="nitrogen"
                value={formData.nitrogen}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-eco-green"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Phosphorus (P)</label>
              <input
                type="number"
                name="phosphorus"
                value={formData.phosphorus}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-eco-green"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Potassium (K)</label>
              <input
                type="number"
                name="potassium"
                value={formData.potassium}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-eco-green"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Temperature (°C)</label>
              <input
                type="number"
                name="temperature"
                value={formData.temperature}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-eco-green"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Humidity (%)</label>
              <input
                type="number"
                name="humidity"
                value={formData.humidity}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-eco-green"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">pH</label>
              <input
                type="number"
                name="ph"
                value={formData.ph}
                onChange={handleChange}
                step="0.1"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-eco-green"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Rainfall (mm)</label>
              <input
                type="number"
                name="rainfall"
                value={formData.rainfall}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-eco-green"
                required
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="mt-8 w-full bg-eco-green text-white font-semibold py-3 rounded-lg hover:bg-eco-green-dark transition-colors disabled:opacity-50"
          >
            {loading ? 'Predicting...' : 'Get Recommendation'}
          </button>
        </form>

        {result && (
          <div className="mt-8 bg-white rounded-lg shadow-lg p-8">
            {result.error ? (
              <p className="text-red-600">{result.error}</p>
            ) : (
              <div>
                <h2 className="text-2xl font-bold text-eco-green-dark mb-4">Recommended Crop</h2>
                <p className="text-3xl font-bold text-eco-green mb-6">{result.crop.toUpperCase()}</p>
                
                {result.explanation && (
                  <div className="bg-eco-cream rounded-lg p-6 mb-6">
                    <h3 className="text-lg font-bold text-eco-green-dark mb-3">Why This Crop?</h3>
                    <div className="text-gray-700 whitespace-pre-wrap text-sm leading-relaxed">
                      {result.explanation}
                    </div>
                  </div>
                )}
                
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div className="bg-blue-50 p-4 rounded">
                    <p className="text-gray-600">Temperature</p>
                    <p className="text-lg font-bold text-blue-600">{result.temperature}°C</p>
                  </div>
                  <div className="bg-green-50 p-4 rounded">
                    <p className="text-gray-600">Humidity</p>
                    <p className="text-lg font-bold text-green-600">{result.humidity}%</p>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default CropRecommendation;
