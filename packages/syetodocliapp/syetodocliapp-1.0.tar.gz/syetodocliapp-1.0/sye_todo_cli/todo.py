import click
from .todo_manager import TodoManager

todo_manager = TodoManager()

@click.group()
def cli():
    "ToDo cli application"
    pass

@cli.command()
@click.argument('task')
def add(task):
    todo_manager.add_todo(task)
    

@cli.command()
def list():
    todos = todo_manager.list_todos()
    for index, todo in enumerate(todos):
        status = "✔" if todo['completed'] else "✘" # "\u2714", "\u2718" are the escape sequences accordingly
        click.echo(f"{index}: [{status}] {todo['task']}")
        
@cli.command()        
@click.argument('index',type=int)
def remove(index):
    try:
        todo_manager.remove_todo(index)
        click.echo(f"task at the index {index} is removed.")
    except IndexError:
        click.echo(f"Invalid Index:{index}")
        
        
if __name__ == "__main__":
    cli()
        
    