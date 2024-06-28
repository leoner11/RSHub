from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from torque_api import JobScheduler
import os

app = Flask(__name__)

# this is if considering that the mysql server is on with the
# username: root
# password: seal123456789
# port: 3306
# name of the db: flask_db


# code to create the flask_db MySQL

'''
    -> CREATE DATABASE flask_db
    -> USE flask_db
    -> CREATE TABLE tasks (
    ->     ID INT AUTO_INCREMENT PRIMARY KEY,
    ->     Username VARCHAR(255) NOT NULL,
    ->     ProjectName VARCHAR(255) NOT NULL,
    ->     TaskName VARCHAR(255) NOT NULL
    -> );
'''
# entering the data of the db is in test.py

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root:seal123456789@localhost:3306/flask_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Parameters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    project_name = db.Column(db.String(200), nullable=False)
    task_name = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/check_job_status', methods=['GET', 'POST'])
def check_job_status():
    data = request.json
    username = data.get('username')
    project_name = data.get('project_name')
    task_name = data.get('task_name')

    # considering the sql has the column called username, project_name and task_name
    if not username or not project_name or not task_name:
        return jsonify({'error': 'Missing required parameters'}), 400

    job_ids = Parameters.query.filter_by(
        username=username, project_name=project_name, task_name=task_name).all()

    if not job_ids:
        return jsonify({'error': 'No jobs found for the given parameters'}), 404

    job_statuses = []
    job_scheduler = JobScheduler()
    for job_id in job_ids:
        job_statuses.append(job_scheduler.see_job_status(job_id))

    return jsonify(job_statuses)


@app.route('/insert_test_data', methods=['POST'])
def insert_test_data():
    try:
        test_data = [
            Parameters(username='user1', project_name='projectA',
                       task_name='task1'),
            Parameters(username='user2', project_name='projectB',
                       task_name='task2'),
            Parameters(username='user3', project_name='projectC',
                       task_name='task3')
        ]
        db.session.add_all(test_data)
        db.session.commit()
        return jsonify({'message': 'Test data inserted successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    with app.app_context():
        # Create database tables if they don't exist
        db.create_all()
    app.run(debug=True)
