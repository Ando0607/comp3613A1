import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import *
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )
from App.controllers.competition import (
    import_results_from_file,
    create_competition,
    add_participant_to_competition,
    view_competitions,
    view_competition_results
)


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli



#import results from file
@app.cli.command("import-results")
@click.argument("file_path")
def import_results(file_path):
    result_message = import_results_from_file(file_path)
    click.echo(result_message)

#create competition
@app.cli.command("create-competition")
@click.argument("title")
@click.argument("description")
@click.argument("date")
def create_competition_cmd(title, description, date):
    result_message = create_competition(title, description, date)
    click.echo(result_message)

#add participant to a competition
@app.cli.command("add-participant")
@click.argument("competition_id")
@click.argument("username")
@click.argument("placement", type=int)
def add_participant(competition_id, username, placement):
    result_message = add_participant_to_competition(competition_id, username, placement)
    click.echo(result_message)

#view competitions list
@app.cli.command("view-competitions")
def view_competitions_list():
    competitions_list = view_competitions()
    click.echo(competitions_list)

#view competition results
@app.cli.command("view-competition-results")
@click.argument("competition_id")
def view_competition_results_cmd(competition_id):
    result_message = view_competition_results(competition_id)
    click.echo(result_message)
    


'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)