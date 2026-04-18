import { useState } from "react";
import { Eye, EyeOff, Phone, User, Leaf } from "lucide-react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

const AuthPage = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [showPassword, setShowPassword] = useState(false);
  const [formData, setFormData] = useState({
    name: "",
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
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (isLogin) {
      console.log("Login:", { mobileNo: formData.mobileNo, password: formData.password });
      alert("Login successful! Welcome back!");
    } else {
      if (formData.password !== formData.confirmPassword) {
        alert("Passwords do not match!");
        return;
      }
      console.log("Sign Up:", formData);
      alert("Account created successfully!");
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />

      {/* Hero Section */}
      <section className="relative py-12 bg-gradient-to-r from-green-50 to-teal-50">
        <div className="max-w-7xl mx-auto px-6 lg:px-16">
          <div className="text-center">
            <h1 className="font-heading text-4xl md:text-5xl font-bold text-eco-green-dark mb-4">
              🌾 KisanSathi - Farmer Portal
            </h1>
            <p className="text-gray-600 text-lg">
              Join thousands of farmers using smart agriculture solutions
            </p>
          </div>
        </div>
      </section>

      {/* Auth Container */}
      <section className="flex-1 py-12 bg-white">
        <div className="max-w-md mx-auto px-6">
          {/* Toggle Buttons */}
          <div className="flex gap-4 mb-8">
            <button
              onClick={() => setIsLogin(true)}
              className={`flex-1 py-3 px-4 rounded-lg font-semibold transition-all ${
                isLogin
                  ? "bg-gradient-to-r from-green-600 to-teal-600 text-white shadow-lg"
                  : "bg-gray-100 text-gray-700 hover:bg-gray-200"
              }`}
            >
              🔐 Login
            </button>
            <button
              onClick={() => setIsLogin(false)}
              className={`flex-1 py-3 px-4 rounded-lg font-semibold transition-all ${
                !isLogin
                  ? "bg-gradient-to-r from-green-600 to-teal-600 text-white shadow-lg"
                  : "bg-gray-100 text-gray-700 hover:bg-gray-200"
              }`}
            >
              ✍️ Sign Up
            </button>
          </div>

          {/* Form Card */}
          <div className="bg-white border-2 border-green-100 rounded-2xl p-8 shadow-lg">
            <h2 className="text-2xl font-bold text-eco-green-dark mb-6 text-center">
              {isLogin ? "Welcome Back, Farmer!" : "Join KisanSathi Today!"}
            </h2>

            <form onSubmit={handleSubmit} className="space-y-5">
              {/* Name Field (Sign Up Only) */}
              {!isLogin && (
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    <User className="inline w-4 h-4 mr-2" />
                    Full Name
                  </label>
                  <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    placeholder="Enter your full name"
                    className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-green-500 focus:outline-none transition"
                    required={!isLogin}
                  />
                </div>
              )}

              {/* Mobile Number */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  <Phone className="inline w-4 h-4 mr-2" />
                  Mobile Number
                </label>
                <input
                  type="tel"
                  name="mobileNo"
                  value={formData.mobileNo}
                  onChange={handleChange}
                  placeholder="Enter 10-digit mobile number"
                  pattern="[0-9]{10}"
                  className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-green-500 focus:outline-none transition"
                  required
                />
              </div>

              {/* Agriculture Type (Sign Up Only) */}
              {!isLogin && (
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    <Leaf className="inline w-4 h-4 mr-2" />
                    Type of Agriculture
                  </label>
                  <select
                    name="agricultureType"
                    value={formData.agricultureType}
                    onChange={handleChange}
                    className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-green-500 focus:outline-none transition bg-white"
                    required={!isLogin}
                  >
                    <option value="">Select your agriculture type</option>
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
                  🔒 Password
                </label>
                <div className="relative">
                  <input
                    type={showPassword ? "text" : "password"}
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    placeholder="Enter password"
                    className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-green-500 focus:outline-none transition"
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-3 text-gray-500 hover:text-gray-700"
                  >
                    {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                  </button>
                </div>
              </div>

              {/* Confirm Password (Sign Up Only) */}
              {!isLogin && (
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    🔒 Confirm Password
                  </label>
                  <input
                    type={showPassword ? "text" : "password"}
                    name="confirmPassword"
                    value={formData.confirmPassword}
                    onChange={handleChange}
                    placeholder="Confirm password"
                    className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-green-500 focus:outline-none transition"
                    required={!isLogin}
                  />
                </div>
              )}

              {/* Submit Button */}
              <button
                type="submit"
                className="w-full py-3 px-4 bg-gradient-to-r from-green-600 to-teal-600 text-white font-bold rounded-lg hover:brightness-110 transition-all shadow-lg mt-6"
              >
                {isLogin ? "🔓 Login" : "✅ Create Account"}
              </button>
            </form>

            {/* Info Box */}
            <div className="mt-6 p-4 bg-green-50 border-l-4 border-green-500 rounded">
              <p className="text-sm text-gray-700">
                <strong>💡 Tip:</strong> {isLogin ? "Don't have an account? Click Sign Up to join!" : "Already have an account? Click Login!"}
              </p>
            </div>
          </div>

          {/* Features */}
          <div className="mt-8 grid grid-cols-3 gap-4 text-center">
            <div className="p-4 bg-green-50 rounded-lg">
              <p className="text-2xl mb-2">🌾</p>
              <p className="text-xs font-semibold text-gray-700">Smart Farming</p>
            </div>
            <div className="p-4 bg-green-50 rounded-lg">
              <p className="text-2xl mb-2">📱</p>
              <p className="text-xs font-semibold text-gray-700">Easy Access</p>
            </div>
            <div className="p-4 bg-green-50 rounded-lg">
              <p className="text-2xl mb-2">🤖</p>
              <p className="text-xs font-semibold text-gray-700">AI Assistant</p>
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default AuthPage;
