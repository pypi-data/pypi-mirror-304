import click
from .todo_manager import TodoManager

todo_manager = TodoManager()
progress_bar = {"new": "□", "inprogress": "▣","done": "■"}  #\u25A1 (□), \u25A3 (▣), \u25A0 (■)

@click.group()
def cli():
    "ToDo cli application"
    pass

# Add tasks
@cli.command()
@click.argument('task')
def add(task):
    todo_manager.add_todo(task)
    

# List tasks
@cli.command()
@click.option('-s','--status',type=click.Choice(['all','new','inprogress','done'], case_sensitive=False),default='all',help='List tasks based on statuses new,inprogress,done or all together')
def list(status):
    status = status.lower()
    todos = todo_manager.list_todos()
    if status!='all':
        todos = [todo for todo in todos if todo['status']==status]
    for index, todo in enumerate(todos):
        click.echo(f"{index}: {progress_bar[todo['status']]} {todo['task']}")
        
        
# Move tasks between statuses
@cli.command()
@click.argument('index',type=int)
@click.option('-s','--to-status', type=click.Choice(['new','inprogress','done'],case_sensitive=False), required=True, help='Moves task to desired status like new,inprogress,done')
def move(index, to_status):
    todo = todo_manager.update_todo(index, status=to_status.lower())
    click.echo(f"Task '{todo[r'task']}' moved to '{todo[r'status']}")


# Removes tasks from the list
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
        
    