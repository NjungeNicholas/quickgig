// src/pages/Services.jsx
import { useEffect, useState } from "react";
import useServiceStore from "../stores/serviceStore";
import TaskerCard from "../components/common/TaskerCard";

export default function Services() {
  const { services, taskers, fetchServices, fetchTaskers } =
    useServiceStore();
  const [selectedService, setSelectedService] = useState(null);

  useEffect(() => {
    fetchServices();
  }, [fetchServices]);

  const handleSelectService = (id) => {
    setSelectedService(id);
    fetchTaskers(id);
  };

  return (
    <div className="m-2 mb-19 p-6 flex flex-col justify-between md:flex-row md:gap-4">
      <div className="mb-6">
        <label htmlFor="service-select" className=" block mb-2 font-medium">
          Select a Service:
        </label>
        <select
          id="service-select"
          placeholder="Select a Service"
          value={selectedService || ""}
          onChange={(e) => handleSelectService(Number(e.target.value))}
          className="p-3 rounded-lg border bg-gray-100 hover:bg-gray-200 w-full "
        >
          <option value="" disabled>
            -- Choose a service --
          </option>
          {services.map((service) => (
            <option key={service.id} value={service.id}>
              {service.name}
            </option>
          ))}
        </select>
      </div>
      {selectedService && (
        <div className="justify-start md:w-2/3">
          <h3 className="text-2xl font-semibold mb-4">
            Taskers for {services.find((s) => s.id === selectedService)?.name}
          </h3>
          {taskers.length === 0 ? (
            <p>No taskers available for this service.</p>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-1 gap-4 ">
              {taskers.map((tasker) => (
                <div
                  key={tasker.id}
                  className="p-4 border rounded-lg shadow-sm bg-white"
                >
                  <TaskerCard
                    tasker={tasker}
                    task={selectedService}
                    taskData={services.find((s) => s.id === selectedService)}
                  />
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}