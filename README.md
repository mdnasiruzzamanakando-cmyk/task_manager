# task_manager
Student Task Manager Project - Shaoxing University - Software Engineering

```markdown id="x2n5qf"
# Student Task Manager Project
Shaoxing University – Computer Science Department  
Course: Software Engineering  

---

## Project Overview
**Student Task Manager** is a simple web application built with **Python and Flask** that helps students:

- Register and log in  
- View tasks by semester  
- Add new tasks  
- Delete tasks  
- Mark tasks as done  

**Features:**

- **Automatic default tasks**: Each semester has 5 default tasks assigned automatically.  
- **Beautiful dashboard**: Tasks displayed as cards  
  - **Pending = yellow**  
  - **Done = green**  
- **Semester filter/search**: View tasks by specific semester.  
- **User-friendly**: Easy to understand, implement, and explain.

---

## Project Structure
```

task_manager/
│── app.py
│── templates/
│     ├── login.html
│     ├── register.html
│     └── dashboard.html
│── static/
│     └── style.css
│── README.md
│── .gitignore

````
> `database.db` is auto-created on first run.

---

## How to Run
1. Clone the repository:  
```bash
git clone https://github.com/YourUsername/task_manager.git
````

2. Navigate into the project folder:

```bash
cd task_manager
```

3. Install dependencies:

```bash
pip install flask
```

4. Run the application:

```bash
python app.py
```

5. Open your browser:

```
http://127.0.0.1:5000/
```

6. Register → Login → Dashboard → Manage tasks

---

## Team Members

* **Akando Md Nasiruzzaman** – 23605108
* **OFOSU Abigail** – 23605109
* **Orifjonov Jasurbek** – 22605101
* **BIRINDA NEMEZO ELLA FRANCK LEVY** – 23605106

````


