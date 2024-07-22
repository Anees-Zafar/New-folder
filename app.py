# Author: Anees Zafar Iqbal
# Date: July 20, 2024
# Description: A simple Flask application for a ToDo list with basic CRUD operations using SQLAlchemy.

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize the Flask application
app = Flask(__name__)

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"  # Path to the database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
db = SQLAlchemy(app)  # Initialize SQLAlchemy with the app

# Define a model for the ToDo items
class todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)  # Serial number, primary key
    title = db.Column(db.String(40), nullable=False)  # Title of the todo item, cannot be null
    desc = db.Column(db.String(100), nullable=False)  # Description of the todo item, cannot be null
    date = db.Column(db.DateTime, default=datetime.utcnow)  # Date and time, default is the current time

    # Representation method for debugging
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

# Route for the home page with GET and POST methods
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        # Get title and description from the form
        title = request.form['title']
        desc = request.form['desc']
        # Create a new todo item
        stodo = todo(title=title, desc=desc)
        # Add to the session and commit to the database
        db.session.add(stodo)
        db.session.commit()
    # Query all todo items from the database
    alltodo = todo.query.all()
    # Render the index.html template with all todo items
    return render_template("index.html", alltodo=alltodo)

# Route for deleting a todo item
@app.route('/delete/<int:sno>')
def delete(sno):
    # Find the todo item by serial number and delete it
    stodo = todo.query.filter_by(sno=sno).first()
    db.session.delete(stodo)
    db.session.commit()
    # Redirect to the home page
    return redirect('/')

# Route for updating a todo item with GET and POST methods
@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        # Get title and description from the form
        title = request.form['title']
        desc = request.form['desc']
        # Find the todo item by serial number and update it
        stodo = todo.query.filter_by(sno=sno).first()
        stodo.title = title
        stodo.desc = desc
        db.session.add(stodo)
        db.session.commit()
        # Redirect to the home page
        return redirect('/')
    # Query the todo item by serial number and render the update.html template
    stodo = todo.query.filter_by(sno=sno).first()
    return render_template("update.html", stodo=stodo)

# Main block to run the app
if __name__ == "__main__":
    # Ensure to run within the application context
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True, port=8000)  # Run the app on port 8000 with debug mode enabled
