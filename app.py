import datetime as dt 
import numpy as np

import sqlalchemy 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session 
from sqlalchemy import create_engine, func


from flask import Flask, jsonify 


engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def home():
    print("Server received request")
    return (
    f"Available Routes:<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations"
    f"/api/v1.0/tobs" )

@app.route("/api/v1.0/precipitation")
def precipitation():
    p_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= p_year).all()
    p_dict = {date: prcp for date, pcrp in precipitation}
    return jsonify(p_dict)

@app.route("/api/v1.0/stations")
def stations():
    data_stat = session.query(Station.station).all()
    stations = list(np.ravel(data_stat))
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    data_tobs = session.query(Measurement.tobs)
    tobs = list(np.ravel(data_tobs))
    return jsonify(tobs)

if __name__ == '__main__':
    app.run()
