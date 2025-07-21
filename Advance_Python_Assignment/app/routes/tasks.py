from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask_login import login_required, current_user
from app.models import db, Task
from datetime import datetime

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/')
@login_required
def view_tasks():
    # Show all tasks for the logged-in user, sorted by most recent
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.created_at.desc()).all()
    return render_template('tasks.html', tasks=tasks)

@tasks_bp.route('/add', methods=['POST'])
@login_required
def add_task():
    # Add a new task with optional due date
    title = request.form.get('title')
    description = request.form.get('description', '')
    due_date_str = request.form.get('due_date')
    
    if not title:
        flash('Task title is required.', 'danger')
        return redirect(url_for('tasks.view_tasks'))
    
    # Convert due date from string to date object
    due_date = None
    if due_date_str:
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format.', 'danger')
            return redirect(url_for('tasks.view_tasks'))
    
    # Create and save task
    new_task = Task(
        title=title,
        description=description,
        due_date=due_date,
        user_id=current_user.id,
        status='pending'
    )
    
    db.session.add(new_task)
    db.session.commit()
    flash('Task added successfully!', 'success')
    
    return redirect(url_for('tasks.view_tasks'))

@tasks_bp.route('/toggle/<int:task_id>', methods=['POST'])
@login_required
def toggle_status(task_id):
    # Cycle task status: pending → working → done → pending
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    
    if not task:
        flash('Task not found.', 'danger')
        return redirect(url_for('tasks.view_tasks'))
    
    if task.status == 'pending':
        task.status = 'working'
    elif task.status == 'working':
        task.status = 'done'
    else:
        task.status = 'pending'
    
    db.session.commit()
    flash('Task status updated!', 'success')
    return redirect(url_for('tasks.view_tasks'))

@tasks_bp.route('/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    # Delete a specific task by ID
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    
    if not task:
        flash('Task not found.', 'danger')
        return redirect(url_for('tasks.view_tasks'))
    
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('tasks.view_tasks'))

@tasks_bp.route('/clear', methods=['POST'])
@login_required
def clear_tasks():
    # Delete all tasks for the current user
    Task.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    flash('All tasks cleared!', 'info')
    return redirect(url_for('tasks.view_tasks'))

@tasks_bp.route('/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    # Edit an existing task's details
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    
    if not task:
        flash('Task not found.', 'danger')
        return redirect(url_for('tasks.view_tasks'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description', '')
        due_date_str = request.form.get('due_date')
        
        if not title:
            flash('Task title is required.', 'danger')
            return render_template('edit_task.html', task=task)
        
        # Parse and update due date
        due_date = None
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format.', 'danger')
                return render_template('edit_task.html', task=task)
        
        # Update task fields
        task.title = title
        task.description = description
        task.due_date = due_date
        task.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('tasks.view_tasks'))
    
    return render_template('edit_task.html', task=task)
