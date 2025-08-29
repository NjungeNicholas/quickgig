import { Routes, Route, useLocation } from "react-router-dom";
import Navbar from "./components/layouts/Navbar";
import Footer from "./components/layouts/Footer";
import Home from "./pages/Home";
import Services from "./pages/Services";
import About from "./pages/About";
import Contact from "./pages/Contact";
import PrivacyPolicy from "./pages/PrivacyPolicy";
import TermsOfService from "./pages/TermsOfService";
import Register from "./pages/Register";
import Login from "./pages/Login";

function Layout() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route index element={<Home />} />
        <Route path="/services" element={<Services />} />
        <Route path="/about" element={<About />} />
        <Route path="/contact" element={<Contact />} />
        <Route path="/privacy" element={<PrivacyPolicy />} />
        <Route path="/terms" element={<TermsOfService />} />
        <Route path="*" element={<h1 className="text-center text-2xl mt-20">Page Not Found</h1>} />
      </Routes>
    </>
  );
}

function App() {
  const location = useLocation();
  const hideFooter = ["/register", "/login"].includes(location.pathname);

  return (
    <>
      <Routes>
        <Route path="/*" element={<Layout />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
      </Routes>
      {!hideFooter && <Footer />}
    </>
  );
}

export default App;
