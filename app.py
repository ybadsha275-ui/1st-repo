from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import date, timedelta
import calendar


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

        # Add missing fields to older tasks
        for task in tasks:

            if "completed" not in task:
                task["completed"] = False

            if "subject" not in task:
                task["subject"] = "General"

            if "due_date" not in task:
                task["due_date"] = ""

            if "description" not in task:
                task["description"] = ""

            if "starred" not in task:
                task["starred"] = False

            if "completed_on" not in task:
                task["completed_on"] = ""

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
            "study_dates": [],
            "daily_goal": 5,
            "pomodoro_sessions": {}
        }

    try:

        with open(STUDY_DATA_FILE, "r") as file:

            data = json.load(file)

        if "study_dates" not in data:
            data["study_dates"] = []

        if "daily_goal" not in data:
            data["daily_goal"] = 5

        if "pomodoro_sessions" not in data:
            data["pomodoro_sessions"] = {}

        return data

    except (json.JSONDecodeError, FileNotFoundError):

        return {
            "study_dates": [],
            "daily_goal": 5,
            "pomodoro_sessions": {}
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

    if today not in data["study_dates"]:

        data["study_dates"].append(today)

        data["study_dates"].sort()

        save_study_data(data)


# ==========================================
# Calculate current streak
# ==========================================

def calculate_current_streak():

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

    today = date.today()

    if today in dates:

        current_date = today

    elif today - timedelta(days=1) in dates:

        current_date = today - timedelta(days=1)

    else:

        return 0

    streak = 0

    while current_date in dates:

        streak += 1

        current_date -= timedelta(days=1)

    return streak


# ==========================================
# Calculate longest streak
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
# Get today's completed tasks
# ==========================================

def get_today_completed_tasks(tasks):

    today = date.today().isoformat()

    count = 0

    for task in tasks:

        if (
            task.get("completed", False)
            and task.get("completed_on", "") == today
        ):

            count += 1

    return count


# ==========================================
# Get weekly dashboard
# ==========================================

def get_weekly_dashboard(tasks):

    today = date.today()

    monday = today - timedelta(
        days=today.weekday()
    )

    data = load_study_data()

    study_dates = set(
        data.get(
            "study_dates",
            []
        )
    )

    weekly_days = []

    for i in range(7):

        current_day = monday + timedelta(days=i)

        iso_date = current_day.isoformat()

        completed_count = 0

        for task in tasks:

            if (
                task.get("completed", False)
                and task.get("completed_on", "") == iso_date
            ):

                completed_count += 1

        weekly_days.append({

            "name": current_day.strftime("%a"),

            "date": current_day.strftime("%d %b"),

            "iso_date": iso_date,

            "studied": iso_date in study_dates,

            "completed": completed_count,

            "is_today": current_day == today

        })

    weekly_study_days = sum(

        1
        for day in weekly_days
        if day["studied"]

    )

    weekly_completed_tasks = sum(

        day["completed"]
        for day in weekly_days

    )

    return (
        weekly_days,
        weekly_study_days,
        weekly_completed_tasks
    )


# ==========================================
# Build monthly calendar
# ==========================================

def get_month_calendar(tasks, year, month):

    cal = calendar.Calendar(firstweekday=0)

    month_weeks = []

    for week in cal.monthdatescalendar(year, month):

        week_data = []

        for current_day in week:

            iso_date = current_day.isoformat()

            day_tasks = [
                task
                for task in tasks
                if task.get("due_date", "") == iso_date
            ]

            week_data.append({
                "date": current_day.day,
                "iso_date": iso_date,
                "current_month": current_day.month == month,
                "is_today": current_day == date.today(),
                "tasks": day_tasks
            })

        month_weeks.append(week_data)

    return month_weeks


# ==========================================
# Build analytics data
# ==========================================

def get_analytics(tasks):

    priority_counts = {
        "HIGH": 0,
        "MEDIUM": 0,
        "LOW": 0
    }

    for task in tasks:

        priority = task.get(
            "priority",
            "MEDIUM"
        )

        if priority in priority_counts:

            priority_counts[priority] += 1

    total = len(tasks)

    completed = sum(
        1
        for task in tasks
        if task.get("completed", False)
    )

    pending = total - completed

    overdue = sum(
        1
        for task in tasks
        if (
            not task.get("completed", False)
            and task.get("due_date", "")
            and get_due_status(
                task.get("due_date", ""),
                False
            ) == "overdue"
        )
    )

    weekday_counts = {
        "Mon": 0,
        "Tue": 0,
        "Wed": 0,
        "Thu": 0,
        "Fri": 0,
        "Sat": 0,
        "Sun": 0
    }

    for task in tasks:

        completed_on = task.get(
            "completed_on",
            ""
        )

        if completed_on:

            try:

                completed_date = date.fromisoformat(
                    completed_on
                )

                weekday_counts[
                    completed_date.strftime("%a")
                ] += 1

            except ValueError:

                pass

    most_productive_day = "—"

    if any(weekday_counts.values()):

        most_productive_day = max(
            weekday_counts,
            key=weekday_counts.get
        )

    return {

        "priority_counts": priority_counts,

        "completed": completed,

        "pending": pending,

        "overdue": overdue,

        "total": total,

        "weekday_counts": weekday_counts,

        "most_productive_day":
            most_productive_day

    }


# ==========================================
# Get due-date status
# ==========================================

def get_due_status(
    due_date,
    completed
):

    if completed:

        return "completed"

    if not due_date:

        return "none"

    try:

        today = date.today()

        due = date.fromisoformat(
            due_date
        )

        if due < today:

            return "overdue"

        elif due == today:

            return "today"

        else:

            return "upcoming"

    except ValueError:

        return "none"


# ==========================================
# Home page
# ==========================================

@app.route("/")
def index():

    all_tasks = load_tasks()

    for task in all_tasks:

        task["due_status"] = get_due_status(
            task.get("due_date", ""),
            task.get("completed", False)
        )

    task_items = list(
        enumerate(all_tasks)
    )

    # Search
    search = request.args.get(
        "search",
        ""
    ).strip().lower()

    # Filters
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

    important_filter = request.args.get(
        "important",
        ""
    )

    # Calendar
    today = date.today()

    try:

        calendar_year = int(
            request.args.get(
                "year",
                today.year
            )
        )

        calendar_month = int(
            request.args.get(
                "month",
                today.month
            )
        )

        if calendar_month < 1:

            calendar_month = 12
            calendar_year -= 1

        elif calendar_month > 12:

            calendar_month = 1
            calendar_year += 1

    except ValueError:

        calendar_year = today.year
        calendar_month = today.month

    # Search filtering
    if search:

        task_items = [

            (task_id, task)

            for task_id, task
            in task_items

            if (
                search
                in task.get(
                    "task",
                    ""
                ).lower()

                or search
                in task.get(
                    "subject",
                    ""
                ).lower()

                or search
                in task.get(
                    "description",
                    ""
                ).lower()
            )
        ]

    # Priority filter
    if priority_filter:

        task_items = [

            (task_id, task)

            for task_id, task
            in task_items

            if task.get(
                "priority"
            ) == priority_filter

        ]

    # Subject filter
    if subject_filter:

        task_items = [

            (task_id, task)

            for task_id, task
            in task_items

            if task.get(
                "subject",
                "General"
            ) == subject_filter

        ]

    # Status filter
    if status_filter == "completed":

        task_items = [

            (task_id, task)

            for task_id, task
            in task_items

            if task.get(
                "completed",
                False
            )

        ]

    elif status_filter == "pending":

        task_items = [

            (task_id, task)

            for task_id, task
            in task_items

            if not task.get(
                "completed",
                False
            )

        ]

    # Important filter
    if important_filter == "true":

        task_items = [

            (task_id, task)

            for task_id, task
            in task_items

            if task.get(
                "starred",
                False
            )

        ]

    # ==========================================
    # Reminders
    # ==========================================

    today = date.today()
    tomorrow = today + timedelta(days=1)
    three_days_later = today + timedelta(days=3)

    reminders = []

    for task_id, task in enumerate(all_tasks):

        # Completed tasks do not need reminders
        if task.get("completed", False):
            continue

        due_date_string = task.get("due_date", "")

        if not due_date_string:
            continue

        try:
            due_date = date.fromisoformat(due_date_string)
        except ValueError:
            continue

        # Overdue
        if due_date < today:
            reminders.append({
                "task_id": task_id,
                "task": task.get("task", ""),
                "subject": task.get("subject", "General"),
                "priority": task.get("priority", "MEDIUM"),
                "due_date": due_date_string,
                "type": "overdue",
                "message": "This task is overdue."
            })

        # Due today
        elif due_date == today:
            reminders.append({
                "task_id": task_id,
                "task": task.get("task", ""),
                "subject": task.get("subject", "General"),
                "priority": task.get("priority", "MEDIUM"),
                "due_date": due_date_string,
                "type": "today",
                "message": "This task is due today."
            })

        # Due tomorrow
        elif due_date == tomorrow:
            reminders.append({
                "task_id": task_id,
                "task": task.get("task", ""),
                "subject": task.get("subject", "General"),
                "priority": task.get("priority", "MEDIUM"),
                "due_date": due_date_string,
                "type": "tomorrow",
                "message": "This task is due tomorrow."
            })

        # Due within 3 days
        elif due_date <= three_days_later:
            reminders.append({
                "task_id": task_id,
                "task": task.get("task", ""),
                "subject": task.get("subject", "General"),
                "priority": task.get("priority", "MEDIUM"),
                "due_date": due_date_string,
                "type": "upcoming",
                "message": "This task is coming up soon."
            })

    # Overall statistics
    total_tasks = len(all_tasks)

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

    progress = (

        round(
            (
                completed_tasks
                / total_tasks
            ) * 100
        )

        if total_tasks > 0

        else 0

    )

    # Subjects
    subjects = sorted(
        set(
            task.get(
                "subject",
                "General"
            )
            for task in all_tasks
        )
    )

    # Subject progress
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

        subject_percentage = (

            round(
                (
                    subject_completed
                    / subject_total
                ) * 100
            )

            if subject_total > 0

            else 0

        )

        subject_progress.append({

            "subject": subject,

            "total": subject_total,

            "completed":
                subject_completed,

            "percentage":
                subject_percentage

        })

    # Study streak
    current_streak = (
        calculate_current_streak()
    )

    longest_streak = (
        calculate_longest_streak()
    )

    # Weekly dashboard
    (
        weekly_days,
        weekly_study_days,
        weekly_completed_tasks
    ) = get_weekly_dashboard(
        all_tasks
    )

    # Daily goal
    study_data = load_study_data()

    daily_goal = study_data.get(
        "daily_goal",
        5
    )

    today_completed = (
        get_today_completed_tasks(
            all_tasks
        )
    )

    daily_goal_progress = (

        round(
            (
                today_completed
                / daily_goal
            ) * 100
        )

        if daily_goal > 0

        else 0

    )

    if daily_goal_progress > 100:

        daily_goal_progress = 100

    # Today's Pomodoros
    today_iso = date.today().isoformat()

    pomodoro_sessions = study_data.get(
        "pomodoro_sessions",
        {}
    )

    today_pomodoros = pomodoro_sessions.get(
        today_iso,
        0
    )

    # Calendar
    month_calendar = get_month_calendar(
        all_tasks,
        calendar_year,
        calendar_month
    )

    calendar_month_name = calendar.month_name[
        calendar_month
    ]

    previous_month = (
        date(
            calendar_year,
            calendar_month,
            1
        )
        - timedelta(days=1)
    )

    next_month = (
        date(
            calendar_year,
            calendar_month,
            28
        )
        + timedelta(days=4)
    ).replace(day=1)

    # Analytics
    analytics = get_analytics(
        all_tasks
    )

    return render_template(

        "index.html",

        task_items=task_items,

        # NEW: send reminders to index.html
        reminders=reminders,

        total_tasks=total_tasks,

        completed_tasks=
            completed_tasks,

        pending_tasks=
            pending_tasks,

        progress=progress,

        subjects=subjects,

        subject_progress=
            subject_progress,

        search=search,

        priority_filter=
            priority_filter,

        subject_filter=
            subject_filter,

        status_filter=
            status_filter,

        important_filter=
            important_filter,

        current_streak=
            current_streak,

        longest_streak=
            longest_streak,

        weekly_days=
            weekly_days,

        weekly_study_days=
            weekly_study_days,

        weekly_completed_tasks=
            weekly_completed_tasks,

        daily_goal=
            daily_goal,

        today_completed=
            today_completed,

        daily_goal_progress=
            daily_goal_progress,

        today_pomodoros=
            today_pomodoros,

        month_calendar=
            month_calendar,

        calendar_year=
            calendar_year,

        calendar_month=
            calendar_month,

        calendar_month_name=
            calendar_month_name,

        previous_month=
            previous_month,

        next_month=
            next_month,

        analytics=
            analytics

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

    if not subject:

        subject = "General"

    if task_name:

        new_task = {

            "task": task_name,

            "subject": subject,

            "description": description,

            "priority": priority,

            "due_date": due_date,

            "completed": False,

            "starred": False,

            "completed_on": ""

        }

        tasks.append(
            new_task
        )

        save_tasks(tasks)

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

        task = tasks[task_id]

        task["completed"] = not task.get(
            "completed",
            False
        )

        if task["completed"]:

            task["completed_on"] = (
                date.today().isoformat()
            )

            record_study_date()

        else:

            task["completed_on"] = ""

        save_tasks(tasks)

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

        tasks.pop(task_id)

        save_tasks(tasks)

    return redirect(
        url_for("index")
    )


# ==========================================
# Edit task
# ==========================================

@app.route(
    "/edit/<int:task_id>"
)
def edit_task(task_id):

    tasks = load_tasks()

    if 0 <= task_id < len(tasks):

        return render_template(
            "edit.html",
            task=tasks[task_id],
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

        tasks[task_id]["task"] = (
            task_name
        )

        tasks[task_id]["subject"] = (
            subject
        )

        tasks[task_id]["priority"] = (
            priority
        )

        tasks[task_id]["due_date"] = (
            due_date
        )

        tasks[task_id]["description"] = (
            description
        )

        save_tasks(tasks)

    return redirect(
        url_for("index")
    )


# ==========================================
# Star / Unstar task
# ==========================================

@app.route(
    "/star/<int:task_id>"
)
def toggle_star(task_id):

    tasks = load_tasks()

    if 0 <= task_id < len(tasks):

        tasks[task_id]["starred"] = not tasks[
            task_id
        ].get(
            "starred",
            False
        )

        save_tasks(tasks)

    return redirect(
        url_for("index")
    )


# ==========================================
# Daily goal
# ==========================================

@app.route(
    "/set-goal",
    methods=["POST"]
)
def set_goal():

    study_data = load_study_data()

    try:

        goal = int(
            request.form.get(
                "daily_goal",
                5
            )
        )

        if goal < 1:

            goal = 1

        if goal > 50:

            goal = 50

    except ValueError:

        goal = 5

    study_data["daily_goal"] = goal

    save_study_data(
        study_data
    )

    return redirect(
        url_for("index")
    )


# ==========================================
# Pomodoro completed
# ==========================================

@app.route(
    "/pomodoro-complete",
    methods=["POST"]
)
def pomodoro_complete():

    study_data = load_study_data()

    today = date.today().isoformat()

    sessions = study_data.setdefault(
        "pomodoro_sessions",
        {}
    )

    sessions[today] = (
        sessions.get(today, 0)
        + 1
    )

    record_study_date()

    save_study_data(
        study_data
    )

    return {
        "success": True,
        "sessions": sessions[today]
    }


# ==========================================
# Run application
# ==========================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )