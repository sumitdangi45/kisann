import { useState } from "react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { Download, X, Eye } from "lucide-react";

const resources = [
  {
    title: "Jaivik Kheti (Organic Farming)",
    category: "Soil & Fertilizer",
    description: "Complete guide to organic farming practices and composting methods.",
    pages: 48,
    icon: "📖",
    pdfFile: "Jaivik kheti.pdf",
    paid: false,
    background: "https://cdn.pixabay.com/photo/2016/09/21/04/46/barley-field-1684052_1280.jpg"
  },
  {
    title: "Phal-Phool (Fruits & Flowers)",
    category: "Crop Management",
    description: "Guide to fruit and flower cultivation with seasonal planning.",
    pages: 56,
    icon: "📖",
    pdfFile: "Phal-Phool-Sept-Oct 2020.pdf",
    paid: false,
    background: "https://cdn.pixabay.com/photo/2016/09/21/04/46/barley-field-1684052_1280.jpg"
  },
  {
    title: "Sabji (Vegetable Farming)",
    category: "Crop Management",
    description: "Complete resource for growing vegetables with seasonal planning.",
    pages: 56,
    icon: "📖",
    pdfFile: "SABJIX16Xpage.pdf",
    paid: false,
    background: "https://cdn.pixabay.com/photo/2016/09/21/04/46/barley-field-1684052_1280.jpg"
  },
  {
    title: "Unnat Krishi (Advanced Farming)",
    category: "Weather & Water",
    description: "Guide to advanced irrigation and water management techniques.",
    pages: 46,
    icon: "📖",
    pdfFile: "Unnat Krishi, January - March, 2022 issue_2_0.pdf",
    paid: false,
    background: "https://cdn.pixabay.com/photo/2016/09/21/04/46/barley-field-1684052_1280.jpg"
  }
];

const ResourcesPage = () => {
  const [selectedIndex, setSelectedIndex] = useState<number | null>(null);
  const selectedResource = selectedIndex !== null ? resources[selectedIndex] : null;

  const downloadPDF = (resource: typeof resources[0]) => {
    if (resource.pdfFile) {
      const link = document.createElement('a');
      const encodedFileName = encodeURIComponent(resource.pdfFile);
      link.href = `/pdfs/${encodedFileName}`;
      link.download = resource.pdfFile;
      link.target = '_blank';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };

  return (
    <div className="min-h-screen">
      <Navbar />

      {/* Hero Banner */}
      <section className="relative h-[400px] md:h-[480px] flex items-center">
        <img
          src="https://cdn.pixabay.com/photo/2016/09/21/04/46/barley-field-1684052_1280.jpg"
          alt="Resources Hero"
          className="absolute inset-0 w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-black/40" />
        <div className="relative z-10 max-w-7xl mx-auto px-6 lg:px-16 w-full">
          <h1 className="font-heading text-5xl md:text-7xl font-bold text-primary-foreground mb-4">
            📚 Learning Resources
          </h1>
          <p className="text-primary-foreground/80 text-lg md:text-xl max-w-lg">
            Comprehensive guides and educational materials for modern farming
          </p>
        </div>
      </section>

      {/* Resources Grid */}
      <section className="py-16 md:py-24 bg-white">
        <div className="max-w-7xl mx-auto px-6 lg:px-16">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {resources.map((resource, index) => (
              <div key={index} className="group">
                {/* Background Image Card */}
                <div 
                  className="relative h-64 rounded-2xl overflow-hidden hover:shadow-xl transition-shadow"
                  style={{
                    backgroundImage: `url(${resource.background})`,
                    backgroundSize: 'cover',
                    backgroundPosition: 'center'
                  }}
                >
                  <div className="absolute inset-0 bg-black/40 group-hover:bg-black/50 transition-all" />
                  <div className="absolute inset-0 flex flex-col justify-between p-6">
                    <div>
                      <h3 className="font-heading text-2xl font-bold text-white mb-2">
                        {resource.title}
                      </h3>
                      <p className="text-white/90 text-sm">{resource.category}</p>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-white text-sm">📄 {resource.pages} pages</span>
                      <span className="bg-green-500 text-white text-xs px-3 py-1 rounded-full font-bold">
                        🟢 Free
                      </span>
                    </div>
                  </div>
                </div>

                {/* Description and Buttons */}
                <div className="mt-4">
                  <p className="text-muted-foreground text-sm mb-4">
                    {resource.description}
                  </p>
                  <div className="flex gap-3">
                    <button 
                      onClick={() => setSelectedIndex(index)}
                      className="flex-1 inline-flex items-center justify-center gap-2 bg-gradient-to-r from-blue-600 to-teal-600 text-white px-4 py-2 rounded-lg font-semibold text-sm hover:brightness-110 transition-all"
                    >
                      <Eye className="w-4 h-4" />
                      Read
                    </button>
                    <button 
                      onClick={() => downloadPDF(resource)}
                      className="flex-1 inline-flex items-center justify-center gap-2 bg-gray-200 text-gray-700 px-4 py-2 rounded-lg font-semibold text-sm hover:bg-gray-300 transition-all"
                    >
                      <Download className="w-4 h-4" />
                      Download
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Modal - PDF Preview */}
      {selectedResource && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col">
            {/* Header */}
            <div className="bg-gradient-to-r from-blue-600 to-teal-600 text-white p-6 flex justify-between items-start">
              <div>
                <h2 className="text-2xl font-bold">{selectedResource.title}</h2>
                <p className="text-white/80 text-sm mt-1">{selectedResource.category} • {selectedResource.pages} pages</p>
              </div>
              <button
                onClick={() => setSelectedIndex(null)}
                className="text-white hover:bg-white/20 p-2 rounded-lg transition"
              >
                <X className="w-6 h-6" />
              </button>
            </div>

            {/* PDF Viewer */}
            <div className="flex-1 overflow-auto bg-gray-100 p-6">
              <div className="bg-white rounded-lg shadow-lg overflow-hidden">
                {selectedResource.pdfFile ? (
                  <iframe
                    src={`/pdfs/${encodeURIComponent(selectedResource.pdfFile)}`}
                    className="w-full h-full"
                    style={{ minHeight: '500px' }}
                    title={selectedResource.title}
                  />
                ) : (
                  <div className="p-6 text-center text-gray-500">
                    No PDF available
                  </div>
                )}
              </div>
            </div>

            {/* Footer */}
            <div className="border-t p-4 flex gap-3 justify-end bg-gray-50">
              <button
                onClick={() => setSelectedIndex(null)}
                className="px-6 py-2 bg-gray-200 text-gray-700 rounded-lg font-semibold hover:bg-gray-300 transition"
              >
                Close
              </button>
              <button 
                onClick={() => downloadPDF(selectedResource)}
                className="inline-flex items-center gap-2 bg-gradient-to-r from-blue-600 to-teal-600 text-white px-6 py-2 rounded-lg font-semibold hover:brightness-110 transition-all"
              >
                <Download className="w-4 h-4" />
                Download PDF
              </button>
            </div>
          </div>
        </div>
      )}

      <Footer />
    </div>
  );
};

export default ResourcesPage;
