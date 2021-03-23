from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

def home():

    # Find one record of data from the mongo database
    data = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", data=data)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    mars_db = mongo.db.mars
    # Run the scrape function
    mars_data = scrape_mars.scrape()
    print(mars_data)
    # Update the Mongo database using update and upsert=True
    mars_db.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)