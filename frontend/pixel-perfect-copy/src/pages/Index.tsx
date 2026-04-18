import Navbar from "@/components/Navbar";
import Hero from "@/components/Hero";
import YellowBanner from "@/components/YellowBanner";
import Services from "@/components/Services";
import About from "@/components/About";
import Projects from "@/components/Projects";
import HowWeWork from "@/components/HowWeWork";
import Team from "@/components/Team";
import Testimonials from "@/components/Testimonials";
import FAQ from "@/components/FAQ";
import Blog from "@/components/Blog";
import Footer from "@/components/Footer";
import KisanSathiServicesSection from "@/components/KisanSathiServicesSection";

const Index = () => {
  return (
    <div className="min-h-screen">
      <Navbar />
      <Hero />
      <KisanSathiServicesSection />
      <YellowBanner />
      <Services />
      <About />
      <Projects />
      <HowWeWork />
      <Team />
      <Testimonials />
      <FAQ />
      <Blog />
      <Footer />
    </div>
  );
};

export default Index;
