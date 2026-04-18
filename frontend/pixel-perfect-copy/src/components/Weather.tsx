import React, { useState } from 'react';
import { Cloud, CloudRain, Droplets, Wind, AlertCircle, Leaf } from 'lucide-react';

interface Alert {
  type: string;
  severity: 'low' | 'medium' | 'high';
  title: string;
  message: string;
  recommendations: string[];
  affected_crops: string[];
  action_required: boolean;
}

interface CropAlert {
  type: string;
  crop: string;
  issue: string;
  severity: 'low' | 'medium' | 'high';
  action: string;
}

interface WeatherData {
  temperature: number;
  humidity: number;
  rainfall: number;
  wind_speed: number;
  conditions: string;
  alerts_count: number;
  recommendation: string;
}

const Weather: React.FC = () => {
  const [city, setCity] = useState('Delhi');
  const [weatherData, setWeatherData] = useState<WeatherData | null>(null);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [selectedCrop, setSelectedCrop] = useState('rice');
  const [cropAlerts, setCropAlerts] = useState<CropAlert[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showCropAlerts, setShowCropAlerts] = useState(false);

  const crops = ['rice', 'wheat', 'maize', 'cotton', 'potato', 'tomato'];

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'high':
        return 'bg-red-100 border-red-300 text-red-800';
      case 'medium':
        return 'bg-yellow-100 border-yellow-300 text-yellow-800';
      case 'low':
        return 'bg-blue-100 border-blue-300 text-blue-800';
      default:
        return 'bg-gray-100 border-gray-300 text-gray-800';
    }
  };

  const getSeverityBadge = (severity: string) => {
    switch (severity) {
      case 'high':
        return 'bg-red-500 text-white';
      case 'medium':
        return 'bg-yellow-500 text-white';
      case 'low':
        return 'bg-blue-500 text-white';
      default:
        return 'bg-gray-500 text-white';
    }
  };

  const fetchWeather = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await fetch('http://localhost:5000/api/weather', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          city: city,
          rainfall: 50,
          wind_speed: 20,
        }),
      });

      const data = await response.json();

      if (data.success) {
        setWeatherData(data.weather);
        setAlerts(data.alerts);
        setShowCropAlerts(false);
      } else {
        setError(data.error || 'Failed to fetch weather data');
      }
    } catch (err) {
      setError('Error connecting to server');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const fetchCropAlerts = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await fetch(
        `http://localhost:5000/api/weather-alerts/${selectedCrop}`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            city: city,
            rainfall: 50,
            wind_speed: 20,
          }),
        }
      );

      const data = await response.json();

      if (data.success) {
        setCropAlerts(data.crop_specific_alerts);
        setShowCropAlerts(true);
      } else {
        setError(data.error || 'Failed to fetch crop alerts');
      }
    } catch (err) {
      setError('Error connecting to server');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const speakText = (text: string) => {
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = 'en-IN';
      window.speechSynthesis.speak(utterance);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-green-50 p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">🌤️ Weather & Alerts</h1>
          <p className="text-gray-600">Get real-time weather alerts for your farming</p>
        </div>

        {/* Location Input */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="flex gap-4 flex-wrap">
            <div className="flex-1 min-w-[250px]">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Enter City Name
              </label>
              <input
                type="text"
                value={city}
                onChange={(e) => setCity(e.target.value)}
                placeholder="e.g., Delhi, Mumbai, Bangalore"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
              />
            </div>
            <div className="flex items-end gap-2">
              <button
                onClick={fetchWeather}
                disabled={loading}
                className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:bg-gray-400 transition"
              >
                {loading ? 'Loading...' : 'Get Weather'}
              </button>
            </div>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg mb-6">
            {error}
          </div>
        )}

        {/* Weather Data Display */}
        {weatherData && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
            {/* Temperature */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center justify-between mb-2">
                <span className="text-gray-600 text-sm font-medium">Temperature</span>
                <Cloud className="w-5 h-5 text-blue-500" />
              </div>
              <p className="text-3xl font-bold text-gray-800">
                {weatherData.temperature}°C
              </p>
              <p className="text-xs text-gray-500 mt-2">{weatherData.conditions}</p>
            </div>

            {/* Humidity */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center justify-between mb-2">
                <span className="text-gray-600 text-sm font-medium">Humidity</span>
                <Droplets className="w-5 h-5 text-blue-400" />
              </div>
              <p className="text-3xl font-bold text-gray-800">{weatherData.humidity}%</p>
              <p className="text-xs text-gray-500 mt-2">
                {weatherData.humidity > 80
                  ? 'High - Disease Risk'
                  : weatherData.humidity < 30
                  ? 'Low - Pest Risk'
                  : 'Normal'}
              </p>
            </div>

            {/* Rainfall */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center justify-between mb-2">
                <span className="text-gray-600 text-sm font-medium">Rainfall</span>
                <CloudRain className="w-5 h-5 text-blue-600" />
              </div>
              <p className="text-3xl font-bold text-gray-800">{weatherData.rainfall}mm</p>
              <p className="text-xs text-gray-500 mt-2">
                {weatherData.rainfall > 50
                  ? 'Heavy Rain'
                  : weatherData.rainfall > 20
                  ? 'Moderate'
                  : 'Light'}
              </p>
            </div>

            {/* Wind Speed */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center justify-between mb-2">
                <span className="text-gray-600 text-sm font-medium">Wind Speed</span>
                <Wind className="w-5 h-5 text-gray-500" />
              </div>
              <p className="text-3xl font-bold text-gray-800">
                {weatherData.wind_speed} km/h
              </p>
              <p className="text-xs text-gray-500 mt-2">
                {weatherData.wind_speed > 40 ? 'Strong' : 'Moderate'}
              </p>
            </div>
          </div>
        )}

        {/* General Recommendation */}
        {weatherData && (
          <div className="bg-green-50 border border-green-200 rounded-lg p-6 mb-6">
            <div className="flex items-start gap-3">
              <Leaf className="w-6 h-6 text-green-600 flex-shrink-0 mt-1" />
              <div className="flex-1">
                <h3 className="font-semibold text-green-800 mb-2">Farming Recommendation</h3>
                <p className="text-green-700">{weatherData.recommendation}</p>
                <button
                  onClick={() => speakText(weatherData.recommendation)}
                  className="mt-3 px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 text-sm transition"
                >
                  🔊 Speak
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Alerts Section */}
        {alerts.length > 0 && (
          <div className="mb-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2">
              <AlertCircle className="w-6 h-6 text-red-500" />
              Weather Alerts ({alerts.length})
            </h2>
            <div className="grid grid-cols-1 gap-4">
              {alerts.map((alert, index) => (
                <div
                  key={index}
                  className={`border-l-4 rounded-lg p-4 ${getSeverityColor(alert.severity)}`}
                >
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="font-bold text-lg">{alert.title}</h3>
                    <span
                      className={`px-3 py-1 rounded-full text-xs font-semibold ${getSeverityBadge(
                        alert.severity
                      )}`}
                    >
                      {alert.severity.toUpperCase()}
                    </span>
                  </div>
                  <p className="mb-3">{alert.message}</p>

                  <div className="mb-3">
                    <p className="font-semibold text-sm mb-2">Recommendations:</p>
                    <ul className="list-disc list-inside space-y-1">
                      {alert.recommendations.map((rec, i) => (
                        <li key={i} className="text-sm">
                          {rec}
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div className="mb-3">
                    <p className="font-semibold text-sm mb-2">Affected Crops:</p>
                    <div className="flex flex-wrap gap-2">
                      {alert.affected_crops.map((crop, i) => (
                        <span
                          key={i}
                          className="px-3 py-1 bg-white bg-opacity-50 rounded-full text-xs font-medium"
                        >
                          {crop}
                        </span>
                      ))}
                    </div>
                  </div>

                  {alert.action_required && (
                    <div className="bg-white bg-opacity-30 px-3 py-2 rounded text-sm font-semibold">
                      ⚠️ Action Required
                    </div>
                  )}

                  <button
                    onClick={() => speakText(alert.message)}
                    className="mt-3 px-3 py-1 bg-white bg-opacity-50 rounded text-xs font-medium hover:bg-opacity-70 transition"
                  >
                    🔊 Speak Alert
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Crop-Specific Alerts */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">🌾 Crop-Specific Alerts</h2>

          <div className="flex gap-4 mb-6 flex-wrap">
            <div className="flex-1 min-w-[200px]">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Select Crop
              </label>
              <select
                value={selectedCrop}
                onChange={(e) => setSelectedCrop(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
              >
                {crops.map((crop) => (
                  <option key={crop} value={crop}>
                    {crop.charAt(0).toUpperCase() + crop.slice(1)}
                  </option>
                ))}
              </select>
            </div>
            <div className="flex items-end">
              <button
                onClick={fetchCropAlerts}
                disabled={loading || !weatherData}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 transition"
              >
                {loading ? 'Loading...' : 'Get Crop Alerts'}
              </button>
            </div>
          </div>

          {showCropAlerts && cropAlerts.length > 0 && (
            <div className="grid grid-cols-1 gap-4">
              {cropAlerts.map((alert, index) => (
                <div
                  key={index}
                  className={`border-l-4 rounded-lg p-4 ${getSeverityColor(alert.severity)}`}
                >
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="font-bold">
                      {selectedCrop.toUpperCase()} - {alert.issue}
                    </h3>
                    <span
                      className={`px-3 py-1 rounded-full text-xs font-semibold ${getSeverityBadge(
                        alert.severity
                      )}`}
                    >
                      {alert.severity.toUpperCase()}
                    </span>
                  </div>
                  <p className="mb-3 font-semibold">Action: {alert.action}</p>
                  <button
                    onClick={() => speakText(`${alert.issue}. ${alert.action}`)}
                    className="px-3 py-1 bg-white bg-opacity-50 rounded text-xs font-medium hover:bg-opacity-70 transition"
                  >
                    🔊 Speak
                  </button>
                </div>
              ))}
            </div>
          )}

          {showCropAlerts && cropAlerts.length === 0 && (
            <div className="bg-green-50 border border-green-200 rounded-lg p-4 text-center">
              <p className="text-green-700 font-semibold">
                ✅ No specific alerts for {selectedCrop}. Conditions are favorable!
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Weather;
