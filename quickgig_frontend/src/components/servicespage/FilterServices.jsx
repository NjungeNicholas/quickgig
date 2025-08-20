import { useState } from "react";

const FilterServices = () => {
    // State variables to hold selected category and service
    const [selectedCategory, setSelectedCategory] = useState("");
    const [selectedService, setSelectedService] = useState("");

    return (
        <div className="flex md:flex-row flex-col gap-3 m-5 mb-20">
            <div className="border p-10 rounded">
                <h2 className="font-header text-2xl mb-4">Services</h2>
                <div className="flex flex-col gap-2 mb-4">
                    <label className="font-header text-lg">Category</label>
                    <select
                        className="border p-2 rounded font-body"
                        value={selectedCategory}
                        onChange={(e) => setSelectedCategory(e.target.value)}
                    >
                        <option value="">Select Category</option>
                    </select>
                </div>
                <div className="flex flex-col gap-2 mb-4">
                    <label className="font-header text-lg">Service</label>
                    <select
                        className="border p-2 rounded font-body"
                        value={selectedService}
                        onChange={(e) => setSelectedService(e.target.value)}
                    >
                        <option value="">Select Service</option>
                    </select>
                </div>
            </div>
            <div className="ml-5 mr-5">
                <h2 className="font-header text-2xl mb-4">Taskers</h2>
                <p className="text-gray-500">Taskers will be displayed here based on the selected service.</p>
                {/* Placeholder for taskers list */}
            </div>
        </div>
    )
}

export default FilterServices;