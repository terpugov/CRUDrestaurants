from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
import datetime
from sqlalchemy import func
engine = create_engine('sqlite:///restaurant.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

 
restaurants = session.query(Restaurant).all()
restaurants = session.query(Restaurant).filter_by(id=3).all()

for restaurant in restaurants:
    print restaurant.name, restaurant.address


    

'''puppies = session.query(Puppy.name, Puppy.date_of_birth).filter(Puppy.date_of_birth > today - month6).order_by(Puppy.date_of_birth.desc())

for i in puppies:
    print i[0], i[1]



puppies = session.query(Puppy.name, Puppy.weight).order_by(Puppy.weight)

for i in puppies:
    print i[0], i[1]
        


def query_four():
    """Query all puppies grouped by the shelter in which they are staying"""
    result = session.query(Shelter, func.count(Puppy.id)).join(Puppy).group_by(Shelter.id).all()
    for item in result:
        print item[0].id, item[0].name, item[1]

query_four()
'''    


 








