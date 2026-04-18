import img_pcb5yTRmmPb3AD4e14mWz1oMukM_jpg from "../assets/external/pcb5yTRmmPb3AD4e14mWz1oMukM.jpg";
import { useLanguage } from "@/context/LanguageContext";

const Hero = () => {
  const { t } = useLanguage();
  return (
    <section className="relative min-h-screen flex items-center overflow-hidden">
      {/* Background Image */}
      <div className="absolute inset-0">
        <img
          src={img_pcb5yTRmmPb3AD4e14mWz1oMukM_jpg}
          alt="Hero BG"
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-r from-eco-green-dark/80 via-eco-green-dark/50 to-transparent" />
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-6 lg:px-16 pt-32 pb-20 w-full">
        <div className="max-w-2xl">
          <div className="inline-block border border-eco-yellow/40 rounded-full px-5 py-2 mb-6">
            <span className="text-eco-yellow text-sm font-medium">{t('hero.badge')}</span>
          </div>

          <h1 className="font-heading text-5xl md:text-7xl font-bold text-primary-foreground leading-tight mb-6">
            {t('hero.title')}
          </h1>

          <p className="text-primary-foreground/70 text-base md:text-lg max-w-lg mb-10 leading-relaxed">
            {t('hero.subtitle')}
          </p>

          <div className="flex flex-wrap gap-4">
            <a
              href="/schemes"
              className="flex items-center gap-3 bg-eco-green text-primary-foreground font-semibold px-7 py-4 rounded-full text-sm hover:bg-eco-green-light transition-colors"
            >
              {t('hero.schemes')}
              <span className="bg-eco-yellow text-eco-green-dark rounded-full w-7 h-7 flex items-center justify-center">→</span>
            </a>
            <a
              href="/services"
              className="flex items-center gap-3 border border-eco-yellow/50 text-eco-yellow font-semibold px-7 py-4 rounded-full text-sm hover:bg-eco-yellow/10 transition-colors"
            >
              {t('hero.services')}
              <span className="bg-eco-yellow text-eco-green-dark rounded-full w-7 h-7 flex items-center justify-center">→</span>
            </a>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
