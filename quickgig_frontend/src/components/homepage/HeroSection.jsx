import { Link } from 'react-router-dom';
import Button from '../common/Button';
const HeroSection = () => {
    return (
        <div className="mt-10 text-center justify-center">
            <h1 className="font-header text-text font-bold text-6xl">Find Trusted Taskers for Any Service</h1>
            <h2 className="font-body text-secondary text-3xl mt-5">Hire skilled professionals near you at fixed prices.</h2>
            <div className=' flex gap-4 p-4 justify-center mt-7'>
                <Link to="/services">
                    <Button variant="primary">Find Services</Button>
                </Link>
                <Link to="/become-tasker">
                    <Button variant="primary">Become a tasker</Button>
                </Link>
            </div>
        </div>
    );
}

export default HeroSection;
