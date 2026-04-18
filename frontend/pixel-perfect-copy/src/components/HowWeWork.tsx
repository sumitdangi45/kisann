import img_ylH1TySsTue8MjCcWn0lFAjBcI_jpg from "../assets/external/ylH1TySsTue8MjCcWn0lFAjBcI.jpg";
const steps = [
  { num: "01", title: "Schedule Your Experience", desc: "Enrich soil with nutrients for healthy crop growth." },
  { num: "02", title: "Get Professional Advice", desc: "Carefully sow seeds to ensure optimal growth." },
  { num: "03", title: "Meet Our Expert Farmer", desc: "Monitor and care for crops with sustainable practices." },
  { num: "04", title: "Now Get a Best Products", desc: "Harvest at peak freshness and deliver straight to you." },
];

const HowWeWork = () => {
  return (
    <section className="py-20 bg-eco-cream">
      <div className="max-w-7xl mx-auto px-6 lg:px-16">
        <div className="text-center mb-4">
          <span className="text-eco-green font-semibold text-sm uppercase tracking-widest">Our Working Step</span>
          <h2 className="font-heading text-3xl md:text-5xl font-bold text-foreground mt-3">
            How We Do Agricultural Work
          </h2>
          <p className="text-muted-foreground max-w-2xl mx-auto mt-4 text-sm">
            The modern consumer demands, quality organic products which is why our selection of farm-grown herbs are top quality, always fresh, and 100% organic certified.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 mt-12 items-center">
          {/* Image */}
          <div className="rounded-3xl overflow-hidden">
            <img
              src={img_ylH1TySsTue8MjCcWn0lFAjBcI_jpg}
              alt="Working"
              className="w-full h-[450px] object-cover rounded-3xl"
            />
          </div>

          {/* Steps */}
          <div className="space-y-8">
            {steps.map((step, i) => (
              <div key={i} className="flex gap-6 items-start">
                <span className="font-heading text-5xl font-bold text-eco-green/20">{step.num}</span>
                <div>
                  <h5 className="font-heading text-lg font-bold text-foreground">{step.title}</h5>
                  <p className="text-muted-foreground text-sm mt-1">{step.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default HowWeWork;
