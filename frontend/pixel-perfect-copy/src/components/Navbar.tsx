import { useState } from "react";
import { Menu, X, ChevronDown } from "lucide-react";
import { useLanguage } from "@/context/LanguageContext";

import img_img_4rNEIMZl5loHoK9yMLJIIMimC4_svg from "../assets/external/4rNEIMZl5loHoK9yMLJIIMimC4.svg";

const Navbar = () => {
  const { t } = useLanguage();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [dropdownOpen, setDropdownOpen] = useState(false);

  const essentialPages = [
    { label: t('nav.gallery'), href: "/gallery" },
    { label: t('nav.schemes'), href: "/schemes" },
    { label: t('nav.faq'), href: "/faq" },
    { label: t('nav.resources'), href: "/resources" },
  ];

  return (
    <nav className="absolute top-0 left-0 right-0 z-50 px-6 lg:px-16 py-5">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        {/* Logo */}
        <a href="/" className="flex items-center gap-2">
          <img
            src={img_img_4rNEIMZl5loHoK9yMLJIIMimC4_svg}
            alt="KisanSathi"
            className="h-10 w-10"
          />
          <div className="flex flex-col">
            <span className="text-primary-foreground font-heading text-2xl font-bold">KisanSathi</span>
            <span className="text-eco-yellow text-xs font-semibold">AI Assistant</span>
          </div>
        </a>

        {/* Desktop Nav */}
        <div className="hidden lg:flex items-center gap-10">
          <a href="/" className="text-eco-yellow font-semibold text-sm tracking-wide">{t('nav.home')}</a>
          <a href="/about" className="text-primary-foreground/80 hover:text-primary-foreground text-sm font-medium transition-colors">{t('nav.chatbot')}</a>
          <div
            className="relative group"
            onMouseEnter={() => setDropdownOpen(true)}
            onMouseLeave={() => setDropdownOpen(false)}
          >
            <button className="flex items-center gap-1 text-primary-foreground/80 hover:text-primary-foreground text-sm font-medium transition-colors">
              {t('nav.essentialPages')} <ChevronDown className={`w-4 h-4 transition-transform ${dropdownOpen ? "rotate-180" : ""}`} />
            </button>
            {dropdownOpen && (
              <div className="absolute top-full left-0 mt-2 bg-eco-green-dark/95 backdrop-blur-md rounded-xl py-3 min-w-[200px] shadow-xl border border-primary-foreground/10">
                {essentialPages.map((page) => (
                  <a
                    key={page.href}
                    href={page.href}
                    className="block px-5 py-2.5 text-primary-foreground/80 hover:text-eco-yellow hover:bg-primary-foreground/5 text-sm font-medium transition-colors"
                  >
                    {page.label}
                  </a>
                ))}
              </div>
            )}
          </div>
          <a href="/shop" className="text-primary-foreground/80 hover:text-primary-foreground text-sm font-medium transition-colors">{t('nav.shop')}</a>
        </div>

        {/* CTA */}
        <a
          href="/auth"
          className="hidden lg:flex items-center gap-2 bg-eco-yellow text-eco-green-dark font-semibold px-6 py-3 rounded-full text-sm hover:brightness-110 transition-all"
        >
          {t('nav.getStarted')}
          <span className="bg-eco-green-dark text-primary-foreground rounded-full w-6 h-6 flex items-center justify-center text-xs">→</span>
        </a>

        {/* Mobile Toggle */}
        <button
          onClick={() => setMobileOpen(!mobileOpen)}
          className="lg:hidden text-primary-foreground"
        >
          {mobileOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
        </button>
      </div>

      {/* Mobile Menu */}
      {mobileOpen && (
        <div className="lg:hidden mt-4 bg-eco-green-dark/95 backdrop-blur-md rounded-2xl p-6 flex flex-col gap-4">
          <a href="/" className="text-eco-yellow font-semibold">{t('nav.home')}</a>
          <a href="/about" className="text-primary-foreground/80">{t('nav.chatbot')}</a>
          <a href="/gallery" className="text-primary-foreground/80">{t('nav.gallery')}</a>
          <a href="/schemes" className="text-primary-foreground/80">{t('nav.schemes')}</a>
          <a href="/faq" className="text-primary-foreground/80">{t('nav.faq')}</a>
          <a href="/shop" className="text-primary-foreground/80">{t('nav.shop')}</a>
          <a href="#contact" className="bg-eco-yellow text-eco-green-dark font-semibold px-6 py-3 rounded-full text-sm text-center">
            {t('nav.getStarted')}
          </a>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
