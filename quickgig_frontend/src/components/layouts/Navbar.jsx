import { Link, Outlet, useNavigate } from 'react-router-dom';
import { Menu, X } from 'lucide-react';
import { useState } from 'react';
import Button from '../common/Button';
import useAuthStore from "../../stores/authstore";

const Navbar = () => {
    const user = useAuthStore((state) => state.user);
    const logout = useAuthStore((state) => state.logout);
    const navigate = useNavigate();
    const [isMenuOpen, setIsMenuOpen] = useState(false);

    const handleLogout = async () => {
        await logout();
        navigate("/");
    };

    const handleLogin = () => {
        navigate("/login");
    };

    const NavLinks = [
        { name: "Home", path: "/" },
        { name: "Services", path: "/services" },
        { name: "About", path: "/about" },
        { name: "Contact", path: "/contact" },
        ...(user ? [{name: "Dashboard", path: "/dashboard"}] : []),
    ];

    return (
        <>
            <nav className="flex justify-between py-[1.5rem] px-[1.5rem] shadow-md sticky top-0 bg-white z-50">
                {/* Mobile menu button */}
                <button className="md:hidden" onClick={() => setIsMenuOpen(!isMenuOpen)}>
                    {isMenuOpen ? <X /> : <Menu />}
                </button>

                <p className="font-header text-primary text-3xl">QuickGig</p>
                <ul className="hidden md:flex gap-[1.5rem] items-center">
                    {NavLinks.map((link) => (
                        <li key={link.name}>
                            <Link to={link.path} className="font-body hover:text-secondary">
                                {link.name}
                            </Link>
                        </li>
                    ))}
                </ul>
                {user ? (
                    <>
                        <Button className="hidden md:block" variant="secondary" onClick={handleLogout}>
                            Sign Out
                        </Button>
                    </>
                ) : (
                    <Button className="hidden md:block" variant="primary" onClick={handleLogin}>
                        Sign In
                    </Button>
                )}

                {/* Mobile menu */}
                <div className={`fixed top-0 left-0 h-full w-2/3 bg-white shadow-lg z-10 transition-transform duration-300 ease-in ${isMenuOpen ? 'translate-x-0' : '-translate-x-full'} md:hidden`}>
                    <ul className="flex flex-col gap-6 mt-9 ml-6">
                        <button className="md:hidden" onClick={() => setIsMenuOpen(!isMenuOpen)}>{isMenuOpen ? <X /> : <Menu />}</button>
                        {NavLinks.map((link) => (
                            <li key={link.name}>
                                <Link to={link.path} className="font-body hover:text-secondary" onClick={() => setIsMenuOpen(false)}>
                                    {link.name}
                                </Link>
                            </li>
                        ))}
                    </ul>
                </div>
            </nav>
            <Outlet />
        </>
    )
}

export default Navbar;