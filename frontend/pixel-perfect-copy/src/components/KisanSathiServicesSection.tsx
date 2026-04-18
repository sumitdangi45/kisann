import { Link } from 'react-router-dom';

const KisanSathiServicesSection = () => {
  const services = [
    {
      title: 'AI Chatbot',
      description: 'Talk to KisanSathi AI. Ask about crops, fertilizer, diseases, weather, and more. Voice and text support.',
      icon: '🤖',
      link: '/chatbot'
    },
    {
      title: 'Crop Recommendation',
      description: 'Get personalized crop recommendations using AI, voice input, or seasonal data.',
      icon: '🌾',
      link: '/crop'
    },
    {
      title: 'Fertilizer Recommendation',
      description: 'Receive optimal fertilizer suggestions to maximize crop yield and soil health.',
      icon: '🧪',
      link: '/fertilizer'
    },
    {
      title: 'Disease Detection',
      description: 'Identify plant diseases early using AI-powered image analysis for timely intervention.',
      icon: '🔍',
      link: '/disease'
    },
    {
      title: 'Weather & Alerts',
      description: 'Get real-time weather alerts and crop-specific recommendations based on current conditions.',
      icon: '🌤️',
      link: '/weather'
    },
    {
      title: 'Smart Reminders',
      description: 'Track your crops with automated reminders for every task throughout the season.',
      icon: '📅',
      link: '/reminders'
    }
  ];

  return (
    <section className="py-20 bg-eco-cream">
      <div className="max-w-7xl mx-auto px-6 lg:px-16">
        <div className="text-center mb-14">
          <span className="text-eco-green font-semibold text-sm uppercase tracking-widest">KisanSathi Services</span>
          <h2 className="font-heading text-3xl md:text-5xl font-bold text-foreground mt-3">
            Smart Farming Solutions
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {services.map((service, i) => (
            <Link key={i} to={service.link}>
              <div className="group cursor-pointer bg-white rounded-2xl p-6 shadow-md hover:shadow-xl transition-all hover:scale-105 h-full">
                <div className="text-4xl mb-3">{service.icon}</div>
                <h3 className="text-lg font-bold text-eco-green-dark mb-2">{service.title}</h3>
                <p className="text-gray-600 text-sm mb-4">{service.description}</p>
                <div className="flex items-center gap-2 text-eco-green font-semibold text-sm">
                  Get Started <span>→</span>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </section>
  );
};

export default KisanSathiServicesSection;
