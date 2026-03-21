import { useState } from "react";

const emptyTask = {
  title: "",
  description: "",
  priority: "medium",
  status: "todo",
  due_date: "2026-04-05"
};

export default function TaskForm({ onSubmit }) {
  const [task, setTask] = useState(emptyTask);

  const update = (event) => {
    setTask((current) => ({ ...current, [event.target.name]: event.target.value }));
  };

  const submit = (event) => {
    event.preventDefault();
    onSubmit(task);
    setTask(emptyTask);
  };

  return (
    <form className="task-form" onSubmit={submit}>
      <h2>Create task</h2>
      <input name="title" placeholder="Title" value={task.title} onChange={update} required />
      <textarea name="description" placeholder="Description" value={task.description} onChange={update} required />
      <select name="priority" value={task.priority} onChange={update}>
        <option value="high">High</option>
        <option value="medium">Medium</option>
        <option value="low">Low</option>
      </select>
      <select name="status" value={task.status} onChange={update}>
        <option value="todo">To do</option>
        <option value="in_progress">In progress</option>
        <option value="done">Done</option>
      </select>
      <input name="due_date" type="date" value={task.due_date} onChange={update} />
      <button type="submit">Add task</button>
    </form>
  );
}
