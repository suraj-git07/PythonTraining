# ToDoNow : Task Management Application

A web-based task management application built with Flask, supporting user authentication, task CRUD operations, and due date tracking.

---

## Features

- **User Registration & Login**: Secure authentication using Flask-Login. Passwords are hashed.
- **Task Management**:
  - Add, edit, and delete tasks
  - Set task title, description, due date, and status
  - Status cycle: `pending` → `working` → `done` → `pending`
  - Mark tasks as done or working
  - Clear all tasks
- **Task Views**:
  - View all your tasks, sorted by most recent
  - Visual priority indicators (overdue, due today, due soon, normal)
- **Responsive UI**: Modern interface using HTML, CSS, and JavaScript
- **Persistent Storage**: Uses SQLite database

---

## Project Structure

```
Advance_Python_Assignment/
│
├── run.py                  # App entry point
├── requirements.txt        # Python dependencies
├── README.MD               # Project documentation
│
├── app/
│   ├── __init__.py         # Flask app factory
│   ├── models.py           # SQLAlchemy models (User, Task)
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py         # Auth routes (login, register, logout)
│   │   └── tasks.py        # Task CRUD routes
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css   # Styles
│   │   └── js/
│   │       └── task-dropdown.js # JavaScript for task dropdowns
│   └── templates/
│       ├── base.html
│       ├── login.html
│       ├── register.html
│       ├── tasks.html
│       └── edit_task.html
│
├── instance/
│   └── todo.db             # SQLite database
```

---

## Database Schema

### User Table
| Field        | Type           | Description                |
|--------------|----------------|----------------------------|
| id           | Integer (PK)   | User ID                    |
| username     | String(80)     | Unique username            |
| email        | String(120)    | Unique email               |
| password_hash| String(255)    | Hashed password            |
| created_at   | DateTime       | Registration timestamp     |

### Task Table
| Field        | Type           | Description                |
|--------------|----------------|----------------------------|
| id           | Integer (PK)   | Task ID                    |
| title        | String(200)    | Task title                 |
| description  | Text           | Task description           |
| status       | String(20)     | Task status                |
| due_date     | Date           | Due date (optional)        |
| created_at   | DateTime       | Creation timestamp         |
| updated_at   | DateTime       | Last update timestamp      |
| user_id      | Integer (FK)   | Linked user (User.id)      |

---

## Getting Started

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Run the app**:
   ```bash
   python run.py
   ```
3. **Access in browser**: [http://localhost:5000](http://localhost:5000)


