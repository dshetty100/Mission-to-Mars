from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

# Use flask_pymongo to connect to mongo to reach database named "mars_app" that we created earlier.
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# define the route for the HTML page
@app.route("/") # tells Flask what to display when we're looking at the home page, index.html 
def index():
   mars = mongo.db.mars.find_one() # uses PyMongo to find the "mars" collection in our database, which we will create when we convert our Jupyter scraping code to Python Script.
   return render_template("index.html", mars=mars) # tells Flask to return an HTML template using an index.html file, & tells Python to use the "mars" collection in MongoDB.


@app.route("/scrape") # This route, “/scrape”, will run the function that we create just beneath it.
def scrape():
   mars = mongo.db.mars # assign a new variable to access the mongo database
   mars_data = scraping.scrape_all() # create a new variable to hold newly scrapped data using "scrape_all" function and scraping.py script that we created earlier
   mars.update({}, mars_data, upsert=True) # update the database
   return redirect('/', code=302)  # return a message when successful

# tell flask to run the app
if __name__ == "__main__":
   app.run()
