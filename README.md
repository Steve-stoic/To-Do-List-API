# To Do List API

This is a simple To Do List application programming interface (API) built with Flask and SQLAlchemy. You can use this API to create, retrieve, update, and delete tasks in your to-do list.

## Features

1. Create new tasks with descriptions, priorities (optional), and due dates (optional).
2. Retrieve all tasks, specific tasks by ID, completed tasks, and uncompleted tasks.
3. Update existing tasks by modifying their description, completion status, priority, or due date.
4. Delete tasks by ID.

## Installation

1. Clone the repository: 

```console
git clone (https://github.com/Steve-stoic/To-Do-List-API.git)
```

2. Install the required dependencies:
 
```console
pip install -r requirements.txt
```


3. Create a .env file in the project root directory with the following environment variables:
   ```
   	DB_USERNAME=your_username
	DB_PASSWORD=your_password
	DB_HOST=your_database_host
	DB_PORT=your_database_port
	DB_NAME=your_database_name
	SECRET_KEY=your_secret_key
   ```

4. Replace the placeholder values with your actual database credentials and a secret key.

## Running the API
1. Start the development server
2. The API will be running on http://localhost:5000 (default port).
   
**API Endpoints**

| Method | URL | Description | Status Code |
|---|---|---|---|
| POST | `/tasks` | Creates a new task | 201 Created |
| GET | `/tasks` | Retrieves all tasks | 200 OK |
| GET | `/tasks/<int:task_id>` | Retrieves a specific task by ID | 200 OK (or 404 Not Found) |
| GET | `/tasks/completed` | Retrieves all completed tasks. | 200 OK |
| GET | `/tasks/uncompleted` | Retrieves all uncompleted tasks | 200 OK |
| PUT | `/tasks/<int:task_id>` | Updates a specific task by ID | 200 OK (or 404 Not Found) |

### Example Usage

(Assuming you are using a tool like Postman)

#### * Create a new task:

**Input**

```json
POST http://localhost:5000/tasks

Content-Type: application/json

{
  "description": "Buy groceries",
  "due_date": "25-05-2024 10:00:00"
}
```

**Response**

```json
{
  "message": "Task for to do list created sucessfully"
}
```
#### * Retrieve all tasks:

**Input:**

GET http://localhost:5000/tasks

**Response**
```json
[
  {
    "id": 1,
    "description": "Buy groceries",
    "completed": false,
    "priority": null,
    "due_date": "25-05-2024 10:00:00"
  }
]
```

**Note:**
1. The *completed* section accepts the boolean *true* for completed and *false* for uncompleted
2. The data type of *task_id* is integer

