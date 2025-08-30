import { useEffect } from "react";
import useDashboardStore from "../stores/dashboardStore";
import Button from "../components/common/Button";

export default function Dashboard() {
  const { 
    tasks, 
    mode, 
    loading, 
    error, 
    setMode, 
    fetchTasks 
  } = useDashboardStore();
  
  const userId = JSON.parse(localStorage.getItem("user"))?.id;
  const isClient = JSON.parse(localStorage.getItem("user"))?.is_client;
  const isTasker = JSON.parse(localStorage.getItem("user"))?.is_tasker;

  useEffect(() => {
    if (!userId) return;
    fetchTasks();
  }, [userId, fetchTasks]);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold font-header mb-4">Dashboard</h1>

      <div className="mb-6 flex gap-4">
        {isClient && (
          <Button
            className={`px-4 py-2 rounded font-body ${mode === "client" ? "bg-secondary text-white" : "bg-gray-200"}`}
            onClick={() => setMode("client")}
            disabled={loading}
          >
            Client Mode
          </Button>
        )}
        {isTasker && (
          <Button
            className={`px-4 py-2 rounded font-body ${mode === "tasker" ? "bg-secondary text-white" : "bg-gray-200"}`}
            onClick={() => setMode("tasker")}
            disabled={loading}
          >
            Tasker Mode
          </Button>
        )}
      </div>

      <h2 className="text-xl mb-2 font-header">
        {mode === "client" ? "Your Created Tasks" : "Tasks Assigned to You"}
      </h2>

      {loading && (
        <div className="flex items-center justify-center p-8">
          <p className="text-gray-600">Loading tasks...</p>
        </div>
      )}

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          <p>{typeof error === 'string' ? error : 'Failed to load tasks'}</p>
        </div>
      )}

      {!loading && !error && tasks.length === 0 ? (
        <p>No tasks found</p>
      ) : !loading && !error ? (
        <ul className="space-y-4">
          {tasks.map((task) => (
            <li key={task.id} className="p-4 border rounded shadow font-body">
              <p><strong>Tasker:</strong> {task.tasker_name}</p>
              <p><strong>Service:</strong> {task.task_name}</p>
              <p><strong>Time:</strong> {task.slot_detail.date} | {task.slot_detail.start_time} - {task.slot_detail.end_time}</p>
              <p><strong>Status:</strong> {task.status}</p>
              <p><strong>Description:</strong> {task.description}</p>
            </li>
          ))}
        </ul>
      ) : null}
    </div>
  );
}
