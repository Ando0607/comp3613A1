
import json
from flask import current_app as app
from App import db
from App.models import Competition, User, UserCompetition

def import_results_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        return f"File '{file_path}' not found."
    except json.JSONDecodeError:
        return f"Error decoding JSON from '{file_path}'."

    for competition_data in data:
        title = competition_data['title']
        date = competition_data['date']
        description = competition_data['description']
        
        competition = Competition.query.filter_by(title=title, date=date).first()
        if not competition:
            competition = Competition(title=title, description=description, date=date)
            db.session.add(competition)
            db.session.commit()
        
        for rank, participant_name in competition_data['participants'].items():
            user = User.query.filter_by(username=participant_name).first()
            if not user:
                user = User(username=participant_name, password="defaultpassword")
                db.session.add(user)
                db.session.commit()
            
            existing_entry = UserCompetition.query.filter_by(user_id=user.id, competition_id=competition.id).first()
            if not existing_entry:
                competition_entry = UserCompetition(
                    user_id=user.id,
                    competition_id=competition.id,
                    placement=int(rank)  
                )
                db.session.add(competition_entry)
        db.session.commit()
    return f"Competition results from '{file_path}' have been imported successfully."


def create_competition(title, description, date):
    new_competition = Competition(
        title=title,
        description=description,
        date=date
    )
    db.session.add(new_competition)
    db.session.commit()
    return f"Competition '{title}' created successfully!"


def add_participant_to_competition(competition_id, username, placement):
    competition = Competition.query.get(competition_id)
    if not competition:
        return f"Competition with ID {competition_id} not found."
    
    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(username=username, password="defaultpassword")
        db.session.add(user)
        db.session.commit()
    
    existing_entry = UserCompetition.query.filter_by(user_id=user.id, competition_id=competition_id).first()
    if existing_entry:
        return f"User '{username}' is already participating in this competition."

    new_participant = UserCompetition(
        user_id=user.id,
        competition_id=competition.id,
        placement=placement
    )
    db.session.add(new_participant)
    db.session.commit()
    return f"Added '{username}' to competition '{competition.title}' with placement {placement}."


def view_competitions():
    competitions = Competition.query.all()
    
    if not competitions:
        return "No competitions found."
    
    competitions_list = [f"- {comp.id}: {comp.title} ({comp.date}) - {comp.description}" for comp in competitions]
    return "\n".join(competitions_list)


def view_competition_results(competition_id):
    competition = Competition.query.get(competition_id)
    if not competition:
        return "Competition not found."
    
    results = UserCompetition.query.filter_by(competition_id=competition_id).all()
    
    if not results:
        return f"No results found for competition: {competition.title}"
    
    result_list = [f"- {User.query.get(result.user_id).username}: Placement {result.placement}" for result in results]
    return f"Results for {competition.title} (ID: {competition.id})\n" + "\n".join(result_list)


