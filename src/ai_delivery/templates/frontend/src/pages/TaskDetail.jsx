export default function TaskDetail({ task }) {
  if (!task) {
    return <p>Select a task to inspect its detail view.</p>;
  }

  return (
    <article>
      <h2>Task detail</h2>
      <p><strong>{task.title}</strong></p>
      <p>{task.description}</p>
      <p>Status: {task.status}</p>
      <p>Priority: {task.priority}</p>
      <p>Due date: {task.due_date}</p>
    </article>
  );
}
