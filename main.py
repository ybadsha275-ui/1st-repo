import json


# Load tasks from file
def load_tasks():
    try:
        with open("tasks.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


# Save tasks to file
def save_tasks(tasks):
    with open("tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)


# Add a new task
def add_task(tasks):
    task = input("Enter your task: ")

    print("\nChoose Priority:")
    print("1. High")
    print("2. Medium")
    print("3. Low")

    priority_choice = input("Enter priority: ")

    if priority_choice == "1":
        priority = "HIGH"
    elif priority_choice == "2":
        priority = "MEDIUM"
    elif priority_choice == "3":
        priority = "LOW"
    else:
        print("Invalid priority. Task not added.")
        return

    new_task = {
        "task": task,
        "priority": priority
    }

    tasks.append(new_task)
    save_tasks(tasks)

    print("Task added successfully!")


# View all tasks
def view_tasks(tasks):
    if len(tasks) == 0:
        print("No tasks added yet.")
        return

    print("\nYour Tasks:")

    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task['task']} - {task['priority']}")


# Complete a task
def complete_task(tasks):
    if len(tasks) == 0:
        print("No tasks to complete.")
        return

    view_tasks(tasks)

    try:
        number = int(input("\nEnter the task number you completed: "))

        if 1 <= number <= len(tasks):
            completed_task = tasks.pop(number - 1)
            save_tasks(tasks)

            print(f"Completed: {completed_task['task']}")
        else:
            print("Invalid task number.")

    except ValueError:
        print("Please enter a valid number.")


# Delete a task
def delete_task(tasks):
    if len(tasks) == 0:
        print("No tasks to delete.")
        return

    view_tasks(tasks)

    try:
        number = int(input("\nEnter the task number you want to delete: "))

        if 1 <= number <= len(tasks):
            deleted_task = tasks.pop(number - 1)
            save_tasks(tasks)

            print(f"Deleted: {deleted_task['task']}")
        else:
            print("Invalid task number.")

    except ValueError:
        print("Please enter a valid number.")


# Main program
def main():
    tasks = load_tasks()

    print("=================================")
    print("      STUDENT STUDY PLANNER")
    print("=================================")

    while True:
        print("\n1. Add Task")
        print("2. View Tasks")
        print("3. Complete Task")
        print("4. Delete Task")
        print("5. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_task(tasks)

        elif choice == "2":
            view_tasks(tasks)

        elif choice == "3":
            complete_task(tasks)

        elif choice == "4":
            delete_task(tasks)

        elif choice == "5":
            print("Thank you for using Student Study Planner!")
            break

        else:
            print("Invalid choice. Please try again.")


# Start the program
if __name__ == "__main__":
    main()