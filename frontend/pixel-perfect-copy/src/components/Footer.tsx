import img_TfVsdEorI3M6CtwPPcnMUstJ5Q_png from "../assets/external/TfVsdEorI3M6CtwPPcnMUstJ5Q.png";
import img_IaiXPcjhnjzr1iVhFOtYldWJlAw_svg from "../assets/external/IaiXPcjhnjzr1iVhFOtYldWJlAw.svg";
import img_FkkZQ21lbczJIWxigYbEQD75uI_svg from "../assets/external/FkkZQ21lbczJIWxigYbEQD75uI.svg";
import img_aGyF36iTVtlRHvmLXOHcT54MK3I_svg from "../assets/external/aGyF36iTVtlRHvmLXOHcT54MK3I.svg";
import img_img_4rNEIMZl5loHoK9yMLJIIMimC4_svg from "../assets/external/4rNEIMZl5loHoK9yMLJIIMimC4.svg";
const Footer = () => {
  return (
    <footer id="contact">
      {/* Yellow Contact Band */}
      <div className="relative bg-eco-yellow py-12 overflow-hidden">
        <img
          src={img_TfVsdEorI3M6CtwPPcnMUstJ5Q_png}
          alt=""
          className="absolute inset-0 w-full h-full object-cover opacity-20 pointer-events-none"
        />
        <div className="relative z-10 max-w-7xl mx-auto px-6 lg:px-16 grid grid-cols-1 md:grid-cols-3 gap-10">
          {/* Phone */}
          <div className="flex items-start gap-4">
            <div className="w-14 h-14 rounded-full bg-eco-green flex items-center justify-center flex-shrink-0">
              <img src={img_IaiXPcjhnjzr1iVhFOtYldWJlAw_svg} alt="Phone" className="w-6 h-6" />
            </div>
            <div>
              <h4 className="font-heading text-lg font-bold text-eco-green-dark">Phone No:</h4>
              <a href="tel:+123456789963" className="text-eco-green font-medium text-sm">+123 456 789 963</a>
              <p className="text-eco-green-dark/60 text-xs mt-1">Mon - Sat : 09.00 to 06.00</p>
            </div>
          </div>

          {/* Email */}
          <div className="flex items-start gap-4">
            <div className="w-14 h-14 rounded-full bg-eco-green flex items-center justify-center flex-shrink-0">
              <img src={img_FkkZQ21lbczJIWxigYbEQD75uI_svg} alt="Email" className="w-6 h-6" />
            </div>
            <div>
              <h4 className="font-heading text-lg font-bold text-eco-green-dark">Email Address:</h4>
              <a href="mailto:framerdevs.official@gmail.com" className="text-eco-green font-medium text-sm block">framerdevs.official@gmail.com</a>
              <a href="mailto:help.framerDevs@mail.com" className="text-eco-green font-medium text-sm block">help.framerDevs@mail.com</a>
            </div>
          </div>

          {/* Location */}
          <div className="flex items-start gap-4">
            <div className="w-14 h-14 rounded-full bg-eco-green flex items-center justify-center flex-shrink-0">
              <img src={img_aGyF36iTVtlRHvmLXOHcT54MK3I_svg} alt="Location" className="w-6 h-6" />
            </div>
            <div>
              <h4 className="font-heading text-lg font-bold text-eco-green-dark">Location:</h4>
              <a
                href="https://maps.google.com/?q=59+E+Madison+St,+Baltimore,+MD+21202,+USA"
                target="_blank"
                rel="noopener noreferrer"
                className="text-eco-green font-medium text-sm"
              >
                No: 59 A East Madison Street Baltimore, MD, USA, 4508
              </a>
            </div>
          </div>
        </div>
      </div>

      {/* Dark Green Footer */}
      <div className="bg-eco-green-dark py-16">
        <div className="max-w-7xl mx-auto px-6 lg:px-16">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-10">
            {/* Logo & Description */}
            <div>
              <a href="/" className="flex items-center gap-2 mb-4">
                <img
                  src={img_img_4rNEIMZl5loHoK9yMLJIIMimC4_svg}
                  alt="Ecoland"
                  className="h-10 w-10"
                />
                <span className="text-primary-foreground font-heading text-2xl font-bold">Ecoland</span>
              </a>
              <p className="text-primary-foreground/60 text-sm leading-relaxed mb-6">
                Enjoy the freshest fruits, vegetables, and more, cultivated with sustainable practices.
              </p>
              <div className="flex gap-3">
                {["facebook", "threads", "twitter", "linkedin"].map((social) => (
                  <a
                    key={social}
                    href="#"
                    className="w-8 h-8 rounded-full border border-primary-foreground/20 flex items-center justify-center text-primary-foreground/60 hover:text-eco-yellow hover:border-eco-yellow transition-colors text-xs"
                  >
                    {social[0].toUpperCase()}
                  </a>
                ))}
              </div>
            </div>

            {/* Useful Info */}
            <div>
              <h4 className="font-heading text-lg font-bold text-primary-foreground mb-6">Useful Info</h4>
              <ul className="space-y-3">
                {["Blog", "Projects", "404"].map((item) => (
                  <li key={item}>
                    <a href="#" className="text-primary-foreground/60 text-sm hover:text-eco-yellow transition-colors">{item}</a>
                  </li>
                ))}
              </ul>
            </div>

            {/* Explore More */}
            <div>
              <h4 className="font-heading text-lg font-bold text-primary-foreground mb-6">Explore More</h4>
              <ul className="space-y-3">
                {["Services", "Shop", "Contact"].map((item) => (
                  <li key={item}>
                    <a href="#" className="text-primary-foreground/60 text-sm hover:text-eco-yellow transition-colors">{item}</a>
                  </li>
                ))}
              </ul>
            </div>

            {/* Subscribe Newsletter */}
            <div>
              <h4 className="font-heading text-lg font-bold text-primary-foreground mb-6">Subscribe Newsletter</h4>
              <p className="text-primary-foreground/60 text-sm mb-4">Sign up to get updates & news.</p>
              <div className="mb-4">
                <input
                  type="email"
                  placeholder="Email Address"
                  className="w-full bg-primary-foreground/5 border border-primary-foreground/10 rounded-xl px-4 py-3 text-primary-foreground text-sm placeholder:text-primary-foreground/30 focus:outline-none focus:border-eco-yellow"
                />
              </div>
              <button className="w-full flex items-center justify-center gap-2 bg-eco-yellow text-eco-green-dark font-semibold px-6 py-3 rounded-full text-sm hover:brightness-110 transition-all">
                Subscribe Now
                <span className="bg-eco-green-dark text-eco-yellow rounded-full w-5 h-5 flex items-center justify-center text-xs">→</span>
              </button>
            </div>
          </div>

          <div className="border-t border-eco-green-light/20 mt-12 pt-8 flex flex-col md:flex-row items-center justify-between gap-4">
            <p className="text-primary-foreground/40 text-sm">© 2024 All Right Reserved by <a href="#" className="text-primary-foreground/60 hover:text-eco-yellow">FramerDevs</a></p>
            <div className="flex gap-6">
              <a href="#" className="text-primary-foreground/40 text-sm hover:text-eco-yellow transition-colors">Privacy Policy</a>
              <span className="text-primary-foreground/20">|</span>
              <a href="#" className="text-primary-foreground/40 text-sm hover:text-eco-yellow transition-colors">Terms of Use</a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
