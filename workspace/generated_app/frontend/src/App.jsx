import { useEffect, useState } from "react";
import TaskList from "./components/TaskList.jsx";
import TaskForm from "./components/TaskForm.jsx";
import TaskDetail from "./pages/TaskDetail.jsx";

const initialTasks = [
  {
    id: 1,
    title: "Kickoff demo",
    description: "Prepare generated task dashboard",
    priority: "high",
    status: "todo",
    due_date: "2026-04-01"
  }
];

export default function App() {
  const [tasks, setTasks] = useState(initialTasks);
  const [selectedTask, setSelectedTask] = useState(initialTasks[0]);

  useEffect(() => {
    setSelectedTask(tasks[0] || null);
  }, [tasks]);

  const addTask = (task) => {
    const next = { ...task, id: Date.now() };
    setTasks((current) => [next, ...current]);
  };

  return (
    <main className="app-shell">
      <section className="hero">
        <p className="eyebrow">DeliveryFlow</p>
        <h1>DeliveryFlow Tasks</h1>
        <p className="lede">
          Generated workspace for Demo Client with configurable branding and a focused task flow.
        </p>
      </section>
      <section className="grid">
        <div className="panel">
          <TaskForm onSubmit={addTask} />
        </div>
        <div className="panel">
          <TaskList tasks={tasks} onSelect={setSelectedTask} />
        </div>
        <div className="panel">
          <TaskDetail task={selectedTask} />
        </div>
      </section>
    </main>
  );
}
