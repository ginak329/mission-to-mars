from flask import Flask, render_template, redirect
import pymongo

app = Flask(__name__)

# setup mongo connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)


@app.route("/")
def index():
    mars_dict = client.db.mars.find_one()
    
    # render an index.html template and pass it the data you retrieved from the database
    return render_template("index.html", mars_dict=mars_dict)

@app.route("/scrape")
def scrape():
    import scrape_mars_test
    mars = client.db.mars 
    mars_data = scrape_mars_test.scrape()
    mars.replace_one({}, mars_data, upsert=True)
    return redirect("http://localhost:6969/", code=302)



if __name__ == "__main__":
    app.run(debug=True, port=6969)
