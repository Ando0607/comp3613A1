from .user import create_user
from App.database import db
from App.models import *
import json

def readfile():
  
    with open('comp.json', 'r') as myfile:
        data = myfile.read()
        obj = json.loads(data)  

      
        for competition_data in obj:
            title = competition_data['title']
            date = competition_data['date']
            description = competition_data['description']

            
            new_competition = Competition(title=title, description=description, date=date)
            db.session.add(new_competition)
            db.session.commit()  

           
            for rank, participant_name in competition_data['participants'].items():
               
                user = User.query.filter_by(username=participant_name).first()
                if not user:
                    user = User(username=participant_name, password="defaultpassword")  
                    db.session.add(user)
                    db.session.commit()

                
                competition_entry = UserCompetition(
                user_id=user.id, 
                competition_id=new_competition.id,  
                placement=int(rank)
                )
                db.session.add(competition_entry)

            db.session.commit()  

    print("Competitions and participants added to the database.")
    


def initialize():
    db.drop_all()
    db.create_all()
    readfile()
