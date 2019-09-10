from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")


@app.route("/")
def index():

    # Find one record of data from the mongo database
    news = mongo.db.latest_news.find_one({},{"title":1})

    # Return template and data
    return render_template("index.html", news=news)
# def echo():
#     return render_template("index.html", text="Serving up cool text from the Flask server!!")

@app.route("/scrape")
def scrape():

    # Run the scrape function
    scrape_mars.scrape_to_db()

    # Update the Mongo database using update and upsert=True
    # mongo.db.collection.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
