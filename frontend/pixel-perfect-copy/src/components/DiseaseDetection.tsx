import { useState } from 'react';

function DiseaseDetection() {
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);

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

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (uploadedFiles.length === 0) {
      alert('Please select at least one image');
      return;
    }

    setLoading(true);
    try {
      const formData = new FormData();
      uploadedFiles.forEach(file => {
        formData.append('files', file);
      });

      const response = await fetch('http://localhost:5000/api/disease-predict', {
        method: 'POST',
        body: formData
      });
      const data = await response.json();
      setResult(data);
      
      if (data.success) {
        speakResult(data);
      }
    } catch (error) {
      console.error('Error:', error);
      setResult({ success: false, error: 'Failed to analyze images' });
    }
    setLoading(false);
  };

  const speakResult = (data) => {
    const text = `Analyzed ${data.total_images} images. Most common disease detected: ${data.most_common_disease}. ${data.disease_info}`;
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

  const getDiseaseColor = (disease) => {
    if (disease.includes('healthy')) return 'bg-green-50 border-green-300';
    if (disease.includes('blight')) return 'bg-red-50 border-red-300';
    if (disease.includes('rust')) return 'bg-orange-50 border-orange-300';
    if (disease.includes('spot')) return 'bg-yellow-50 border-yellow-300';
    return 'bg-gray-50 border-gray-300';
  };

  const getDiseaseIcon = (disease) => {
    if (disease.includes('healthy')) return '✅';
    if (disease.includes('blight')) return '🔴';
    if (disease.includes('rust')) return '🟠';
    if (disease.includes('spot')) return '🟡';
    return '⚠️';
  };

  return (
    <div className="min-h-screen bg-eco-cream py-20">
      <div className="max-w-4xl mx-auto px-6">
        <h1 className="text-4xl font-bold text-eco-green-dark mb-2">🔍 Disease Detection</h1>
        <p className="text-gray-600 mb-8">Upload multiple plant leaf images for accurate disease detection and analysis</p>
        
        <div className="bg-white rounded-lg shadow-lg p-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* File Upload */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Upload Plant Leaf Images</label>
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
                    Click to upload plant leaf images
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

            {/* Info Box */}
            <div className="bg-blue-50 p-4 rounded-lg border-2 border-blue-300">
              <p className="text-blue-700 text-sm">
                <span className="font-semibold">💡 Tip:</span> Upload multiple images of the same plant or different plants for better disease detection accuracy. The system will analyze each image and identify the most common disease.
              </p>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading || uploadedFiles.length === 0}
              className="w-full bg-eco-green text-white font-semibold py-3 rounded-lg hover:bg-eco-green-dark transition-colors disabled:opacity-50"
            >
              {loading ? '⏳ Analyzing Images...' : `🔍 Detect Disease (${uploadedFiles.length})`}
            </button>
          </form>
        </div>

        {/* Results */}
        {result && (
          <div className="mt-8 bg-white rounded-lg shadow-lg p-8">
            {!result.success ? (
              <div className="bg-red-50 border-2 border-red-300 rounded-lg p-6">
                <p className="text-red-700 font-semibold">❌ Error</p>
                <p className="text-red-600 mt-2">{result.error}</p>
              </div>
            ) : (
              <div>
                <h2 className="text-2xl font-bold text-eco-green-dark mb-6">
                  🔍 Disease Detection Results
                </h2>

                {/* Summary */}
                <div className="bg-blue-50 p-6 rounded-lg border-2 border-blue-300 mb-6">
                  <p className="text-blue-700 text-lg">
                    <span className="font-semibold">📊 Summary:</span> {result.summary}
                  </p>
                </div>

                {/* Most Common Disease */}
                <div className={`p-6 rounded-lg border-2 mb-6 ${getDiseaseColor(result.most_common_disease)}`}>
                  <h3 className="text-lg font-bold text-gray-800 mb-3">
                    {getDiseaseIcon(result.most_common_disease)} Most Common Disease
                  </h3>
                  <p className="text-2xl font-bold text-eco-green mb-3">
                    {result.most_common_disease.replace(/_/g, ' ')}
                  </p>
                  <p className="text-gray-700">
                    <span className="font-semibold">Info:</span> {result.disease_info}
                  </p>
                </div>

                {/* Individual Results */}
                <div className="mb-6">
                  <h3 className="text-lg font-bold text-gray-800 mb-4">
                    📋 Individual Image Analysis
                  </h3>
                  <div className="space-y-3">
                    {result.predictions.map((pred, idx) => (
                      <div key={idx} className={`p-4 rounded-lg border-2 ${getDiseaseColor(pred.disease)}`}>
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <p className="font-semibold text-gray-800">
                              {getDiseaseIcon(pred.disease)} {pred.filename}
                            </p>
                            {pred.success ? (
                              <>
                                <p className="text-gray-700 mt-1">
                                  <span className="font-semibold">Disease:</span> {pred.disease.replace(/_/g, ' ')}
                                </p>
                                <p className="text-gray-600 text-sm mt-1">
                                  {pred.info}
                                </p>
                              </>
                            ) : (
                              <p className="text-red-600 mt-1">Error: {pred.error}</p>
                            )}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Statistics */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                  <div className="bg-green-50 p-4 rounded-lg border-2 border-green-300">
                    <p className="text-gray-600 text-sm">Total Images</p>
                    <p className="text-3xl font-bold text-green-600 mt-2">
                      {result.total_images}
                    </p>
                  </div>
                  <div className="bg-blue-50 p-4 rounded-lg border-2 border-blue-300">
                    <p className="text-gray-600 text-sm">Successful Analysis</p>
                    <p className="text-3xl font-bold text-blue-600 mt-2">
                      {result.predictions.filter(p => p.success).length}
                    </p>
                  </div>
                  <div className="bg-orange-50 p-4 rounded-lg border-2 border-orange-300">
                    <p className="text-gray-600 text-sm">Failed Analysis</p>
                    <p className="text-3xl font-bold text-orange-600 mt-2">
                      {result.predictions.filter(p => !p.success).length}
                    </p>
                  </div>
                </div>

                {/* Voice Output */}
                <div className="flex gap-3">
                  <button
                    onClick={() => speakResult(result)}
                    disabled={isSpeaking}
                    className="flex-1 bg-blue-500 text-white font-semibold py-2 rounded-lg hover:bg-blue-600 disabled:opacity-50"
                  >
                    {isSpeaking ? '🔊 Speaking...' : '🔊 Speak Results'}
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

export default DiseaseDetection;
