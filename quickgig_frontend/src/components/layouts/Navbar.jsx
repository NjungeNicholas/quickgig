import { Link, Outlet } from 'react-router-dom';
import {useState} from 'react';
import Button from '../common/Button';


const Navbar = () => {
    const [loggedIn, setLoggedIn] = useState("Sign In");
    return (
        <>
            <nav className="flex justify-between py-[1.5rem] px-[1.5rem]">
                <p className="font-header text-primary text-3xl">QuickGig</p>
                <ul className="flex gap-[1.5rem] items-center">
                    <li><Link to={"/"} className="font-body">Home</Link></li>
                    <li><Link to={"/services"} className="font-body">Services</Link></li>
                    <li><Link to={"/about"} className="font-body">About</Link></li>
                    <li><Link to={"/contact"} className="font-body">Contact</Link></li>
                </ul>
                <Button variant={loggedIn === "Sign In" ? "primary" : "secondary"} onClick={() => setLoggedIn(loggedIn === "Sign In" ? "Sign Out" : "Sign In")}>
                    {loggedIn}
                </Button>
            </nav>
            <Outlet />
        </>
    )
}

export default Navbar;