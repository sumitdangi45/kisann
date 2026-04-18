import { useState } from "react";
import { ChevronDown } from "lucide-react";

import img_BOLtGGPkktAAAMX75ryj66ff0E_jpg from "../assets/external/BOLtGGPkktAAAMX75ryj66ff0E.jpg";
import img_RLae8rFgka9llSGK2Jajl5UKjeg_svg from "../assets/external/RLae8rFgka9llSGK2Jajl5UKjeg.svg";

const faqs = [
  { q: "What types of produce do you grow?", a: "We grow a wide variety of organic fruits, vegetables, and herbs using sustainable farming practices." },
  { q: "How can I purchase your products?", a: "You can purchase our products through our online shop, farmers' markets, or directly at our farm store." },
  { q: "Do you offer farm tours?", a: "Yes! We offer guided farm tours every weekend. You can book through our website or call us directly." },
  { q: "Do you use any chemicals or pesticides?", a: "No, we are 100% organic. We use only natural methods for pest control and soil enhancement." },
];

const FAQ = () => {
  const [open, setOpen] = useState<number | null>(null);

  return (
    <section className="py-20 bg-background">
      <div className="max-w-7xl mx-auto px-6 lg:px-16">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-start">
          {/* Image */}
          <div className="relative">
            <img
              src={img_BOLtGGPkktAAAMX75ryj66ff0E_jpg}
              alt="FAQ"
              className="w-full h-[500px] object-cover rounded-3xl"
            />
            <div className="absolute bottom-6 left-6 bg-eco-green text-primary-foreground rounded-2xl p-5 flex items-center gap-3">
              <img src={img_RLae8rFgka9llSGK2Jajl5UKjeg_svg} alt="" className="w-8 h-8" />
              <div>
                <p className="font-bold text-lg">+123 456 789 963</p>
                <p className="text-primary-foreground/60 text-xs">Book a free visiting</p>
              </div>
            </div>
          </div>

          {/* FAQ Content */}
          <div>
            <span className="text-eco-green font-semibold text-sm uppercase tracking-widest">Frequently Asked Questions</span>
            <h2 className="font-heading text-3xl md:text-5xl font-bold text-foreground mt-3 mb-8">
              How can we help you?
            </h2>

            <div className="space-y-4">
              {faqs.map((faq, i) => (
                <div
                  key={i}
                  className="border border-border rounded-xl overflow-hidden"
                >
                  <button
                    onClick={() => setOpen(open === i ? null : i)}
                    className="w-full flex items-center justify-between p-5 text-left"
                  >
                    <span className="font-heading text-base font-semibold text-foreground">{faq.q}</span>
                    <ChevronDown
                      className={`w-5 h-5 text-muted-foreground transition-transform ${open === i ? "rotate-180" : ""}`}
                    />
                  </button>
                  {open === i && (
                    <div className="px-5 pb-5 text-muted-foreground text-sm">
                      {faq.a}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default FAQ;
