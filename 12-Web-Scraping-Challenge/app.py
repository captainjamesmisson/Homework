from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app=Flask(__name__)

mongo = PyMongo(app, uri = "mongodb://localhost:27017/mars_db")

@app.route("/")
def home():
        mars_results = mongo.db.mars_results.find_one()
        return render_template("index.html",mars_results=mars_results)

@app.route("/scrape")
def scrape():
    
    mars_results = mongo.db.mars_results
    mars_data=scrape_mars.scrape_nasa_news()
    mars_data=scrape_mars.scrape_nasa_image()
    mars_data=scrape_mars.scrape_mars_twitter()
    mars_data=scrape_mars.scrape_mars_facts()
    mars_data=scrape_mars.scrape_mars_hemisphere()
    mars_results.update({},mars_data,upsert=True)

    return redirect("/",code=302)

if __name__ == '__main__':
    app.run(debug=True)