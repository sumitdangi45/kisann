import { useState, useEffect, useRef } from 'react';

function CropRecommendationAdvanced() {
  const [formData, setFormData] = useState({
    nitrogen: '',
    phosphorus: '',
    potassium: '',
    temperature: '',
    humidity: '',
    ph: '',
    rainfall: '',
    month: ''
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [months, setMonths] = useState([]);
  const [activeTab, setActiveTab] = useState('manual');
  const [uploadedFile, setUploadedFile] = useState(null);
  const [cameraStream, setCameraStream] = useState(null);
  const [isCameraActive, setIsCameraActive] = useState(false);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  useEffect(() => {
    // Fetch months
    fetch('http://localhost:5000/api/months')
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          setMonths(data.months);
        }
      })
      .catch(err => console.error('Error fetching months:', err));
  }, []);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleFileUpload = (e, type) => {
    const file = e.target.files?.[0];
    if (file) {
      if (type === 'pdf' && !file.type.includes('pdf')) {
        alert('Please select a PDF file');
        return;
      }
      if (type === 'image' && !file.type.includes('image')) {
        alert('Please select an image file');
        return;
      }
      setUploadedFile({ file, type });
    }
  };

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        setCameraStream(stream);
        setIsCameraActive(true);
      }
    } catch (error) {
      console.error('Error accessing camera:', error);
      alert('Could not access camera. Please check permissions.');
    }
  };

  const stopCamera = () => {
    if (cameraStream) {
      cameraStream.getTracks().forEach(track => track.stop());
      setCameraStream(null);
      setIsCameraActive(false);
    }
  };

  const capturePhoto = () => {
    if (videoRef.current && canvasRef.current) {
      const context = canvasRef.current.getContext('2d');
      if (context) {
        context.drawImage(videoRef.current, 0, 0, canvasRef.current.width, canvasRef.current.height);
        canvasRef.current.toBlob((blob) => {
          if (blob) {
            const file = new File([blob], 'camera_capture.jpg', { type: 'image/jpeg' });
            setUploadedFile({ file, type: 'image' });
            stopCamera();
          }
        }, 'image/jpeg');
      }
    }
  };

  const handleFileSubmit = async (e) => {
    e.preventDefault();
    if (!uploadedFile) {
      alert('Please select a file');
      return;
    }

    setLoading(true);
    try {
      const formDataFile = new FormData();
      formDataFile.append('file', uploadedFile.file);
      const month = formData.month;
      if (month) {
        formDataFile.append('month', month);
      }

      const endpoint = uploadedFile.type === 'pdf' 
        ? 'http://localhost:5000/api/soil-report-predict'
        : 'http://localhost:5000/api/soil-image-predict';

      const response = await fetch(endpoint, {
        method: 'POST',
        body: formDataFile
      });
      const data = await response.json();
      setResult(data);
      
      if (data.crop) {
        speakResult(data);
      }
    } catch (error) {
      console.error('Error:', error);
      setResult({ error: 'Failed to process file' });
    }
    setLoading(false);
  };

  const handleManualSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await fetch('http://localhost:5000/api/crop-predict-partial', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      const data = await response.json();
      setResult(data);
      
      if (data.crop) {
        speakResult(data);
      }
    } catch (error) {
      console.error('Error:', error);
      setResult({ error: 'Failed to get prediction' });
    }
    setLoading(false);
  };

  const speakResult = (data) => {
    const text = `The recommended crop is ${data.crop}. ${data.explanation || ''}`;
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

  const isFormValid = formData.nitrogen || formData.phosphorus || formData.potassium || 
                      formData.temperature || formData.humidity || formData.ph || formData.rainfall;

  return (
    <div className="min-h-screen bg-eco-cream py-20">
      <div className="max-w-4xl mx-auto px-6">
        <h1 className="text-4xl font-bold text-eco-green-dark mb-2">🌾 Crop Recommendation</h1>
        <p className="text-gray-600 mb-8">Upload PDF/Image, use camera, or enter data manually</p>
        
        {/* Tab Navigation */}
        <div className="flex gap-2 mb-8 border-b-2 border-gray-200 overflow-x-auto">
          <button
            onClick={() => setActiveTab('manual')}
            className={`px-6 py-3 font-semibold transition-colors whitespace-nowrap ${
              activeTab === 'manual'
                ? 'text-eco-green border-b-4 border-eco-green'
                : 'text-gray-600 hover:text-eco-green'
            }`}
          >
            📝 Manual
          </button>
          <button
            onClick={() => setActiveTab('pdf')}
            className={`px-6 py-3 font-semibold transition-colors whitespace-nowrap ${
              activeTab === 'pdf'
                ? 'text-eco-green border-b-4 border-eco-green'
                : 'text-gray-600 hover:text-eco-green'
            }`}
          >
            📄 PDF Report
          </button>
          <button
            onClick={() => setActiveTab('image')}
            className={`px-6 py-3 font-semibold transition-colors whitespace-nowrap ${
              activeTab === 'image'
                ? 'text-eco-green border-b-4 border-eco-green'
                : 'text-gray-600 hover:text-eco-green'
            }`}
          >
            🖼️ Image
          </button>
          <button
            onClick={() => setActiveTab('camera')}
            className={`px-6 py-3 font-semibold transition-colors whitespace-nowrap ${
              activeTab === 'camera'
                ? 'text-eco-green border-b-4 border-eco-green'
                : 'text-gray-600 hover:text-eco-green'
            }`}
          >
            📷 Camera
          </button>
        </div>

        <div className="bg-white rounded-lg shadow-lg p-8">
          {/* Manual Input Tab */}
          {activeTab === 'manual' && (
            <form onSubmit={handleManualSubmit} className="space-y-6">
              <p className="text-sm text-gray-600 mb-4">Enter as many parameters as you have. Minimum 1 required.</p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {[
                  { name: 'nitrogen', label: 'Nitrogen (N) mg/kg' },
                  { name: 'phosphorus', label: 'Phosphorus (P) mg/kg' },
                  { name: 'potassium', label: 'Potassium (K) mg/kg' },
                  { name: 'temperature', label: 'Temperature (°C)' },
                  { name: 'humidity', label: 'Humidity (%)' },
                  { name: 'ph', label: 'pH', step: '0.1' },
                  { name: 'rainfall', label: 'Rainfall (mm)' }
                ].map(field => (
                  <div key={field.name}>
                    <label className="block text-sm font-medium text-gray-700 mb-2">{field.label}</label>
                    <input
                      type="number"
                      name={field.name}
                      value={formData[field.name as keyof typeof formData]}
                      onChange={handleChange}
                      step={field.step || '1'}
                      placeholder="Optional"
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-eco-green"
                    />
                  </div>
                ))}
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Month (Optional)</label>
                <select
                  name="month"
                  value={formData.month}
                  onChange={handleChange}
                  className="w-full px-4 py-3 border-2 border-blue-300 rounded-lg focus:ring-2 focus:ring-eco-green"
                >
                  <option value="">Select month...</option>
                  {months.map(month => (
                    <option key={month} value={month}>{month}</option>
                  ))}
                </select>
              </div>
              <button
                type="submit"
                disabled={loading || !isFormValid}
                className="w-full bg-eco-green text-white font-semibold py-3 rounded-lg hover:bg-eco-green-dark transition-colors disabled:opacity-50"
              >
                {loading ? '⏳ Predicting...' : '🌾 Get Recommendation'}
              </button>
            </form>
          )}

          {/* PDF Upload Tab */}
          {activeTab === 'pdf' && (
            <form onSubmit={handleFileSubmit} className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Upload Soil Report PDF</label>
                <div className="border-2 border-dashed border-eco-green rounded-lg p-8 text-center cursor-pointer hover:bg-eco-cream transition-colors">
                  <input
                    type="file"
                    accept=".pdf"
                    onChange={(e) => handleFileUpload(e, 'pdf')}
                    className="hidden"
                    id="pdf-input"
                  />
                  <label htmlFor="pdf-input" className="cursor-pointer">
                    <div className="text-4xl mb-2">📄</div>
                    <p className="text-gray-700 font-semibold">
                      {uploadedFile?.type === 'pdf' ? uploadedFile.file.name : 'Click to upload PDF'}
                    </p>
                    <p className="text-gray-500 text-sm mt-1">Only PDF files supported</p>
                  </label>
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Month (Optional)</label>
                <select
                  value={formData.month}
                  onChange={handleChange}
                  className="w-full px-4 py-3 border-2 border-blue-300 rounded-lg focus:ring-2 focus:ring-eco-green"
                >
                  <option value="">Select month...</option>
                  {months.map(month => (
                    <option key={month} value={month}>{month}</option>
                  ))}
                </select>
              </div>
              <button
                type="submit"
                disabled={loading || !uploadedFile || uploadedFile.type !== 'pdf'}
                className="w-full bg-eco-green text-white font-semibold py-3 rounded-lg hover:bg-eco-green-dark transition-colors disabled:opacity-50"
              >
                {loading ? '⏳ Processing...' : '📄 Analyze PDF'}
              </button>
            </form>
          )}

          {/* Image Upload Tab */}
          {activeTab === 'image' && (
            <form onSubmit={handleFileSubmit} className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Upload Soil Report Image</label>
                <div className="border-2 border-dashed border-eco-green rounded-lg p-8 text-center cursor-pointer hover:bg-eco-cream transition-colors">
                  <input
                    type="file"
                    accept="image/*"
                    onChange={(e) => handleFileUpload(e, 'image')}
                    className="hidden"
                    id="image-input"
                  />
                  <label htmlFor="image-input" className="cursor-pointer">
                    <div className="text-4xl mb-2">🖼️</div>
                    <p className="text-gray-700 font-semibold">
                      {uploadedFile?.type === 'image' ? uploadedFile.file.name : 'Click to upload image'}
                    </p>
                    <p className="text-gray-500 text-sm mt-1">JPG, PNG, GIF, BMP supported</p>
                  </label>
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Month (Optional)</label>
                <select
                  value={formData.month}
                  onChange={handleChange}
                  className="w-full px-4 py-3 border-2 border-blue-300 rounded-lg focus:ring-2 focus:ring-eco-green"
                >
                  <option value="">Select month...</option>
                  {months.map(month => (
                    <option key={month} value={month}>{month}</option>
                  ))}
                </select>
              </div>
              <button
                type="submit"
                disabled={loading || !uploadedFile || uploadedFile.type !== 'image'}
                className="w-full bg-eco-green text-white font-semibold py-3 rounded-lg hover:bg-eco-green-dark transition-colors disabled:opacity-50"
              >
                {loading ? '⏳ Processing...' : '🖼️ Analyze Image'}
              </button>
            </form>
          )}

          {/* Camera Tab */}
          {activeTab === 'camera' && (
            <div className="space-y-6">
              {!isCameraActive ? (
                <button
                  onClick={startCamera}
                  className="w-full bg-blue-500 text-white font-semibold py-3 rounded-lg hover:bg-blue-600 transition-colors"
                >
                  📷 Start Camera
                </button>
              ) : (
                <>
                  <video
                    ref={videoRef}
                    autoPlay
                    playsInline
                    className="w-full rounded-lg border-2 border-eco-green"
                  />
                  <canvas
                    ref={canvasRef}
                    width={640}
                    height={480}
                    className="hidden"
                  />
                  <div className="flex gap-3">
                    <button
                      onClick={capturePhoto}
                      className="flex-1 bg-green-500 text-white font-semibold py-3 rounded-lg hover:bg-green-600 transition-colors"
                    >
                      📸 Capture Photo
                    </button>
                    <button
                      onClick={stopCamera}
                      className="flex-1 bg-red-500 text-white font-semibold py-3 rounded-lg hover:bg-red-600 transition-colors"
                    >
                      ❌ Stop Camera
                    </button>
                  </div>
                </>
              )}
              
              {uploadedFile?.type === 'image' && (
                <form onSubmit={handleFileSubmit} className="space-y-4">
                  <div className="bg-green-50 p-4 rounded-lg">
                    <p className="text-green-700 font-semibold">✅ Photo captured: {uploadedFile.file.name}</p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Month (Optional)</label>
                    <select
                      value={formData.month}
                      onChange={handleChange}
                      className="w-full px-4 py-3 border-2 border-blue-300 rounded-lg focus:ring-2 focus:ring-eco-green"
                    >
                      <option value="">Select month...</option>
                      {months.map(month => (
                        <option key={month} value={month}>{month}</option>
                      ))}
                    </select>
                  </div>
                  <button
                    type="submit"
                    disabled={loading}
                    className="w-full bg-eco-green text-white font-semibold py-3 rounded-lg hover:bg-eco-green-dark transition-colors disabled:opacity-50"
                  >
                    {loading ? '⏳ Processing...' : '📷 Analyze Photo'}
                  </button>
                </form>
              )}
            </div>
          )}
        </div>

        {/* Results */}
        {result && (
          <div className="mt-8 bg-white rounded-lg shadow-lg p-8">
            {result.error ? (
              <div className="bg-red-50 border-2 border-red-300 rounded-lg p-6">
                <p className="text-red-700 font-semibold mb-2">❌ Error</p>
                <p className="text-red-600">{result.error}</p>
                {result.available_count && (
                  <p className="text-red-600 text-sm mt-2">Found {result.available_count} parameters. Need at least 4.</p>
                )}
              </div>
            ) : (
              <div>
                <h2 className="text-2xl font-bold text-eco-green-dark mb-4">Recommended Crop</h2>
                <p className="text-4xl font-bold text-eco-green mb-6">🌾 {result.crop.toUpperCase()}</p>
                
                {result.parameters_count && (
                  <div className="bg-blue-50 p-4 rounded-lg mb-6">
                    <p className="text-blue-700">📊 Extracted {result.parameters_count} parameters from your report</p>
                  </div>
                )}
                
                {result.month_info && (
                  <div className={`rounded-lg p-6 mb-6 ${result.month_info.suitable ? 'bg-green-50 border-2 border-green-300' : 'bg-yellow-50 border-2 border-yellow-300'}`}>
                    <h3 className="text-lg font-bold mb-3">
                      {result.month_info.suitable ? '✅ Seasonal Match' : '⚠️ Seasonal Adjustment'}
                    </h3>
                    <p className="text-gray-700 mb-3">{result.month_info.reason}</p>
                  </div>
                )}
                
                {result.explanation && (
                  <div className="bg-eco-cream rounded-lg p-6 mb-6">
                    <h3 className="text-lg font-bold text-eco-green-dark mb-3">Why This Crop?</h3>
                    <div className="text-gray-700 whitespace-pre-wrap text-sm leading-relaxed">
                      {result.explanation}
                    </div>
                  </div>
                )}

                {/* Voice Output */}
                <div className="flex gap-3">
                  <button
                    onClick={() => speakResult(result)}
                    disabled={isSpeaking}
                    className="flex-1 bg-blue-500 text-white font-semibold py-2 rounded-lg hover:bg-blue-600 disabled:opacity-50"
                  >
                    {isSpeaking ? '🔊 Speaking...' : '🔊 Speak Result'}
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
      </div>
    </div>
  );
}

export default CropRecommendationAdvanced;
