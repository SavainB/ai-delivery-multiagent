export default function TaskList({ tasks, onSelect }) {
  return (
    <div>
      <h2>Task dashboard</h2>
      <ul className="task-list">
        {tasks.map((task) => (
          <li key={task.id}>
            <button className="task-card" onClick={() => onSelect(task)}>
              <strong>{task.title}</strong>
              <span>{task.status}</span>
              <span>{task.priority}</span>
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
