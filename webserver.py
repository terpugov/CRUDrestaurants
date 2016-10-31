#!/usr/bin/env python# -*- coding: utf-8 -*-

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import re

#CRUD operations 
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#query
from sqlalchemy import func
engine = create_engine('sqlite:///restaurant.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()




#from flask.ext.sqlalchemy import SQLAlchemy
class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            restaurants = session.query(Restaurant).all()
            if self.path.endswith("/restaurant"):


                self.send_response(200)
                self.send_header('Content_type', 'text/html')
                self.end_headers()

                restaurants = session.query(Restaurant).all()
                print type(restaurants)
                output = ""
                output = ""
                output += "<html><head><meta http-equiv='Content-Type' content='text/html; charset=utf-8'></head><body>"
                output += "<h1>Restaurant's of Chelyabinsk</h1>"
                output += "<a href = /restaurant/new> Добавить ресторан </a>"
                output += "<table style='width:100%'><tr><th>name</th><th>address</th></tr>"

                for i in restaurants:

                    output += "<tr><td>" + i.name.encode('utf-8')  + "</td>"
                    output += "<td>" +  i.address.encode('utf-8')  + "</td>"
                    output += "<td>" + str(i.id) + "</td>"
                    output += "<td>" + "<a href='/restaurant/" + str(i.id) + "/edit'> edit" + "</td>"
                    output += "<td>" + "<a href='/restaurante/" +str(i.id)+ "/delete'> delete" + "</td>"
                    
                output += "</table></body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith('/delete'):
                restaurant_id_path = self.path.split("/")[2]

                restaurant_id_query = session.query(Restaurant).filter_by(id=restaurant_id_path).all()
                print restaurant_id_path, restaurant_id_query
                if restaurant_id_query != []:
                    self.send_response(200)
                    self.send_header('Content_type', 'text/html')
                    self.end_headers()
                    output = "<html><head><meta http-equiv='Content-Type' content='text/html; charset=utf-8'></head><body>"
                    output += "<h2>Вы уверены, что хотите удалить ресторан?</h2>"
                    output += "<form method='POST' enctype='multipart/form-data' action=/restaurant/" + str(restaurant_id_query[0].id) + "/delete>\
                            <input type = 'submit' value = 'Delete'></form>"
                    self.wfile.write(output)

                return

            if self.path.endswith('/edit'):
                restaurant_id_path = self.path.split("/")[2]

                restaurant_id_query = session.query(Restaurant).filter_by(id=restaurant_id_path).all()
                print restaurant_id_path, restaurant_id_query
                if restaurant_id_query != []:
                    self.send_response(200)
                    self.send_header('Content_type', 'text/html')
                    self.end_headers()
                    output = "<html><head><meta http-equiv='Content-Type' content='text/html; charset=utf-8'></head><body>"
                    output += "<h2>Здесь можно изменить название или адресс ресторана</h2>"
                    output += "<form method='POST' enctype='multipart/form-data' action=/restaurant/" + str(restaurant_id_query[0].id) + "/edit>\
                              <input name='change_name' type='text'\
                              placeholder = 'Change restaurant name' ><input name='change_address' type='text' \
                              placeholder = 'Change address of restaurant' > <input type = 'submit' value = 'Change'></form>"
                    self.wfile.write(output)

                return


            if self.path.endswith("/restaurant/new"): 
                
                self.send_response(200)
                self.send_header('Content_type', 'text/html')
                self.end_headers()
                output = ""
                ouptut = ""
                output += "<html><head><meta http-equiv='Content-Type' content='text/html; charset=utf-8'></head><body>"
                
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurant/new'>\
                        <h2>Добававь новый ресторан?</h2><input name='newRestaurantName' type='text'\
                        placeholder = 'New restaurant name' ><input name='address' type='text' \
                        placeholder = 'Address of restaurant' > <input type = 'submit' value = 'Create'></form>"


                output += "</body></html>"
                self.wfile.write(output)
                return

                
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print dir(self.wfile)
                print output
                return

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)
    def do_POST(self):
        try:
            print self.path

            if self.path.endswith('/delete'):
                
                restaurant_id_path = self.path.split("/")[2]
                restaurant_id_query = session.query(Restaurant).filter_by(id=restaurant_id_path).one()
                session.delete(restaurant_id_query)
                session.commit()
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location','/restaurant')
                self.end_headers()
                return
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                restaurant_id_path = self.path.split("/")[2]
                restaurant = session.query(Restaurant).filter_by(id=restaurant_id_path).one()
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    rest_address = fields.get('change_address')
                    rest_name = fields.get('change_name')
                    rest_address = unicode(rest_address[0],'utf-8')
                    rest_name = unicode(rest_name[0], 'utf-8')
                    restaurant.name = rest_name
                    restaurant.address = rest_address
                    session.add(restaurant)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location','/restaurant')
                    self.end_headers()
            return



            if self.path.endswith("/restaurant/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                print "ctype = %s pdict = %s type(ctype) = %s, ctype == multipart = %s " % (ctype, pdict,type(ctype), ctype == 'multipart/form-data')
                if ctype == 'multipart/form-data':
                    print "Check"
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    rest_address = fields.get('address')
                    rest_name = fields.get('newRestaurantName')
                    print rest_address, type(rest_address)
                    rest_address = unicode(rest_address[0],'utf-8')
                    rest_name = unicode(rest_name[0], 'utf-8')
                    abc = type(rest_name[0])
                    print type(rest_address[0])
                    print "smthg"
                    newRestaurant = Restaurant(name = rest_name, address = rest_address)
                    session.add(newRestaurant)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location','/restaurant/new')
                    self.end_headers()
                    
                    '''output = ""
                    output += "<html><body>"
                    output += "<h2> Okay, you have added newrestaurant: %s </h2> " % messagecontent[0]
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurant/new'><h2>You have added new restaurant</h2><input name='newRestaurantName' type='text' ><input type='submit' value='Submit'> </form>"
                    output += "</body></html>"                
                    self.wfile.write(output)'''
                print "Check after"
            return 
            
        except: 
            pass
            
def main():

    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print "Web server runnunug on port %s" % port

        server.serve_forever()
    except KeyboardInterrupt:
        print "^C entered, stopping web server ..."
        server.socket.close()

if __name__ == '__main__':
    main()
