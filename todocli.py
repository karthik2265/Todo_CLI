import typer
from rich.console import Console
from rich.table import Table
from model import Todo
from database import insert_todo, delete_todo, update_todo, complete_todo, get_all_todos

console = Console()
app = typer.Typer()


@app.command(short_help='adds an item')
def add(task: str, category: str):
    typer.echo(f"adding {task}, {category}")
    todo = Todo(task, category)
    insert_todo(todo)
    show()


@app.command(short_help='deletes an item')
def delete(position: int):
    typer.echo(f"deleting {position}")
    delete_todo(position - 1)
    show()


@app.command(short_help='updates an item')
def update(position: int, task: str, category: str):
    typer.echo(f"updating {position}")
    update_todo(position - 1, task, category)
    show()


@app.command(short_help='complete an item')
def complete(position: int):
    typer.echo(f"{position} done")
    complete_todo(position - 1)
    show()


@app.command(short_help='show all items')
def show():
    console.print("[bold magenta]Todos[/bold magenta]!", "💻")
    tasks = get_all_todos()
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=6)
    table.add_column("Todo", min_width=20)
    table.add_column("Category", min_width=12, justify="right")
    table.add_column("Done", min_width=12, justify="right")

    for idx, item in enumerate(tasks, start=1):
        todo, category = item.task, item.category
        is_done_str = '✅' if item.status == 2 else '❎'
        category_color = get_category_color(category)
        table.add_row(str(idx), todo, f'[{category_color}]{category}[/{category_color}]', is_done_str)

    console.print(table)


def get_category_color(category: str):
    colors = {'Interview': 'cyan', 'Work': 'yellow', 'Learn': 'violet', 'Ireland': 'green'}
    return colors.get(category, 'white')


if __name__ == '__main__':
    app()
