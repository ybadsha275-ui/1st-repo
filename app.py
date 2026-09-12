from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import date, timedelta


app = Flask(__name__)


# ==========================================
# File locations
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TASKS_FILE = os.path.join(BASE_DIR, "tasks.json")

STUDY_DATA_FILE = os.path.join(BASE_DIR, "study_data.json")


# ==========================================
# Load tasks
# ==========================================

def load_tasks():

    if not os.path.exists(TASKS_FILE):
        return []

    try:

        with open(TASKS_FILE, "r") as file:
            tasks = json.load(file)

        # Make sure older tasks have all required fields
        for task in tasks:

            if "completed" not in task:
                task["completed"] = False

            if "subject" not in task:
                task["subject"] = "General"

            if "due_date" not in task:
                task["due_date"] = ""

            if "description" not in task:
                task["description"] = ""

        return tasks

    except (json.JSONDecodeError, FileNotFoundError):

        return []


# ==========================================
# Save tasks
# ==========================================

def save_tasks(tasks):

    with open(TASKS_FILE, "w") as file:

        json.dump(tasks, file, indent=4)


# ==========================================
# Load study data
# ==========================================

def load_study_data():

    if not os.path.exists(STUDY_DATA_FILE):

        return {
            "study_dates": []
        }

    try:

        with open(STUDY_DATA_FILE, "r") as file:

            data = json.load(file)

        # Make sure study_dates exists
        if "study_dates" not in data:

            data["study_dates"] = []

        return data

    except (json.JSONDecodeError, FileNotFoundError):

        return {
            "study_dates": []
        }


# ==========================================
# Save study data
# ==========================================

def save_study_data(data):

    with open(STUDY_DATA_FILE, "w") as file:

        json.dump(data, file, indent=4)


# ==========================================
# Record study date
# ==========================================

def record_study_date():

    data = load_study_data()

    today = date.today().isoformat()

    # Add today's date only once
    if today not in data["study_dates"]:

        data["study_dates"].append(today)

        # Sort dates
        data["study_dates"].sort()

        save_study_data(data)


# ==========================================
# Calculate current study streak
# ==========================================

def calculate_current_streak():

    data = load_study_data()

    study_dates = data.get(
        "study_dates",
        []
    )

    if not study_dates:

        return 0


    # Convert strings to date objects
    dates = set()

    for date_string in study_dates:

        try:

            dates.add(
                date.fromisoformat(date_string)
            )

        except ValueError:

            continue


    if not dates:

        return 0


    today = date.today()


    # If user did not study today,
    # check whether they studied yesterday.
    if today not in dates:

        if today - timedelta(days=1) not in dates:

            return 0

        current_date = today - timedelta(days=1)

    else:

        current_date = today


    streak = 0


    while current_date in dates:

        streak += 1

        current_date -= timedelta(days=1)


    return streak


# ==========================================
# Calculate longest study streak
# ==========================================

def calculate_longest_streak():

    data = load_study_data()

    study_dates = data.get(
        "study_dates",
        []
    )

    if not study_dates:

        return 0


    dates = set()

    for date_string in study_dates:

        try:

            dates.add(
                date.fromisoformat(date_string)
            )

        except ValueError:

            continue


    if not dates:

        return 0


    sorted_dates = sorted(dates)


    longest = 1

    current = 1


    for i in range(
        1,
        len(sorted_dates)
    ):

        difference = (
            sorted_dates[i]
            - sorted_dates[i - 1]
        ).days


        if difference == 1:

            current += 1

        else:

            current = 1


        if current > longest:

            longest = current


    return longest


# ==========================================
# Get due-date status
# ==========================================

def get_due_status(due_date, completed):

    # Completed tasks
    if completed:

        return "completed"


    # No due date
    if not due_date:

        return "none"


    try:

        today = date.today()

        due = date.fromisoformat(due_date)


        # Due date has passed
        if due < today:

            return "overdue"


        # Due today
        elif due == today:

            return "today"


        # Future due date
        else:

            return "upcoming"


    except ValueError:

        return "none"


# ==========================================
# Home page
# ==========================================

@app.route("/")
def index():

    # Load all tasks
    all_tasks = load_tasks()


    # ==========================================
    # Add due-date status
    # ==========================================

    for task in all_tasks:

        task["due_status"] = get_due_status(
            task.get(
                "due_date",
                ""
            ),
            task.get(
                "completed",
                False
            )
        )


    # ==========================================
    # Create task items with ORIGINAL IDs
    # ==========================================

    task_items = list(
        enumerate(all_tasks)
    )


    # ==========================================
    # Search
    # ==========================================

    search = request.args.get(
        "search",
        ""
    ).strip().lower()


    # ==========================================
    # Filters
    # ==========================================

    priority_filter = request.args.get(
        "priority",
        ""
    )

    subject_filter = request.args.get(
        "subject",
        ""
    )

    status_filter = request.args.get(
        "status",
        ""
    )


    # ==========================================
    # Apply search
    # ==========================================

    if search:

        task_items = [

            (task_id, task)

            for task_id, task in task_items

            if (
                search in task.get(
                    "task",
                    ""
                ).lower()

                or search in task.get(
                    "subject",
                    ""
                ).lower()

                or search in task.get(
                    "description",
                    ""
                ).lower()
            )
        ]


    # ==========================================
    # Apply priority filter
    # ==========================================

    if priority_filter:

        task_items = [

            (task_id, task)

            for task_id, task in task_items

            if task.get(
                "priority"
            ) == priority_filter
        ]


    # ==========================================
    # Apply subject filter
    # ==========================================

    if subject_filter:

        task_items = [

            (task_id, task)

            for task_id, task in task_items

            if task.get(
                "subject",
                "General"
            ) == subject_filter
        ]


    # ==========================================
    # Apply status filter
    # ==========================================

    if status_filter == "completed":

        task_items = [

            (task_id, task)

            for task_id, task in task_items

            if task.get(
                "completed",
                False
            )
        ]

    elif status_filter == "pending":

        task_items = [

            (task_id, task)

            for task_id, task in task_items

            if not task.get(
                "completed",
                False
            )
        ]


    # ==========================================
    # Statistics
    # ==========================================

    total_tasks = len(
        all_tasks
    )


    completed_tasks = sum(

        1

        for task in all_tasks

        if task.get(
            "completed",
            False
        )
    )


    pending_tasks = (
        total_tasks
        - completed_tasks
    )


    # ==========================================
    # Overall progress
    # ==========================================

    if total_tasks > 0:

        progress = round(

            (
                completed_tasks
                / total_tasks
            )
            * 100
        )

    else:

        progress = 0


    # ==========================================
    # Get subjects
    # ==========================================

    subjects = sorted(

        set(

            task.get(
                "subject",
                "General"
            )

            for task in all_tasks
        )
    )


    # ==========================================
    # Subject-wise progress
    # ==========================================

    subject_progress = []


    for subject in subjects:

        subject_tasks = [

            task

            for task in all_tasks

            if task.get(
                "subject",
                "General"
            ) == subject
        ]


        subject_total = len(
            subject_tasks
        )


        subject_completed = sum(

            1

            for task in subject_tasks

            if task.get(
                "completed",
                False
            )
        )


        if subject_total > 0:

            subject_percentage = round(

                (
                    subject_completed
                    / subject_total
                )
                * 100
            )

        else:

            subject_percentage = 0


        subject_progress.append({

            "subject": subject,

            "total": subject_total,

            "completed": subject_completed,

            "percentage": subject_percentage

        })


    # ==========================================
    # Study streak
    # ==========================================

    current_streak = calculate_current_streak()

    longest_streak = calculate_longest_streak()


    # ==========================================
    # Render page
    # ==========================================

    return render_template(

        "index.html",

        task_items=task_items,

        total_tasks=total_tasks,

        completed_tasks=completed_tasks,

        pending_tasks=pending_tasks,

        progress=progress,

        subjects=subjects,

        subject_progress=subject_progress,

        search=search,

        priority_filter=priority_filter,

        subject_filter=subject_filter,

        status_filter=status_filter,

        current_streak=current_streak,

        longest_streak=longest_streak

    )


# ==========================================
# Add task
# ==========================================

@app.route(
    "/add",
    methods=["POST"]
)
def add_task():

    tasks = load_tasks()


    task_name = request.form.get(
        "task",
        ""
    ).strip()


    subject = request.form.get(
        "subject",
        ""
    ).strip()


    priority = request.form.get(
        "priority",
        "MEDIUM"
    )


    due_date = request.form.get(
        "due_date",
        ""
    ).strip()


    description = request.form.get(
        "description",
        ""
    ).strip()


    # Default subject
    if not subject:

        subject = "General"


    # Add task only if task name exists
    if task_name:

        new_task = {

            "task": task_name,

            "subject": subject,

            "description": description,

            "priority": priority,

            "due_date": due_date,

            "completed": False

        }


        tasks.append(
            new_task
        )

        save_tasks(
            tasks
        )


    return redirect(
        url_for("index")
    )


# ==========================================
# Complete / Undo task
# ==========================================

@app.route(
    "/complete/<int:task_id>"
)
def complete_task(task_id):

    tasks = load_tasks()


    if 0 <= task_id < len(tasks):

        currently_completed = tasks[
            task_id
        ].get(
            "completed",
            False
        )


        # Toggle completion
        tasks[
            task_id
        ][
            "completed"
        ] = not currently_completed


        # If task is being completed
        if not currently_completed:

            record_study_date()


        save_tasks(
            tasks
        )


    return redirect(
        url_for("index")
    )


# ==========================================
# Delete task
# ==========================================

@app.route(
    "/delete/<int:task_id>"
)
def delete_task(task_id):

    tasks = load_tasks()


    if 0 <= task_id < len(tasks):

        tasks.pop(
            task_id
        )

        save_tasks(
            tasks
        )


    return redirect(
        url_for("index")
    )


# ==========================================
# Edit task - Show edit page
# ==========================================

@app.route(
    "/edit/<int:task_id>"
)
def edit_task(task_id):

    tasks = load_tasks()


    if 0 <= task_id < len(tasks):

        return render_template(

            "edit.html",

            task=tasks[
                task_id
            ],

            task_id=task_id

        )


    return redirect(
        url_for("index")
    )


# ==========================================
# Update task
# ==========================================

@app.route(
    "/update/<int:task_id>",
    methods=["POST"]
)
def update_task(task_id):

    tasks = load_tasks()


    if 0 <= task_id < len(tasks):

        task_name = request.form.get(
            "task",
            ""
        ).strip()


        subject = request.form.get(
            "subject",
            "General"
        ).strip()


        priority = request.form.get(
            "priority",
            "MEDIUM"
        )


        due_date = request.form.get(
            "due_date",
            ""
        ).strip()


        description = request.form.get(
            "description",
            ""
        ).strip()


        if not subject:

            subject = "General"


        # Update task
        tasks[
            task_id
        ][
            "task"
        ] = task_name


        tasks[
            task_id
        ][
            "subject"
        ] = subject


        tasks[
            task_id
        ][
            "priority"
        ] = priority


        tasks[
            task_id
        ][
            "due_date"
        ] = due_date


        tasks[
            task_id
        ][
            "description"
        ] = description


        # Save changes
        save_tasks(
            tasks
        )


    return redirect(
        url_for("index")
    )


# ==========================================
# Run application
# ==========================================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )