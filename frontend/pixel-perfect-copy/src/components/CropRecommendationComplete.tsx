import { useState, useEffect } from 'react';

function CropRecommendationComplete() {
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
  const [voiceMode, setVoiceMode] = useState(false);
  const [months, setMonths] = useState([]);
  const [activeTab, setActiveTab] = useState('manual');
  const [transcript, setTranscript] = useState('');
  const [listening, setListening] = useState(false);
  const [browserSupportsSpeechRecognition, setBrowserSupportsSpeechRecognition] = useState(true);
  const [recognition, setRecognition] = useState(null);
  const [pdfFile, setPdfFile] = useState(null);
  const [pdfMonth, setPdfMonth] = useState('');

  useEffect(() => {
    // Initialize speech recognition
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      const recognitionInstance = new SpeechRecognition();
      recognitionInstance.continuous = false;
      recognitionInstance.interimResults = true;
      recognitionInstance.lang = 'en-US';

      recognitionInstance.onstart = () => setListening(true);
      recognitionInstance.onend = () => setListening(false);
      recognitionInstance.onresult = (event) => {
        let interimTranscript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
          const transcript = event.results[i][0].transcript;
          if (event.results[i].isFinal) {
            setTranscript(prev => prev + transcript + ' ');
          } else {
            interimTranscript += transcript;
          }
        }
      };

      setRecognition(recognitionInstance);
    } else {
      setBrowserSupportsSpeechRecognition(false);
    }

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

  const handleVoiceInput = () => {
    if (!voiceMode) {
      setVoiceMode(true);
      setTranscript('');
      if (recognition) {
        recognition.start();
      }
    }
  };

  const resetTranscript = () => {
    setTranscript('');
  };

  const parseVoiceInput = () => {
    const words = transcript.toLowerCase().split(/\s+/);
    const newData = { ...formData };

    for (let i = 0; i < words.length - 1; i++) {
      const key = words[i];
      const value = words[i + 1];

      if (key === 'nitrogen' && !isNaN(value)) newData.nitrogen = value;
      else if (key === 'phosphorus' && !isNaN(value)) newData.phosphorus = value;
      else if (key === 'potassium' && !isNaN(value)) newData.potassium = value;
      else if (key === 'temperature' && !isNaN(value)) newData.temperature = value;
      else if (key === 'humidity' && !isNaN(value)) newData.humidity = value;
      else if (key === 'ph' && !isNaN(value)) newData.ph = value;
      else if (key === 'rainfall' && !isNaN(value)) newData.rainfall = value;
    }

    setFormData(newData);
    setVoiceMode(false);
    if (recognition) {
      recognition.stop();
    }
    resetTranscript();
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

  const handlePdfUpload = (e) => {
    const file = e.target.files?.[0];
    if (file && file.type === 'application/pdf') {
      setPdfFile(file);
    } else {
      alert('Please select a valid PDF file');
    }
  };

  const handlePdfSubmit = async (e) => {
    e.preventDefault();
    if (!pdfFile) {
      alert('Please select a PDF file');
      return;
    }

    setLoading(true);
    try {
      const formDataPdf = new FormData();
      formDataPdf.append('file', pdfFile);
      if (pdfMonth) {
        formDataPdf.append('month', pdfMonth);
      }

      const response = await fetch('http://localhost:5000/api/soil-report-predict', {
        method: 'POST',
        body: formDataPdf
      });
      const data = await response.json();
      setResult(data);
      
      if (data.crop) {
        speakResult(data);
      }
    } catch (error) {
      console.error('Error:', error);
      setResult({ error: 'Failed to process PDF' });
    }
    setLoading(false);
  };

  const isFormValid = formData.nitrogen && formData.phosphorus && formData.potassium && 
                      formData.temperature && formData.humidity && formData.ph && formData.rainfall;

  return (
    <div className="min-h-screen bg-eco-cream py-20">
      <div className="max-w-4xl mx-auto px-6">
        <h1 className="text-4xl font-bold text-eco-green-dark mb-2">🌾 Crop Recommendation</h1>
        <p className="text-gray-600 mb-8">Get personalized crop recommendations using AI, voice, or seasonal data</p>
        
        <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-lg p-8">
          {/* Tab Navigation */}
          <div className="flex gap-2 mb-8 border-b-2 border-gray-200 overflow-x-auto">
            <button
              type="button"
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
              type="button"
              onClick={() => setActiveTab('voice')}
              className={`px-6 py-3 font-semibold transition-colors whitespace-nowrap ${
                activeTab === 'voice'
                  ? 'text-eco-green border-b-4 border-eco-green'
                  : 'text-gray-600 hover:text-eco-green'
              }`}
              disabled={!browserSupportsSpeechRecognition}
            >
              🎤 Voice
            </button>
            <button
              type="button"
              onClick={() => setActiveTab('month')}
              className={`px-6 py-3 font-semibold transition-colors whitespace-nowrap ${
                activeTab === 'month'
                  ? 'text-eco-green border-b-4 border-eco-green'
                  : 'text-gray-600 hover:text-eco-green'
              }`}
            >
              📅 Seasonal
            </button>
            <button
              type="button"
              onClick={() => setActiveTab('pdf')}
              className={`px-6 py-3 font-semibold transition-colors whitespace-nowrap ${
                activeTab === 'pdf'
                  ? 'text-eco-green border-b-4 border-eco-green'
                  : 'text-gray-600 hover:text-eco-green'
              }`}
            >
              📄 Soil Report
            </button>
          </div>

          {/* Manual Input Tab */}
          {activeTab === 'manual' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {[
                  { name: 'nitrogen', label: 'Nitrogen (N)' },
                  { name: 'phosphorus', label: 'Phosphorus (P)' },
                  { name: 'potassium', label: 'Potassium (K)' },
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
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-eco-green"
                      required
                    />
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Voice Input Tab */}
          {activeTab === 'voice' && (
            <div className="space-y-6">
              {voiceMode ? (
                <div>
                  <div className={`p-4 rounded-lg mb-4 ${listening ? 'bg-red-100 border-2 border-red-500' : 'bg-gray-100'}`}>
                    <p className="text-sm font-semibold mb-2">
                      {listening ? '🔴 Listening...' : '⏹️ Ready to listen'}
                    </p>
                    <p className="text-gray-700 min-h-12 p-2 bg-white rounded">
                      {transcript || 'Say: nitrogen 90 phosphorus 42 potassium 43 temperature 20 humidity 82 ph 6.5 rainfall 202'}
                    </p>
                  </div>
                  <div className="flex gap-3">
                    <button
                      type="button"
                      onClick={parseVoiceInput}
                      className="flex-1 bg-green-500 text-white font-semibold py-2 rounded-lg hover:bg-green-600"
                    >
                      ✓ Use This Input
                    </button>
                    <button
                      type="button"
                      onClick={() => setVoiceMode(false)}
                      className="flex-1 bg-gray-500 text-white font-semibold py-2 rounded-lg hover:bg-gray-600"
                    >
                      ✕ Cancel
                    </button>
                  </div>
                </div>
              ) : (
                <button
                  type="button"
                  onClick={handleVoiceInput}
                  className="w-full bg-blue-500 text-white font-semibold py-3 rounded-lg hover:bg-blue-600"
                >
                  🎤 Enable Voice Input
                </button>
              )}
            </div>
          )}

          {/* Seasonal Tab */}
          {activeTab === 'month' && (
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Select Month</label>
                <select
                  name="month"
                  value={formData.month}
                  onChange={handleChange}
                  className="w-full px-4 py-3 border-2 border-blue-300 rounded-lg focus:ring-2 focus:ring-eco-green text-lg"
                  required
                >
                  <option value="">Choose a month...</option>
                  {months.map(month => (
                    <option key={month} value={month}>{month}</option>
                  ))}
                </select>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {[
                  { name: 'nitrogen', label: 'Nitrogen (N)' },
                  { name: 'phosphorus', label: 'Phosphorus (P)' },
                  { name: 'potassium', label: 'Potassium (K)' },
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
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-eco-green"
                      required
                    />
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* PDF Upload Tab */}
          {activeTab === 'pdf' && (
            <form onSubmit={handlePdfSubmit} className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Upload Soil Report PDF</label>
                <div className="border-2 border-dashed border-eco-green rounded-lg p-8 text-center cursor-pointer hover:bg-eco-cream transition-colors">
                  <input
                    type="file"
                    accept=".pdf"
                    onChange={handlePdfUpload}
                    className="hidden"
                    id="pdf-input"
                  />
                  <label htmlFor="pdf-input" className="cursor-pointer">
                    <div className="text-4xl mb-2">📄</div>
                    <p className="text-gray-700 font-semibold">
                      {pdfFile ? pdfFile.name : 'Click to upload or drag PDF here'}
                    </p>
                    <p className="text-gray-500 text-sm mt-1">Only PDF files are supported</p>
                  </label>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Select Month (Optional)</label>
                <select
                  value={pdfMonth}
                  onChange={(e) => setPdfMonth(e.target.value)}
                  className="w-full px-4 py-3 border-2 border-blue-300 rounded-lg focus:ring-2 focus:ring-eco-green text-lg"
                >
                  <option value="">No specific month</option>
                  {months.map(month => (
                    <option key={month} value={month}>{month}</option>
                  ))}
                </select>
              </div>

              <button
                type="submit"
                disabled={loading || !pdfFile}
                className="w-full bg-eco-green text-white font-semibold py-3 rounded-lg hover:bg-eco-green-dark transition-colors disabled:opacity-50"
              >
                {loading ? '⏳ Processing PDF...' : '📄 Analyze Soil Report'}
              </button>
            </form>
          )}

          {/* Submit Button for other tabs */}
          {activeTab !== 'pdf' && (
            <button
              type="submit"
              disabled={loading || !isFormValid}
              className="w-full mt-8 bg-eco-green text-white font-semibold py-3 rounded-lg hover:bg-eco-green-dark transition-colors disabled:opacity-50"
            >
              {loading ? '⏳ Predicting...' : '🌾 Get Recommendation'}
            </button>
          )}
        </form>

        {/* Results */}
        {result && (
          <div className="mt-8 bg-white rounded-lg shadow-lg p-8">
            {result.error ? (
              <p className="text-red-600 text-lg">{result.error}</p>
            ) : (
              <div>
                <h2 className="text-2xl font-bold text-eco-green-dark mb-4">Recommended Crop</h2>
                <p className="text-4xl font-bold text-eco-green mb-6">🌾 {result.crop.toUpperCase()}</p>
                
                {/* Month Info */}
                {result.month_info && (
                  <div className={`rounded-lg p-6 mb-6 ${result.month_info.suitable ? 'bg-green-50 border-2 border-green-300' : 'bg-yellow-50 border-2 border-yellow-300'}`}>
                    <h3 className="text-lg font-bold mb-3">
                      {result.month_info.suitable ? '✅ Seasonal Match' : '⚠️ Seasonal Adjustment'}
                    </h3>
                    <p className="text-gray-700 mb-3">{result.month_info.reason}</p>
                    {result.month_info.season && (
                      <p className="text-sm text-gray-600">Season: <span className="font-bold text-eco-green">{result.month_info.season}</span></p>
                    )}
                  </div>
                )}
                
                {/* Explanation */}
                {result.explanation && (
                  <div className="bg-eco-cream rounded-lg p-6 mb-6">
                    <h3 className="text-lg font-bold text-eco-green-dark mb-3">Why This Crop?</h3>
                    <div className="text-gray-700 whitespace-pre-wrap text-sm leading-relaxed">
                      {result.explanation}
                    </div>
                  </div>
                )}
                
                {/* Weather Info */}
                <div className="grid grid-cols-2 gap-4 text-sm mb-6">
                  <div className="bg-blue-50 p-4 rounded">
                    <p className="text-gray-600">Temperature</p>
                    <p className="text-lg font-bold text-blue-600">{result.temperature}°C</p>
                  </div>
                  <div className="bg-green-50 p-4 rounded">
                    <p className="text-gray-600">Humidity</p>
                    <p className="text-lg font-bold text-green-600">{result.humidity}%</p>
                  </div>
                </div>

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

export default CropRecommendationComplete;
