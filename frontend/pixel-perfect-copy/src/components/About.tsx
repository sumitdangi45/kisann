import { useNavigate } from "react-router-dom";
import { Mic } from "lucide-react";
import img_Vxh4GSakf127cXVLEamVAl9JE_jpg from "../assets/external/Vxh4GSakf127cXVLEamVAl9JE.jpg";
import img_jKxnU7K7YUyQuRBwc8ZdkoW3s_svg from "../assets/external/jKxnU7K7YUyQuRBwc8ZdkoW3s.svg";
import img_rdJGZz63dXFUMdxDt6Uq2I2rI_svg from "../assets/external/rdJGZz63dXFUMdxDt6Uq2I2rI.svg";
import img_yrSXe1E6oJ7AvZHbZeE3i4paGA_jpg from "../assets/external/yrSXe1E6oJ7AvZHbZeE3i4paGA.jpg";

const About = () => {
  const navigate = useNavigate();
  return (
    <section id="about" className="py-20 bg-background">
      <div className="max-w-7xl mx-auto px-6 lg:px-16">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center mb-20">
          {/* Microphone Button Section */}
          <div className="relative h-[500px] rounded-3xl overflow-hidden bg-gradient-to-br from-eco-green via-eco-green-dark to-eco-green-dark flex items-center justify-center group">
            {/* Animated background elements */}
            <div className="absolute inset-0 opacity-10">
              <div className="absolute top-10 right-10 w-40 h-40 bg-eco-yellow rounded-full blur-3xl"></div>
              <div className="absolute bottom-10 left-10 w-40 h-40 bg-eco-yellow rounded-full blur-3xl"></div>
            </div>
            
            {/* Content */}
            <div className="relative z-10 flex flex-col items-center gap-6">
              <div className="text-center">
                <h3 className="text-primary-foreground text-2xl font-bold mb-2">Talk to AI Assistant</h3>
                <p className="text-primary-foreground/70 text-sm">Click the microphone to start chatting</p>
              </div>
              
              <button
                onClick={() => navigate("/about")}
                className="bg-eco-yellow text-eco-green-dark p-8 rounded-full shadow-2xl hover:scale-110 transition-all duration-300 hover:shadow-3xl hover:brightness-110 group/btn"
              >
                <Mic className="w-12 h-12 group-hover/btn:animate-pulse" />
              </button>
              
              <p className="text-primary-foreground/60 text-xs mt-4">🎤 Voice & Text Support</p>
            </div>
          </div>

          {/* Content */}
          <div>
            <span className="text-eco-green font-semibold text-sm uppercase tracking-widest">About Us</span>
            <h2 className="font-heading text-3xl md:text-5xl font-bold text-foreground mt-3 mb-8">
              We're Best Agriculture & Organic Farms
            </h2>

            <div className="space-y-6">
              <div className="flex gap-4">
                <div className="w-12 h-12 bg-eco-yellow rounded-full flex items-center justify-center flex-shrink-0">
                  <img src={img_jKxnU7K7YUyQuRBwc8ZdkoW3s_svg} alt="" className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="font-heading text-lg font-bold text-foreground">100% Guaranteed Organic Product</h4>
                  <p className="text-muted-foreground text-sm mt-1">This service includes stabling, daily care, feeding, and access to riding arenas and trails.</p>
                </div>
              </div>

              <div className="flex gap-4">
                <div className="w-12 h-12 bg-eco-yellow rounded-full flex items-center justify-center flex-shrink-0">
                  <img src={img_rdJGZz63dXFUMdxDt6Uq2I2rI_svg} alt="" className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="font-heading text-lg font-bold text-foreground">Top-Quality Healthy Foods Production</h4>
                  <p className="text-muted-foreground text-sm mt-1">Expertly grown seasonal crops using sustainable farming practices to ensure the highest quality produce.</p>
                </div>
              </div>
            </div>

          </div>
        </div>
      </div>
    </section>
  );
};

export default About;
