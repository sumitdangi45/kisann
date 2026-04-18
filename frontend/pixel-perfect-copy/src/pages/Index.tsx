import Navbar from "@/components/Navbar";
import Hero from "@/components/Hero";
import About from "@/components/About";
import HowWeWork from "@/components/HowWeWork";
import FAQ from "@/components/FAQ";
import Footer from "@/components/Footer";
import KisanSathiServicesSection from "@/components/KisanSathiServicesSection";
import ShopPreview from "@/components/ShopPreview";

const Index = () => {
  return (
    <div className="min-h-screen">
      <Navbar />
      <Hero />
      <KisanSathiServicesSection />
      <ShopPreview />
      <About />
      <HowWeWork />
      <FAQ />
      <Footer />
    </div>
  );
};

export default Index;
