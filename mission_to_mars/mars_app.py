#Import relevant dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

#Create a Flask app
app = Flask(__name__)

#Go into MongoDB and create a mars_app db
#Find local host address
#Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#Create app route to show homepage of index.html that uses data from MongoDB mars_app
@app.route("/")
def index():

    #Identify a random record of data from the mongo database (mars_app)
    mars = mongo.db.mars.find_one()
    #Return template and data
    return render_template("index.html", mars=mars)

#Create app route to scrape data using code from scrape file
@app.route("/scrape")
def scrape():
  
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    #Update the Mongo database using update and upsert=True. {} is when there is no condition for the query
    mars.update({}, mars_data, upsert=True)
    #Return to the homepage app
    return "successful"

#Standard end of flask code to run flask app
if __name__ == "__main__":
    app.run(debug=True)