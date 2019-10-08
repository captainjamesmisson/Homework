from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd

import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database set-up
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect database into a new model
Base = automap_base()
Base.prepare(engine,reflect=True)

# Save reference to tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask set-up
app = Flask(__name__)

# Flask routes
@app.route("/")
def welcome():
    return f"Available Routes:<br/>" f"/api/v1.0/precipitation<br/>\
        "f"/api/v1.0/station<br/>"f"/api/v1.0/tobs<br/>\
        "f"api/v1.0/start<br/>"f"api/v1.0/start/end<br/>"
    
@app.route("/api/v1.0/precipitation/")
def precipitation():
    
    session = Session(engine)
    select_prcp = [Measurement.date, Measurement.prcp]
    
# Define trip start and end dates as well as one-year look-back period based on trip start date
    trip_start = dt.datetime(2015, 1, 1)
    trip_end = dt.datetime(2015,1, 15)
    one_year_ago_start = trip_start-dt.timedelta(days=365)
    # one_year_ago_end = trip_end-dt.timedelta(days=365)

# Design a query to retrieve the last 12 months of precipitation data and plot the results
    trail_one_year_prcp = session.query(*select_prcp).\
    filter(Measurement.date.between(one_year_ago_start, trip_start)).\
    group_by(Measurement.date).all()

    session.close()

# Convert the query results to a Dictionary using date as the key and prcp as the value
    prcp_data = []
    for date, prcp in trail_one_year_prcp:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_data.append(prcp_dict)

#  Return the JSON representation of your dictionary       
    return jsonify(prcp_data)

@app.route("/api/v1.0/station/")
def station():
    
    session = Session(engine)

# Design a query to show  available stations in dataset
    stations = session.query(Station.station).all()
   
    session.close()

#  Return the JSON representation of query results           
    return jsonify(stations)

@app.route("/api/v1.0/tobs/")
def tobs():
    
    session = Session(engine)
    select_tobs = [Measurement.date, Measurement.tobs]

# Design a query for the dates and temperature observations from a year from the last data point    
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    most_recent_date = dt.datetime(2017,8,23) 
    # hard-coding most_recent_date not ideal, how to properly fix?
    one_year_ago= most_recent_date-dt.timedelta(days=365)
    trail_one_year_tobs = session.query(*select_tobs).\
    filter(Measurement.date.between(one_year_ago, most_recent_date)).\
    group_by(Measurement.date).all()

    session.close()
    
# Convert the query results to a Dictionary using date as the key and prcp as the value
    tobs_data = []
    
    for date, tobs in trail_one_year_tobs:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_data.append(tobs_dict)

# Return a JSON list of Temperature Observations (tobs) for the previous year    
    return jsonify(tobs_data)


@app.route("/api/v1.0/<start_date>")
def start(start_date):
    
    session = Session(engine)
    
    select_start = [Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs),\
    func.max(Measurement.tobs)]
    select_start_results = (session.query(*select_start).filter(func.strftime("%Y-%m-%d", Measurement.date) >= start_date)\
    .group_by(Measurement.date).all())

    session.close()

    start_dates = []                       
    
    for result in select_start_results:
        start_dict = {}
        start_dict["Date"] = result[0]
        start_dict["Low Temp"] = result[1]
        start_dict["Avg Temp"] = result[2]
        start_dict["Max Temp"] = result[3]
        start_dates.append(start_dict)
    
    return jsonify(start_dates)

@app.route("/api/v1.0/<start_date>/<end_date>")
def startend(start_date, end_date):
    
    session = Session(engine)
    
    select_start_end = [Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    select_start_end_results = (session.query(*select_start_end).filter(func.strftime("%Y-%m-%d", Measurement.date)\
    >= start_date).filter(func.strftime("%Y-%m-%d", Measurement.date) <= end_date).\
    group_by(Measurement.date).all())

    session.close()

    start_end_dates = []                       
    
    for result in select_start_end_results:
        start_end_dict = {}
        start_end_dict["Date"] = result[0]
        start_end_dict["Low Temp"] = result[1]
        start_end_dict["Avg Temp"] = result[2]
        start_end_dict["Max Temp"] = result[3]
        start_end_dates.append(start_end_dict)
    
    return jsonify(start_end_dates)
    
if __name__ == "__main__":
    app.run(debug=True)