import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt


from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Precipitation = Base.classes.prcp

app = Flask(__name__)



@app.route("/")
def home():
      return 
        f"Welcome to Weather Data!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"




@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    results = session.query(*sel).\
        filter(Measurement.date >= year_ago).\
        filter(Measurement.date <= last_date).\
        order_by(Measurement.date).all()


    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    precipitation = []
    for date, precipitation in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = precipitation
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    
    stations = session.query(Measurement.station).group_by(Measurement.station).all()
    
    session.close()

       return jsonify(stations)
    
    
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date = dt.datetime(2017, 8, 23)
    year_ago = last_date - dt.timedelta(days=365)
    
    annual_tobs = session.query(Measurement.tobs).\
        filter(Measurement.date >= year_ago).\
        filter(Measurement.date <= last_date).\
        all()
    
    return jsonify(annual_tobs)


@app.route("/api/v1.0/<start>")
def start(start_date):
    session = Session(engine)
    
    start =  session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    
    return jsonify(start)
    
@app.route("/api/v1.0/<start>/<end>")
def start_end((start_date, end_date):
    session = Session(engine)
    start_end = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
              
      return jsonify(start_end)

if __name__ == "__main__":
    app.run(debug=True)
