from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Restaurant, MenuItem
#from flask.ext.sqlalchemy import SQLAlchemy
from random import randint
import datetime
import random
import json 
engine = create_engine('sqlite:///restaurant.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

f = open('json.txt', 'r')
loaded = json.load(f)
#print a
#print type(a)
restaurante = []
for i in loaded[u'results']:
    new_restaurante = Restaurant(name = i[u'name'], address =  i[u'formatted_address'])
    session.add(new_restaurante)
    session.commit()
    






