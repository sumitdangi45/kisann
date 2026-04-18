import { useState } from "react";
import { Eye, EyeOff, Phone, User, Leaf, Mail, Lock } from "lucide-react";
import { useNavigate } from "react-router-dom";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { useLanguage } from "@/context/LanguageContext";

const AuthPage = () => {
  const navigate = useNavigate();
  const { t } = useLanguage();
  const [isLogin, setIsLogin] = useState(true);
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    mobileNo: "",
    agricultureType: "",
    password: "",
    confirmPassword: "",
  });

  const agricultureTypes = [
    "🌾 Cereals (Rice, Wheat, Maize)",
    "🥬 Vegetables (Tomato, Onion, Potato)",
    "🌻 Cash Crops (Cotton, Sugarcane)",
    "🍎 Fruits & Orchards",
    "🌱 Organic Farming",
    "🐄 Dairy & Livestock",
    "🐟 Aquaculture",
    "🍯 Beekeeping",
    "🌿 Spices & Herbs",
    "🥕 Mixed Farming",
  ];

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
    setError("");
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    setLoading(true);

    try {
      if (isLogin) {
        const response = await fetch("http://localhost:5000/api/auth/login", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            mobile: formData.mobileNo,
            password: formData.password,
          }),
        });

        const data = await response.json();

        if (data.success) {
          localStorage.setItem("token", data.token);
          localStorage.setItem("user_id", data.user_id);
          localStorage.setItem("user_name", data.name);
          
          setSuccess("Login successful! Redirecting...");
          setTimeout(() => {
            navigate("/");
          }, 1500);
        } else {
          setError(data.error || "Login failed");
        }
      } else {
        if (formData.password !== formData.confirmPassword) {
          setError("Passwords do not match!");
          setLoading(false);
          return;
        }

        const response = await fetch("http://localhost:5000/api/auth/register", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            name: formData.name,
            email: formData.email,
            mobile: formData.mobileNo,
            agriculture_type: formData.agricultureType,
            password: formData.password,
          }),
        });

        const data = await response.json();

        if (data.success) {
          localStorage.setItem("token", data.token);
          localStorage.setItem("user_id", data.user_id);
          localStorage.setItem("user_name", data.name);
          
          setSuccess("Account created successfully! Redirecting...");
          setTimeout(() => {
            navigate("/");
          }, 1500);
        } else {
          setError(data.error || "Registration failed");
        }
      }
    } catch (err) {
      setError("Connection error. Please try again.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-slate-50 via-white to-green-50">
      <Navbar />

      {/* Hero Section */}
      <section className="relative py-16 bg-gradient-to-r from-eco-green via-eco-green-dark to-teal-700 text-white overflow-hidden">
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-0 right-0 w-96 h-96 bg-white rounded-full blur-3xl"></div>
          <div className="absolute bottom-0 left-0 w-96 h-96 bg-white rounded-full blur-3xl"></div>
        </div>
        <div className="relative max-w-7xl mx-auto px-6 lg:px-16">
          <div className="text-center">
            <h1 className="font-heading text-4xl md:text-5xl font-bold mb-4">
              {t('auth.title')}
            </h1>
            <p className="text-white/80 text-lg max-w-2xl mx-auto">
              {t('auth.subtitle')}
            </p>
          </div>
        </div>
      </section>

      {/* Auth Container */}
      <section className="flex-1 py-16 px-6">
        <div className="max-w-md mx-auto">
          {/* Toggle Buttons */}
          <div className="flex gap-3 mb-8 bg-white rounded-xl p-1 shadow-md">
            <button
              onClick={() => {
                setIsLogin(true);
                setError("");
                setSuccess("");
              }}
              className={`flex-1 py-3 px-4 rounded-lg font-semibold transition-all duration-300 ${
                isLogin
                  ? "bg-gradient-to-r from-eco-green to-teal-600 text-white shadow-lg"
                  : "text-gray-600 hover:text-gray-900"
              }`}
            >
              {t('auth.login')}
            </button>
            <button
              onClick={() => {
                setIsLogin(false);
                setError("");
                setSuccess("");
              }}
              className={`flex-1 py-3 px-4 rounded-lg font-semibold transition-all duration-300 ${
                !isLogin
                  ? "bg-gradient-to-r from-eco-green to-teal-600 text-white shadow-lg"
                  : "text-gray-600 hover:text-gray-900"
              }`}
            >
              {t('auth.signup')}
            </button>
          </div>

          {/* Error Message */}
          {error && (
            <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-700 text-sm font-medium">❌ {error}</p>
            </div>
          )}

          {/* Success Message */}
          {success && (
            <div className="mb-4 p-4 bg-green-50 border border-green-200 rounded-lg">
              <p className="text-green-700 text-sm font-medium">✅ {success}</p>
            </div>
          )}

          {/* Form Card */}
          <div className="bg-white rounded-2xl p-8 shadow-xl border border-green-100">
            <h2 className="text-2xl font-bold text-eco-green-dark mb-2 text-center">
              {isLogin ? t('auth.welcome') : t('auth.create')}
            </h2>
            <p className="text-center text-gray-600 text-sm mb-6">
              {isLogin ? t('auth.login_desc') : t('auth.signup_desc')}
            </p>

            <form onSubmit={handleSubmit} className="space-y-4">
              {/* Name Field (Sign Up Only) */}
              {!isLogin && (
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    <User className="inline w-4 h-4 mr-2" />
                    {t('auth.name')}
                  </label>
                  <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    placeholder={t('auth.name')}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-eco-green focus:ring-2 focus:ring-eco-green/20 focus:outline-none transition"
                    required={!isLogin}
                  />
                </div>
              )}

              {/* Email Field (Sign Up Only) */}
              {!isLogin && (
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    <Mail className="inline w-4 h-4 mr-2" />
                    {t('auth.email')}
                  </label>
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    placeholder={t('auth.email')}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-eco-green focus:ring-2 focus:ring-eco-green/20 focus:outline-none transition"
                    required={!isLogin}
                  />
                </div>
              )}

              {/* Mobile Number */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  <Phone className="inline w-4 h-4 mr-2" />
                  {t('auth.mobile')}
                </label>
                <input
                  type="tel"
                  name="mobileNo"
                  value={formData.mobileNo}
                  onChange={handleChange}
                  placeholder="10-digit mobile number"
                  pattern="[0-9]{10}"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-eco-green focus:ring-2 focus:ring-eco-green/20 focus:outline-none transition"
                  required
                />
              </div>

              {/* Agriculture Type (Sign Up Only) */}
              {!isLogin && (
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    <Leaf className="inline w-4 h-4 mr-2" />
                    {t('auth.agriculture')}
                  </label>
                  <select
                    name="agricultureType"
                    value={formData.agricultureType}
                    onChange={handleChange}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-eco-green focus:ring-2 focus:ring-eco-green/20 focus:outline-none transition bg-white"
                    required={!isLogin}
                  >
                    <option value="">{t('auth.agriculture')}</option>
                    {agricultureTypes.map((type) => (
                      <option key={type} value={type}>
                        {type}
                      </option>
                    ))}
                  </select>
                </div>
              )}

              {/* Password */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  <Lock className="inline w-4 h-4 mr-2" />
                  {t('auth.password')}
                </label>
                <div className="relative">
                  <input
                    type={showPassword ? "text" : "password"}
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    placeholder={t('auth.password')}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-eco-green focus:ring-2 focus:ring-eco-green/20 focus:outline-none transition"
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-3 text-gray-500 hover:text-eco-green transition"
                  >
                    {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                  </button>
                </div>
              </div>

              {/* Confirm Password (Sign Up Only) */}
              {!isLogin && (
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    <Lock className="inline w-4 h-4 mr-2" />
                    {t('auth.confirm')}
                  </label>
                  <input
                    type={showPassword ? "text" : "password"}
                    name="confirmPassword"
                    value={formData.confirmPassword}
                    onChange={handleChange}
                    placeholder={t('auth.confirm')}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-eco-green focus:ring-2 focus:ring-eco-green/20 focus:outline-none transition"
                    required={!isLogin}
                  />
                </div>
              )}

              {/* Submit Button */}
              <button
                type="submit"
                disabled={loading}
                className="w-full py-3 px-4 bg-gradient-to-r from-eco-green to-teal-600 text-white font-bold rounded-lg hover:shadow-lg hover:brightness-105 transition-all mt-6 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? "Processing..." : isLogin ? t('auth.loginBtn') : t('auth.signupBtn')}
              </button>
            </form>

            {/* Divider */}
            <div className="my-6 flex items-center gap-3">
              <div className="flex-1 h-px bg-gray-200"></div>
              <span className="text-gray-500 text-sm">or</span>
              <div className="flex-1 h-px bg-gray-200"></div>
            </div>

            {/* Social Login */}
            <div className="grid grid-cols-2 gap-3">
              <button className="py-2 px-4 border border-gray-300 rounded-lg hover:bg-gray-50 transition text-sm font-medium">
                📱 WhatsApp
              </button>
              <button className="py-2 px-4 border border-gray-300 rounded-lg hover:bg-gray-50 transition text-sm font-medium">
                🔗 Google
              </button>
            </div>
          </div>

          {/* Features */}
          <div className="mt-8 grid grid-cols-3 gap-3">
            <div className="p-4 bg-white rounded-xl shadow-md border border-green-100 text-center hover:shadow-lg transition">
              <p className="text-3xl mb-2">🌾</p>
              <p className="text-xs font-semibold text-gray-700">{t('auth.smartFarming')}</p>
            </div>
            <div className="p-4 bg-white rounded-xl shadow-md border border-green-100 text-center hover:shadow-lg transition">
              <p className="text-3xl mb-2">📱</p>
              <p className="text-xs font-semibold text-gray-700">{t('auth.easyAccess')}</p>
            </div>
            <div className="p-4 bg-white rounded-xl shadow-md border border-green-100 text-center hover:shadow-lg transition">
              <p className="text-3xl mb-2">🤖</p>
              <p className="text-xs font-semibold text-gray-700">{t('auth.aiAssistant')}</p>
            </div>
          </div>

          {/* Info Box */}
          <div className="mt-6 p-4 bg-gradient-to-r from-green-50 to-teal-50 border-l-4 border-eco-green rounded-lg">
            <p className="text-sm text-gray-700">
              <strong>{t('auth.tip')}</strong> {isLogin ? t('auth.tipLogin') : t('auth.tipSignup')}
            </p>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default AuthPage;
