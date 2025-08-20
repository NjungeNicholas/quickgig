const HowItWorks = () => {
    // This component explains how the service works

    return (
        <div className="how-it-works py-10">
            <h2 className="font-header text-text text-center text-4xl">How It Works</h2>
            <ul className="text-center text-lg text-gray-800 mt-8 space-y-3 ">
                <li ><strong>Browse Services</strong>– Explore categories or search</li>
                <li><strong>Choose a Tasker</strong>– Compare profiles, ratings</li>
                <li><strong>Get the job Done</strong>– Sit back and relax while your task is completed.</li>
            </ul>
        </div>
    );
}

export default HowItWorks;
