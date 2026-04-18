import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { Toaster } from "@/components/ui/toaster";
import { TooltipProvider } from "@/components/ui/tooltip";
import Index from "./pages/Index.tsx";
import AboutPage from "./pages/AboutPage.tsx";
import ShopPage from "./pages/ShopPage.tsx";
import GalleryPage from "./pages/GalleryPage.tsx";
import TestimonialPage from "./pages/TestimonialPage.tsx";
import GovernmentSchemesPage from "./pages/GovernmentSchemesPage.tsx";
import FAQPage from "./pages/FAQPage.tsx";
import NotFound from "./pages/NotFound.tsx";
import CropCompletePage from "./pages/CropCompletePage.tsx";
import FertilizerPage from "./pages/FertilizerPage.tsx";
import DiseasePage from "./pages/DiseasePage.tsx";
import ServicesPage from "./pages/ServicesPage.tsx";
import WeatherPage from "./pages/WeatherPage.tsx";
import SmartRemindersPage from "./pages/SmartRemindersPage.tsx";
import VoiceAssistantPage from "./pages/VoiceAssistantPage.tsx";
import ChatbotPage from "./pages/ChatbotPage.tsx";
import ResourcesPage from "./pages/ResourcesPage.tsx";
import AuthPage from "./pages/AuthPage.tsx";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Index />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/shop" element={<ShopPage />} />
          <Route path="/gallery" element={<GalleryPage />} />
          <Route path="/testimonial" element={<TestimonialPage />} />
          <Route path="/schemes" element={<GovernmentSchemesPage />} />
          <Route path="/faq" element={<FAQPage />} />
          <Route path="/services" element={<ServicesPage />} />
          <Route path="/crop" element={<CropCompletePage />} />
          <Route path="/fertilizer" element={<FertilizerPage />} />
          <Route path="/disease" element={<DiseasePage />} />
          <Route path="/weather" element={<WeatherPage />} />
          <Route path="/reminders" element={<SmartRemindersPage />} />
          <Route path="/voice-assistant" element={<VoiceAssistantPage />} />
          <Route path="/chatbot" element={<ChatbotPage />} />
          <Route path="/resources" element={<ResourcesPage />} />
          <Route path="/auth" element={<AuthPage />} />
          {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
