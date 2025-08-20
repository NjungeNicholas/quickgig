import FilterServices from "../components/servicespage/FilterServices";
function Services() {
    return (
        <div>
            <h1 className="font-header text-primary text-4xl mb-4 mt-10 text-center">Our Services</h1>
            <p className="text-gray-500 font-body text-center text-2xl">We offer a variety of services to help you succeed.</p>
            <FilterServices />
        </div>
    );
}

export default Services;
