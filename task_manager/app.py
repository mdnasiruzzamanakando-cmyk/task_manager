from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret123'

# Default tasks for each semester
DEFAULT_TASKS = {
    "Semester 1": [
        "Math Assignment",
        "Programming Lab",
        "English Essay",
        "Computer Networks Quiz",
        "Software Engineering Report"
    ],
    "Semester 2": [
        "Database Project",
        "Python Lab",
        "Data Structures Assignment",
        "Operating System Quiz",
        "Web Development Project"
    ]
}

# Initialize DB
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        semester TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS user_tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        task_id INTEGER,
        status TEXT
    )''')
    conn.commit()
    conn.close()

init_db()

# Insert default tasks if not exists
def insert_default_tasks():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    for semester, tasks in DEFAULT_TASKS.items():
        for t in tasks:
            c.execute("SELECT * FROM tasks WHERE title=? AND semester=?", (t, semester))
            if not c.fetchone():
                c.execute("INSERT INTO tasks (title, semester) VALUES (?, ?)", (t, semester))
    conn.commit()
    conn.close()

insert_default_tasks()

# REGISTER
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        user = request.form['username']
        pw = request.form['password']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username,password) VALUES (?,?)",(user,pw))
            conn.commit()
        except:
            conn.close()
            return "Username already exists!"
        conn.close()
        return redirect('/')
    return render_template('register.html')

# LOGIN
@app.route('/', methods=['GET','POST'])
def login():
    if request.method=='POST':
        user = request.form['username']
        pw = request.form['password']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?",(user,pw))
        result = c.fetchone()
        conn.close()
        if result:
            session['user_id']=result[0]
            return redirect('/dashboard')
        else:
            return "Invalid credentials!"
    return render_template('login.html')

# DASHBOARD
@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    user_id = session['user_id']
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Add manual task
    if request.method=='POST' and 'new_task' in request.form:
        title = request.form['new_task'].strip()
        semester = request.form['semester_add']
        if title:
            # Insert task in tasks table if not exists
            c.execute("SELECT * FROM tasks WHERE title=? AND semester=?", (title, semester))
            if not c.fetchone():
                c.execute("INSERT INTO tasks (title, semester) VALUES (?,?)", (title, semester))
            # Assign to user_tasks if not exists
            c.execute("SELECT id FROM tasks WHERE title=? AND semester=?", (title, semester))
            task_id = c.fetchone()[0]
            c.execute("SELECT * FROM user_tasks WHERE user_id=? AND task_id=?", (user_id, task_id))
            if not c.fetchone():
                c.execute("INSERT INTO user_tasks (user_id,task_id,status) VALUES (?,?,?)",(user_id,task_id,"Pending"))
            conn.commit()

    # Handle Semester Search / Auto assign
    semester_filter = request.args.get('semester_filter')
    if semester_filter:
        # Auto assign default 5 tasks
        for task_title in DEFAULT_TASKS.get(semester_filter, []):
            c.execute("SELECT id FROM tasks WHERE title=? AND semester=?", (task_title, semester_filter))
            task_id = c.fetchone()[0]
            c.execute("SELECT * FROM user_tasks WHERE user_id=? AND task_id=?", (user_id, task_id))
            if not c.fetchone():
                c.execute("INSERT INTO user_tasks (user_id,task_id,status) VALUES (?,?,?)", (user_id, task_id, "Pending"))
        conn.commit()

        # Fetch only selected semester tasks
        c.execute("""
            SELECT user_tasks.id, tasks.title, user_tasks.status
            FROM user_tasks
            JOIN tasks ON user_tasks.task_id=tasks.id
            WHERE user_tasks.user_id=? AND tasks.semester=?
        """, (user_id, semester_filter))
    else:
        # Fetch all tasks
        c.execute("""
            SELECT user_tasks.id, tasks.title, user_tasks.status, tasks.semester
            FROM user_tasks
            JOIN tasks ON user_tasks.task_id=tasks.id
            WHERE user_tasks.user_id=?
        """, (user_id,))
    tasks = c.fetchall()
    conn.close()
    return render_template('dashboard.html', tasks=tasks, semester_filter=semester_filter)

# MARK DONE
@app.route('/complete/<int:id>')
def complete(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("UPDATE user_tasks SET status='Done' WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/dashboard')

# DELETE TASK
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM user_tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/dashboard')

# LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__=='__main__':
    app.run(debug=True)