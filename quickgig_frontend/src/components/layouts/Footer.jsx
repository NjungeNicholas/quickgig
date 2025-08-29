import { Link } from 'react-router-dom'
const Footer = () => {
    // This component renders the footer of the application
    const quickLinks = [
        { label: "About Us", url: "/about" },
        { label: "Contact", url: "/contact" },
        { label: "Privacy Policy", url: "/privacy" },
        { label: "Terms of Service", url: "/terms" },
    ];
    return (
        <footer className="bg-gray-800 font-body text-white py-4 mt-6 fixed bottom-0 w-full">
            <div className="flex flex-wrap justify-between items-center mx-auto container">
                <p>&copy; {new Date().getFullYear()} QuickGig. All rights reserved.</p>
                <ul className="flex  justify-center text-center space-x-4 mt-2">
                    {quickLinks.map((link) => (
                        <li key={link.label}>
                            <Link to={link.url} className="hover:underline">
                                {link.label}
                            </Link>
                        </li>
                    ))}
                </ul>
            </div>
        </footer>
    );
}

export default Footer;
