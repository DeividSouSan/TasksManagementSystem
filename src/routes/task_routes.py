from flask import Blueprint, Response, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from src import htmx
from src.forms.task_form import TaskForm
from src.models.task import TaskStatus
from src.repositories.task_repository import TaskRepository
from src.use_cases.tasks.add_task_use_case import AddTaskUseCase
from src.use_cases.tasks.delete_task_use_case import DeleteTaskUseCase
from src.use_cases.tasks.get_tasks_use_case import GetTasksUseCase
from src.use_cases.tasks.search_tasks_use_case import SearchTasksUseCase

task = Blueprint("task", __name__, url_prefix="/task")


def redirectResponse(route: str):
    response = Response()
    response.headers["hx-redirect"] = url_for(route)
    return response


@task.route("/get", methods=["GET"])
@login_required
def get():
    repository = TaskRepository()

    use_case = GetTasksUseCase(current_user.id, repository)
    tasks = use_case.execute()

    return render_template(
        "partials/task-container.html",
        tasks=tasks,
        TaskStatus=TaskStatus
    )


@task.route("/search", methods=["GET"])
def search():
    text = request.args.get("text-to-search")
    repository = TaskRepository()

    use_case = SearchTasksUseCase(current_user.id, repository)
    tasks = use_case.execute(text)

    return render_template(
        "partials/task-container.html", tasks=tasks, TaskStatus=TaskStatus
    )


@task.route("/add", methods=["POST"])
@login_required
def add():
    form = TaskForm()
    repository = TaskRepository()

    if form.validate_on_submit():
        use_case = AddTaskUseCase(current_user.id, form, repository)
        use_case.execute()

    return redirect(url_for("view.board"))

@task.route("/delete/<id>", methods=["DELETE"])
@login_required
def delete(id):
    form = TaskForm()
    repository = TaskRepository()

    if form.validate_on_submit():
        use_case = DeleteTaskUseCase(current_user.id, form, repository)
        use_case.execute()

    return redirect(url_for("view.board"))
