from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv
import os

# Loads data from .env file
load_dotenv()

db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
secret_key = os.getenv('SECRET_KEY')



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_username}:{db_password}@{db_host}/{db_name}"
app.config['SECRET_KEY'] = secret_key  



db = SQLAlchemy(app)


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String, nullable = False)
    completed = db.Column(db.Boolean, default = False)
    priority = db.Column(db.String, nullable = True)
    due_date = db.Column(db.DateTime, nullable = True)



    def __repr__(self):
        return f"<Task {self.description}>"
    

#the priorities options that can used
priority_options = ['high', 'medium', 'low']    


#Creates tasks in the to do list
@app.route('/tasks', methods=['POST'])
def create_task():
    try:
        data = request.get_json()

#Error handling for no data and missing description
        if not data or not data.get('description'):
            print(len(data.get('description')))
            return jsonify({'error': 'Missing description'}), 400
        
        
#Error handling for improper due_date entry
        due_date = None
        if data.get('due_date'):
            try: 
                due_date = datetime.strptime(data['due_date'], "%d-%m-%Y %H:%M:%S")
            except ValueError:
                return jsonify({'error': 'Invalid due date format. Use DD-MM-YYYY %H:%M:%S instead '}), 400
        
#Error handling / checking for correct priority entry
        priority = data.get('priority')
    
        if priority and priority not in priority_options:
            return jsonify({'error': 'Invalid priority entry. Valid options are high, medium, low'}), 400
     

        new_task = Task(description=data['description'], due_date=due_date, priority=priority)
        db.session.add(new_task)
        db.session.commit()

        return jsonify({'message': 'Task for to do list created sucessfully',}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


#Retrieves all tasks   
@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    try:
        tasks = Task.query.order_by(Task.id).all()
        result = [ ]
        for task in tasks:
            result.append(
                {
                    'id' : task.id,
                    'description' : task.description,
                    'completed' : task.completed,
                    'priority' : task.priority if task.priority else None,
                    'due_date' : task.due_date.strftime("%d-%m_%Y %H:%M:%S") if task.due_date else None
                }
            )
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
   

#Give details of each and every Task with its task status and the due date using task id
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task_by_id(task_id):
    try:
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': 'Task not found. Enter correct id'}), 404
        
        return jsonify (
                {
                    'id' : task.id,
                    'description' : task.description,
                    'completed' : task.completed,
                    'priority' : task.priority if task.priority else None,
                    'due_date' : task.due_date.strftime("%d-%m-%Y %H:%M:%S") if task.due_date else None
                }
            )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


#Update task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task_by_id(task_id):
    try:
        data = request.get_json()

        task = Task.query.get(task_id)
        
        if not task:
            return jsonify({'error':'Task not found. Enter correct id'}), 404
        if data.get('description'):
            task.description = data['description']
        if data.get('completed') is not None:
            if not isinstance(data['completed'], bool):
                return jsonify({'error': 'Invalid entry. Completed status must be either booleans: true or false'}), 400
            task.completed = data['completed']
            
        if data.get('priority'):
            if data.get('priority') not in priority_options:
                return jsonify({'error': 'Invalid priority entry. Valid options are high, medium, low'}), 400
            else:
                task.priority = data['priority']
        if data.get('due_date'):
            try:
                due_date = datetime.strptime(data['due_date'], "%d-%m-%Y %H:%M:%S")
                task.due_date = due_date
            except ValueError:
                return jsonify({'error': 'Invalid due date format. Use DD-MM-YYYY %H:%M:%S instead '}), 400
                
        db.session.commit()
        return jsonify({'message':'Task updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

  
#Delete task using task id.
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task_by_id(task_id):
    try:
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error':'Task not found. Enter correct id'}), 404
        
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message':'Task deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


#Produce a list of all the completed tasks with their due dates
@app.route('/tasks/completed', methods=['GET'])
def completed_tasks():
    try:
        tasks = Task.query.filter_by(completed=True).all()

        completed_tasks = []
        for task in tasks:
            completed_tasks.append(
                {
                    'id' : task.id,
                    'description' : task.description,
                    'completed' : task.completed,
                    'priority' : task.priority if task.priority else None,
                    'due_date' : task.due_date.strftime("%d-%m-%Y %H:%M:%S") if task.due_date else None
                }
            )

        return jsonify(completed_tasks) 
    except Exception as e:
        return jsonify({'error': str(e)}), 500 

#Produce a list of all the uncompleted tasks with their due dates
@app.route('/tasks/uncompleted', methods=['GET'])
def uncompleted_tasks():
    try:
        tasks = Task.query.filter_by(completed=False).all()

        uncompleted_tasks = []
        for task in tasks:
            uncompleted_tasks.append(
                {
                    'id' : task.id,
                    'description' : task.description,
                    'completed' : task.completed,
                    'priority' : task.priority if task.priority else None,
                    'due_date' : task.due_date.strftime("%d-%m-%Y %H:%M:%S") if task.due_date else None
                }
            )

        return jsonify(uncompleted_tasks), 200 
    except Exception as e:
        return jsonify({'error': str(e)}), 500 



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

