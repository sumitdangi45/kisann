import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { ShoppingCart, ExternalLink, Mic } from "lucide-react";
import { useNavigate } from "react-router-dom";

const products = [
  { 
    name: "Neem Oil (Organic Pesticide)", 
    price: "₹250-350", 
    image: "https://m.media-amazon.com/images/I/31Hjv+PFTtL._SX342_SY445_QL70_FMwebp_.jpg",
    amazon: "https://www.amazon.in/s?k=neem+oil+pesticide",
    flipkart: "https://www.flipkart.com/search?q=neem+oil+pesticide"
  },
  { 
    name: "DAP Fertilizer (18:46:0)", 
    price: "₹600-800/50kg", 
    image: "https://images.unsplash.com/photo-1574943320219-553eb213f72d?w=400&h=400&fit=crop",
    amazon: "https://www.amazon.in/s?k=DAP+fertilizer",
    flipkart: "https://www.flipkart.com/search?q=DAP+fertilizer"
  },
  { 
    name: "Urea Fertilizer (46% N)", 
    price: "₹500-700/50kg", 
    image: "https://m.media-amazon.com/images/I/617MOehEBaL._SX522_.jpg",
    amazon: "https://www.amazon.in/s?k=urea+fertilizer",
    flipkart: "https://www.flipkart.com/search?q=urea+fertilizer"
  },
  { 
    name: "Carbofuran (Insecticide)", 
    price: "₹400-550", 
    image: "https://images.unsplash.com/photo-1599599810694-b5ac4dd64b73?w=400&h=400&fit=crop",
    amazon: "https://www.amazon.in/s?k=carbofuran+insecticide",
    flipkart: "https://www.flipkart.com/search?q=carbofuran+insecticide"
  },
  { 
    name: "Potassium Chloride (MOP)", 
    price: "₹700-900/50kg", 
    image: "https://images.unsplash.com/photo-1584622181563-430f63602d4b?w=400&h=400&fit=crop",
    amazon: "https://www.amazon.in/s?k=potassium+chloride+MOP",
    flipkart: "https://www.flipkart.com/search?q=potassium+chloride+MOP"
  },
  { 
    name: "Sulfur Powder (Fungicide)", 
    price: "₹200-300/kg", 
    image: "https://images.unsplash.com/photo-1585314062340-f4346add912b?w=400&h=400&fit=crop",
    amazon: "https://www.amazon.in/s?k=sulfur+powder+fungicide",
    flipkart: "https://www.flipkart.com/search?q=sulfur+powder+fungicide"
  },
  { 
    name: "Copper Fungicide", 
    price: "₹350-500", 
    image: "https://images.unsplash.com/photo-1576091160550-112173f7f869?w=400&h=400&fit=crop",
    amazon: "https://www.amazon.in/s?k=copper+fungicide",
    flipkart: "https://www.flipkart.com/search?q=copper+fungicide"
  },
  { 
    name: "Azospirillum Bio-Fertilizer", 
    price: "₹150-250/kg", 
    image: "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=400&h=400&fit=crop",
    amazon: "https://www.amazon.in/s?k=azospirillum+biofertilizer",
    flipkart: "https://www.flipkart.com/search?q=azospirillum+biofertilizer"
  },
  { 
    name: "Zinc Sulfate (Micronutrient)", 
    price: "₹300-450/kg", 
    image: "https://images.unsplash.com/photo-1585314062340-f4346add912b?w=400&h=400&fit=crop",
    amazon: "https://www.amazon.in/s?k=zinc+sulfate+micronutrient",
    flipkart: "https://www.flipkart.com/search?q=zinc+sulfate+micronutrient"
  },
  { 
    name: "Mancozeb Fungicide", 
    price: "₹400-600", 
    image: "https://images.unsplash.com/photo-1599599810694-b5ac4dd64b73?w=400&h=400&fit=crop",
    amazon: "https://www.amazon.in/s?k=mancozeb+fungicide",
    flipkart: "https://www.flipkart.com/search?q=mancozeb+fungicide"
  },
  { 
    name: "Bacillus Thuringiensis (Bt)", 
    price: "₹200-350/kg", 
    image: "https://images.unsplash.com/photo-1576091160550-112173f7f869?w=400&h=400&fit=crop",
    amazon: "https://www.amazon.in/s?k=bacillus+thuringiensis+bt",
    flipkart: "https://www.flipkart.com/search?q=bacillus+thuringiensis+bt"
  },
  { 
    name: "Vermicompost (Organic)", 
    price: "₹150-250/kg", 
    image: "https://images.unsplash.com/photo-1625246333195-78d9c38ad576?w=400&h=400&fit=crop",
    amazon: "https://www.amazon.in/s?k=vermicompost+organic",
    flipkart: "https://www.flipkart.com/search?q=vermicompost+organic"
  },
];

const ShopPage = () => {
  const navigate = useNavigate();
  return (
    <div className="min-h-screen">
      <Navbar />

      {/* Hero Banner */}
      <section className="relative h-[400px] md:h-[480px] flex items-center">
        <img
          src="https://cdn.pixabay.com/photo/2016/09/21/04/46/barley-field-1684052_1280.jpg"
          alt="Shop Hero"
          className="absolute inset-0 w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-black/40" />
        <div className="relative z-10 max-w-7xl mx-auto px-6 lg:px-16 w-full">
          <h1 className="font-heading text-5xl md:text-7xl font-bold text-primary-foreground mb-4">
            🧪 Agricultural Medicines & Fertilizers
          </h1>
          <p className="text-primary-foreground/80 text-lg md:text-xl max-w-lg">
            Quality pesticides, fertilizers, and bio-products for healthy crops
          </p>
        </div>
      </section>

      {/* Products Grid */}
      <section className="py-16 md:py-24 bg-white">
        <div className="max-w-7xl mx-auto px-6 lg:px-16">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {products.map((product, index) => (
              <div key={index} className="group cursor-pointer">
                <div className="bg-gradient-to-br from-green-100 to-teal-100 rounded-2xl overflow-hidden aspect-square flex items-center justify-center p-4 hover:shadow-lg transition-shadow">
                  <img 
                    src={product.image} 
                    alt={product.name}
                    className="w-full h-full object-cover rounded-lg"
                    onError={(e) => {
                      e.currentTarget.src = "https://via.placeholder.com/400?text=" + encodeURIComponent(product.name.split('(')[0].trim());
                    }}
                  />
                </div>
                <div className="text-center mt-5">
                  <h3 className="font-heading text-lg font-bold text-eco-green-dark">
                    {product.name}
                  </h3>
                  <p className="text-muted-foreground mt-1 font-semibold text-green-600">
                    {product.price}
                  </p>
                  
                  {/* Buy Buttons */}
                  <div className="flex gap-3 mt-4">
                    <a
                      href={product.amazon}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex-1 inline-flex items-center justify-center gap-2 bg-yellow-500 hover:bg-yellow-600 text-white font-semibold py-2 px-3 rounded-lg transition-all text-sm"
                    >
                      <ShoppingCart className="w-4 h-4" />
                      Amazon
                      <ExternalLink className="w-3 h-3" />
                    </a>
                    <a
                      href={product.flipkart}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex-1 inline-flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-3 rounded-lg transition-all text-sm"
                    >
                      <ShoppingCart className="w-4 h-4" />
                      Flipkart
                      <ExternalLink className="w-3 h-3" />
                    </a>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default ShopPage;
