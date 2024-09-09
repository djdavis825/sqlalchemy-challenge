# Import the dependencies.
from flask import Flask, jsonify

import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

app = Flask(__name__)

# connect to database
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# home route
@app.route("/")
def home():
    return(
        f"<center><h2>Welcome to the Hawaii Climate Analysis Local API!</h2></center>"
        f"<center><h3>Select from one of the available routes:</h3></center>"
        f"<center>/api/v1.0/precipitation</center>"
        f"<center>/api/v1.0/stations</center>"
        f"<center>/api/v1.0/tobs</center>"
        f"<center>/api/v1.0/start/end</center>"
    )

# /api/v1.0/precipitation
@app.route("/api/v1.0/precipitation")
def precip():
    # return as json
    # Calculate the date one year from the last date in data set.
    prevYear = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prevYear).all()

    session.close()
    #dictionary w date as key
    precipitation = {date: prcp for date, prcp in results}
    #convert to json
    return jsonify(precipitation)

# /api/v1.0/stations
@app.route("/api/v1.0/stations")
def stations():
    # list of stations
    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Station.station).all()
    session.close()

    stationList = list(np.ravel(results))

    # jsonify and display
    return jsonify(stationList)

# /api/v1.0/tobs
@app.route("/api/v1.0/tobs")
def temperatures():
    # return prev year temps
    # Calculate the date one year from the last date in data set.
    prevYear = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    results = results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prevYear).all()

    session.close()

    tempList = list(np.ravel(results))

    # return list of temps
    return jsonify(tempList)

# /api/v1.0/start/end
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def dateState(start=None, end=None):

    # select statement
    selection = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]

    if not end:

        startDate = dt.datetime.strptime(start, "%m%d%Y")

        results = session.query(*selection).filter(Measurement.date >= startDate).all()

        session.close()

        tempList = list(np.ravel(results))

        # return list of temps
        return jsonify(tempList)
    
    else:

        startDate = dt.datetime.strptime(start, "%m%d%Y")
        endDate = dt.datetime.strptime(end, "%m%d%Y")

        results = session.query(*selection)\
            .filter(Measurement.date >= startDate)\
            .filter(Measurement.date >= endDate).all()

        session.close()

        tempList = list(np.ravel(results))

        # return list of temps
        return jsonify(tempList)

# app launcher
if __name__ == '__main__':
    app.run(debug=True)


#################################################
# Database Setup
#################################################


# reflect an existing database into a new model

# reflect the tables


# Save references to each table


# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################




#################################################
# Flask Routes
#################################################
