import { useState } from 'react';
import BookingModal from '../layouts/BookingModal';
import useAuthStore from '../../stores/authstore';
import { useNavigate } from 'react-router-dom'

export default function TaskerCard({ tasker, task, taskData }) {

    const [showModal, setShowModal] = useState(false);
    const { user } = useAuthStore();
    const navigate = useNavigate();

    const handleBook = () => {
        if (!user) {
            navigate("/login");
            return;
        }
        setShowModal(true);
    };

    return (
        <div className="p-4 flex gap-10 bg-white">
            <div>
                <img
                    src={tasker.user.profile_picture}
                    alt={tasker.user.username}
                    className="w-30 h-30 rounded-full object-cover m-2"
                />
                <button
                    onClick={handleBook}
                    className="mt-4 w-full bg-secondary font-body text-white py-2 p-2 rounded-lg hover:bg-primary"
                >
                    Book Now
                </button>
                {showModal && (
                    <BookingModal
                        tasker={tasker}
                        task={task}
                        taskData={taskData}
                        onClose={() => setShowModal(false)}
                    />
                )}
            </div>
            <div>
                <h3 className="text-lg font-header font-semibold mt-3">{tasker.user.username}</h3>
                <div className="mt-3">
                    <h4 className="text-sm  font-header font-semibold mt-2">Skills / Services:</h4>
                    <ul className="flex flex-wrap gap-2 mt-2">
                        {tasker.skills.map((skill, idx) => (
                            <li
                                key={idx}
                                className="px-2 py-1 text-xs font-body bg-blue-100 text-blue-700 rounded-lg"
                            >
                                {skill}
                            </li>
                        ))}
                    </ul>
                    <p className="text-gray-600 font-body text-sm mt-2">{tasker.bio || "No bio available"}</p>
                </div>
            </div>
        </div>
    );
}
