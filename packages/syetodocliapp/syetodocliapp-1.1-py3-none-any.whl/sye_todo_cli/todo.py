import click
from .todo_manager import TodoManager

todo_manager = TodoManager()
progress_bar = {"new": "□", "inprogress": "▣","done": "■"}  #\u25A1 (□), \u25A3 (▣), \u25A0 (■)

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
        # status = "✔" if todo['completed'] else "✘" # "\u2714", "\u2718" are the escape sequences accordingly
        click.echo(f"{index}: {progress_bar[todo['status']]} {todo['task']}")
        
def update_util(index,status):
    try:
        status = "done" if status else "inprogress"
        todo_manager.update_todo(index, status)
        todo = todo_manager.get_todo(index)
        msg = f"{progress_bar[status]} {todo}" if todo else "No such task"
        click.echo(msg)
    except IndexError as e:
        click.echo(f"{str(e)}. Invalid Index.")
        
        
@cli.command()
@click.argument('index', type=int)
def inprogress(index):
    update_util(index, False)
        
@cli.command()
@click.argument('index',type=int)
def done(index):
    update_util(index, True)
    
@cli.command()        
@click.argument('index',type=int)
def remove(index):
    try:
        task = todo_manager.get_todo(index)
        todo_manager.remove_todo(index)
        click.echo(f"task '{task}' is removed.")
    except IndexError as e:
        click.echo(f"{str(e)}. Invalid Index:{index}")
        
        
if __name__ == "__main__":
    cli()
        
    