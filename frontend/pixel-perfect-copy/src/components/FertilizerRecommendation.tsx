import { useState } from 'react';

function FertilizerRecommendation() {
  const [formData, setFormData] = useState({
    crop: '',
    nitrogen: '',
    phosphorus: '',
    potassium: ''
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [activeTab, setActiveTab] = useState('manual');
  const [uploadedFiles, setUploadedFiles] = useState([]);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.crop || !formData.nitrogen || !formData.phosphorus || !formData.potassium) {
      alert('Please fill all fields');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('http://localhost:5000/api/fertilizer-recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          crop: formData.crop,
          nitrogen: parseFloat(formData.nitrogen),
          phosphorus: parseFloat(formData.phosphorus),
          potassium: parseFloat(formData.potassium)
        })
      });
      const data = await response.json();
      setResult(data);
      
      if (data.success) {
        speakResult(data);
      }
    } catch (error) {
      console.error('Error:', error);
      setResult({ success: false, error: 'Failed to get recommendation' });
    }
    setLoading(false);
  };

  const speakResult = (data) => {
    const text = `For ${data.crop}, your soil has ${data.soil_status.nitrogen.level} nitrogen, ${data.soil_status.phosphorus.level} phosphorus, and ${data.soil_status.potassium.level} potassium. Recommended fertilizer is ${data.primary_recommendation.fertilizer}. Apply ${data.primary_recommendation.quantity} at ${data.primary_recommendation.timing}.`;
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 0.9;
    utterance.pitch = 1;
    utterance.volume = 1;
    
    setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    
    window.speechSynthesis.speak(utterance);
  };

  const stopSpeaking = () => {
    window.speechSynthesis.cancel();
    setIsSpeaking(false);
  };

  const handleFileUpload = (e) => {
    const files = e.target.files;
    if (files) {
      const newFiles = Array.from(files).filter(file => file.type.includes('image'));
      if (newFiles.length > 0) {
        setUploadedFiles([...uploadedFiles, ...newFiles]);
      } else {
        alert('Please select image files');
      }
    }
  };

  const removeFile = (index) => {
    setUploadedFiles(uploadedFiles.filter((_, i) => i !== index));
  };

  const handleImagesSubmit = async (e) => {
    e.preventDefault();
    if (uploadedFiles.length === 0) {
      alert('Please select at least one image');
      return;
    }

    setLoading(true);
    try {
      // Process each image
      const results = [];
      for (const file of uploadedFiles) {
        const formDataFile = new FormData();
        formDataFile.append('file', file);

        const response = await fetch('http://localhost:5000/api/fertilizer-from-image', {
          method: 'POST',
          body: formDataFile
        });
        const data = await response.json();
        results.push({
          filename: file.name,
          data: data
        });
      }

      // Show results for all images
      setResult({ success: true, results: results });
      
      if (results.length > 0 && results[0].data.success) {
        speakResult(results[0].data.fertilizer_recommendation);
      }
    } catch (error) {
      console.error('Error:', error);
      setResult({ success: false, error: 'Failed to process images' });
    }
    setLoading(false);
  };

  const crops = ['rice', 'wheat', 'maize', 'cotton', 'potato', 'coffee'];

  return (
    <div className="min-h-screen bg-eco-cream py-20">
      <div className="max-w-4xl mx-auto px-6">
        <h1 className="text-4xl font-bold text-eco-green-dark mb-2">🧪 Fertilizer Recommendation</h1>
        <p className="text-gray-600 mb-8">Get personalized fertilizer suggestions based on your crop and soil nutrients</p>
        
        <div className="bg-white rounded-lg shadow-lg p-8">
          {/* Tab Navigation */}
          <div className="flex gap-2 mb-8 border-b-2 border-gray-200">
            <button
              onClick={() => setActiveTab('manual')}
              className={`px-6 py-3 font-semibold transition-colors whitespace-nowrap ${
                activeTab === 'manual'
                  ? 'text-eco-green border-b-4 border-eco-green'
                  : 'text-gray-600 hover:text-eco-green'
              }`}
            >
              📝 Manual Input
            </button>
            <button
              onClick={() => setActiveTab('image')}
              className={`px-6 py-3 font-semibold transition-colors whitespace-nowrap ${
                activeTab === 'image'
                  ? 'text-eco-green border-b-4 border-eco-green'
                  : 'text-gray-600 hover:text-eco-green'
              }`}
            >
              🖼️ Crop Image
            </button>
          </div>

          {/* Manual Input Tab */}
          {activeTab === 'manual' && (
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Crop Selection */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Select Crop</label>
                <select
                  name="crop"
                  value={formData.crop}
                  onChange={handleChange}
                  className="w-full px-4 py-3 border-2 border-eco-green rounded-lg focus:ring-2 focus:ring-eco-green text-lg"
                  required
                >
                  <option value="">Choose a crop...</option>
                  {crops.map(crop => (
                    <option key={crop} value={crop}>
                      {crop.charAt(0).toUpperCase() + crop.slice(1)}
                    </option>
                  ))}
                </select>
              </div>

            {/* Soil Parameters */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Nitrogen (N) mg/kg</label>
                <input
                  type="number"
                  name="nitrogen"
                  value={formData.nitrogen}
                  onChange={handleChange}
                  placeholder="e.g., 90"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-eco-green"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Phosphorus (P) mg/kg</label>
                <input
                  type="number"
                  name="phosphorus"
                  value={formData.phosphorus}
                  onChange={handleChange}
                  placeholder="e.g., 42"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-eco-green"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Potassium (K) mg/kg</label>
                <input
                  type="number"
                  name="potassium"
                  value={formData.potassium}
                  onChange={handleChange}
                  placeholder="e.g., 43"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-eco-green"
                  required
                />
              </div>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-eco-green text-white font-semibold py-3 rounded-lg hover:bg-eco-green-dark transition-colors disabled:opacity-50"
            >
              {loading ? '⏳ Analyzing...' : '🧪 Get Fertilizer Recommendation'}
            </button>
            </form>
          )}

          {/* Image Upload Tab */}
          {activeTab === 'image' && (
            <form onSubmit={handleImagesSubmit} className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Upload Crop Images</label>
                <div className="border-2 border-dashed border-eco-green rounded-lg p-8 text-center cursor-pointer hover:bg-eco-cream transition-colors">
                  <input
                    type="file"
                    accept="image/*"
                    multiple
                    onChange={handleFileUpload}
                    className="hidden"
                    id="image-input"
                  />
                  <label htmlFor="image-input" className="cursor-pointer">
                    <div className="text-4xl mb-2">🖼️</div>
                    <p className="text-gray-700 font-semibold">
                      Click to upload crop images
                    </p>
                    <p className="text-gray-500 text-sm mt-1">JPG, PNG, GIF, BMP supported - Multiple files allowed</p>
                  </label>
                </div>
              </div>

              {/* Uploaded Files List */}
              {uploadedFiles.length > 0 && (
                <div>
                  <h3 className="text-lg font-bold text-gray-800 mb-3">📁 Uploaded Files ({uploadedFiles.length})</h3>
                  <div className="space-y-2">
                    {uploadedFiles.map((file, idx) => (
                      <div key={idx} className="flex items-center justify-between bg-gray-50 p-3 rounded-lg border border-gray-300">
                        <div className="flex items-center gap-2">
                          <span className="text-lg">🖼️</span>
                          <span className="text-gray-700 font-semibold">{file.name}</span>
                          <span className="text-gray-500 text-sm">({(file.size / 1024).toFixed(2)} KB)</span>
                        </div>
                        <button
                          type="button"
                          onClick={() => removeFile(idx)}
                          className="text-red-500 hover:text-red-700 font-bold"
                        >
                          ✕
                        </button>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <div className="bg-blue-50 p-4 rounded-lg border-2 border-blue-300">
                <p className="text-blue-700 text-sm">
                  <span className="font-semibold">💡 Tip:</span> Upload multiple crop images. The system will identify each crop and recommend fertilizer for each one.
                </p>
              </div>

              <button
                type="submit"
                disabled={loading || uploadedFiles.length === 0}
                className="w-full bg-eco-green text-white font-semibold py-3 rounded-lg hover:bg-eco-green-dark transition-colors disabled:opacity-50"
              >
                {loading ? '⏳ Analyzing Images...' : `📷 Identify Crops & Recommend Fertilizer (${uploadedFiles.length})`}
              </button>
            </form>
          )}
        </div>

        {/* Results - Manual */}
        {result && activeTab === 'manual' && result.success && (
          <div className="mt-8 bg-white rounded-lg shadow-lg p-8">
            {!result.success ? (
              <div className="bg-red-50 border-2 border-red-300 rounded-lg p-6">
                <p className="text-red-700 font-semibold">❌ Error</p>
                <p className="text-red-600 mt-2">{result.error}</p>
              </div>
            ) : (
              <div>
                <h2 className="text-2xl font-bold text-eco-green-dark mb-6">
                  Fertilizer Recommendation for {result.crop.toUpperCase()}
                </h2>

                {/* Soil Status */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
                  <div className="bg-blue-50 p-4 rounded-lg border-2 border-blue-300">
                    <p className="text-gray-600 text-sm">Nitrogen Level</p>
                    <p className="text-2xl font-bold text-blue-600 mt-2">
                      {result.soil_status.nitrogen.value} mg/kg
                    </p>
                    <p className="text-sm text-blue-700 mt-1 capitalize">
                      Status: {result.soil_status.nitrogen.level}
                    </p>
                  </div>
                  <div className="bg-green-50 p-4 rounded-lg border-2 border-green-300">
                    <p className="text-gray-600 text-sm">Phosphorus Level</p>
                    <p className="text-2xl font-bold text-green-600 mt-2">
                      {result.soil_status.phosphorus.value} mg/kg
                    </p>
                    <p className="text-sm text-green-700 mt-1 capitalize">
                      Status: {result.soil_status.phosphorus.level}
                    </p>
                  </div>
                  <div className="bg-yellow-50 p-4 rounded-lg border-2 border-yellow-300">
                    <p className="text-gray-600 text-sm">Potassium Level</p>
                    <p className="text-2xl font-bold text-yellow-600 mt-2">
                      {result.soil_status.potassium.value} mg/kg
                    </p>
                    <p className="text-sm text-yellow-700 mt-1 capitalize">
                      Status: {result.soil_status.potassium.level}
                    </p>
                  </div>
                </div>

                {/* Primary Recommendation */}
                <div className="bg-eco-cream rounded-lg p-6 mb-6 border-2 border-eco-green">
                  <h3 className="text-xl font-bold text-eco-green-dark mb-4">
                    🎯 Primary Recommendation
                  </h3>
                  <div className="space-y-3">
                    <div>
                      <p className="text-sm text-gray-600">Fertilizer</p>
                      <p className="text-lg font-bold text-eco-green">
                        {result.primary_recommendation.fertilizer}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Quantity</p>
                      <p className="text-lg font-semibold text-gray-800">
                        {result.primary_recommendation.quantity}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Timing</p>
                      <p className="text-lg font-semibold text-gray-800">
                        {result.primary_recommendation.timing}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Reason</p>
                      <p className="text-gray-700 mt-1">
                        {result.primary_recommendation.reason}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Benefits</p>
                      <p className="text-gray-700 mt-1">
                        {result.primary_recommendation.benefits}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Secondary Recommendations */}
                {result.secondary_recommendations && result.secondary_recommendations.length > 0 && (
                  <div className="mb-6">
                    <h3 className="text-lg font-bold text-eco-green-dark mb-4">
                      📋 Additional Recommendations
                    </h3>
                    <div className="space-y-4">
                      {result.secondary_recommendations.map((rec, idx) => (
                        <div key={idx} className="bg-gray-50 p-4 rounded-lg border-l-4 border-eco-green">
                          <p className="font-semibold text-gray-800 mb-2">
                            {rec.details.fertilizer}
                          </p>
                          <p className="text-sm text-gray-600">
                            <span className="font-semibold">Quantity:</span> {rec.details.quantity}
                          </p>
                          <p className="text-sm text-gray-600">
                            <span className="font-semibold">Timing:</span> {rec.details.timing}
                          </p>
                          <p className="text-sm text-gray-600 mt-2">
                            {rec.details.reason}
                          </p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Summary */}
                <div className="bg-blue-50 p-4 rounded-lg border-2 border-blue-300 mb-6">
                  <p className="text-blue-700">
                    <span className="font-semibold">Summary:</span> {result.summary}
                  </p>
                </div>

                {/* Voice Output */}
                <div className="flex gap-3">
                  <button
                    onClick={() => speakResult(result)}
                    disabled={isSpeaking}
                    className="flex-1 bg-blue-500 text-white font-semibold py-2 rounded-lg hover:bg-blue-600 disabled:opacity-50"
                  >
                    {isSpeaking ? '🔊 Speaking...' : '🔊 Speak Recommendation'}
                  </button>
                  {isSpeaking && (
                    <button
                      onClick={stopSpeaking}
                      className="flex-1 bg-red-500 text-white font-semibold py-2 rounded-lg hover:bg-red-600"
                    >
                      ⏹️ Stop
                    </button>
                  )}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Results - Image */}
        {result && activeTab === 'image' && result.success && (
          <div className="mt-8 space-y-6">
            <h2 className="text-2xl font-bold text-eco-green-dark">
              🖼️ Crop Analysis Results ({result.results.length} images)
            </h2>

            {result.results.map((item, idx) => (
              <div key={idx} className="bg-white rounded-lg shadow-lg p-8">
                <h3 className="text-xl font-bold text-eco-green-dark mb-6">
                  📸 Image {idx + 1}: {item.filename}
                </h3>

                {item.data.success ? (
                  <>
                    {/* Crop Identification */}
                    <div className="bg-green-50 p-6 rounded-lg border-2 border-green-300 mb-6">
                      <h4 className="text-lg font-bold text-green-700 mb-3">✅ Crop Identified</h4>
                      <p className="text-3xl font-bold text-eco-green mb-2">
                        {item.data.crop_identification.crop.toUpperCase()}
                      </p>
                      <p className="text-gray-700 mb-2">
                        <span className="font-semibold">Confidence:</span> {(item.data.crop_identification.confidence * 100).toFixed(0)}%
                      </p>
                      <p className="text-gray-700">
                        <span className="font-semibold">Analysis:</span> {item.data.crop_identification.reason}
                      </p>
                    </div>

                    {/* Default Nutrients */}
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                      <div className="bg-blue-50 p-4 rounded-lg border-2 border-blue-300">
                        <p className="text-gray-600 text-sm">Nitrogen</p>
                        <p className="text-2xl font-bold text-blue-600 mt-2">
                          {item.data.default_nutrients.nitrogen} mg/kg
                        </p>
                      </div>
                      <div className="bg-green-50 p-4 rounded-lg border-2 border-green-300">
                        <p className="text-gray-600 text-sm">Phosphorus</p>
                        <p className="text-2xl font-bold text-green-600 mt-2">
                          {item.data.default_nutrients.phosphorus} mg/kg
                        </p>
                      </div>
                      <div className="bg-yellow-50 p-4 rounded-lg border-2 border-yellow-300">
                        <p className="text-gray-600 text-sm">Potassium</p>
                        <p className="text-2xl font-bold text-yellow-600 mt-2">
                          {item.data.default_nutrients.potassium} mg/kg
                        </p>
                      </div>
                    </div>

                    {/* Fertilizer Recommendation */}
                    <div className="bg-eco-cream rounded-lg p-6 mb-6 border-2 border-eco-green">
                      <h4 className="text-lg font-bold text-eco-green-dark mb-4">
                        🎯 Recommended Fertilizer
                      </h4>
                      <div className="space-y-3">
                        <div>
                          <p className="text-sm text-gray-600">Fertilizer</p>
                          <p className="text-lg font-bold text-eco-green">
                            {item.data.fertilizer_recommendation.primary_recommendation.fertilizer}
                          </p>
                        </div>
                        <div>
                          <p className="text-sm text-gray-600">Quantity</p>
                          <p className="text-lg font-semibold text-gray-800">
                            {item.data.fertilizer_recommendation.primary_recommendation.quantity}
                          </p>
                        </div>
                        <div>
                          <p className="text-sm text-gray-600">Timing</p>
                          <p className="text-lg font-semibold text-gray-800">
                            {item.data.fertilizer_recommendation.primary_recommendation.timing}
                          </p>
                        </div>
                        <div>
                          <p className="text-sm text-gray-600">Benefits</p>
                          <p className="text-gray-700 mt-1">
                            {item.data.fertilizer_recommendation.primary_recommendation.benefits}
                          </p>
                        </div>
                      </div>
                    </div>

                    {/* Summary */}
                    <div className="bg-blue-50 p-4 rounded-lg border-2 border-blue-300">
                      <p className="text-blue-700">
                        <span className="font-semibold">Summary:</span> {item.data.summary}
                      </p>
                    </div>

                    {/* Note if using fallback */}
                    {item.data.note && (
                      <div className="bg-yellow-50 p-4 rounded-lg border-2 border-yellow-300 mt-4">
                        <p className="text-yellow-800 text-sm">
                          ⚠️ <span className="font-semibold">Note:</span> {item.data.note}
                        </p>
                      </div>
                    )}
                  </>
                ) : (
                  <div className="bg-red-50 border-2 border-red-300 rounded-lg p-6">
                    <p className="text-red-700 font-semibold">❌ Error</p>
                    <p className="text-red-600 mt-2">{item.data.error}</p>
                  </div>
                )}
              </div>
            ))}

            {/* Voice Output for First Image */}
            {result.results.length > 0 && result.results[0].data.success && (
              <div className="bg-white rounded-lg shadow-lg p-6">
                <div className="flex gap-3">
                  <button
                    onClick={() => speakResult(result.results[0].data.fertilizer_recommendation)}
                    disabled={isSpeaking}
                    className="flex-1 bg-blue-500 text-white font-semibold py-2 rounded-lg hover:bg-blue-600 disabled:opacity-50"
                  >
                    {isSpeaking ? '🔊 Speaking...' : '🔊 Speak First Result'}
                  </button>
                  {isSpeaking && (
                    <button
                      onClick={stopSpeaking}
                      className="flex-1 bg-red-500 text-white font-semibold py-2 rounded-lg hover:bg-red-600"
                    >
                      ⏹️ Stop
                    </button>
                  )}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Error Results */}
        {result && !result.success && (
          <div className="mt-8 bg-white rounded-lg shadow-lg p-8">
            <div className="bg-red-50 border-2 border-red-300 rounded-lg p-6">
              <p className="text-red-700 font-semibold">❌ Error</p>
              <p className="text-red-600 mt-2">{result.error}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default FertilizerRecommendation;

