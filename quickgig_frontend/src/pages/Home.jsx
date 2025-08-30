import CategoryPreview from "../components/homepage/CategoryPreview";
import HeroSection from "../components/homepage/HeroSection";
import HowItWorks from "../components/homepage/HowItWorks";

function Home() {
  return (
    <div className="mb-20">
      <HeroSection />
      <CategoryPreview />
      <HowItWorks />
    </div>
  );
}

export default Home;
