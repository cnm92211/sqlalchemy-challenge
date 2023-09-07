# Import the dependencies.
from flask import Flask, jsonify
import numpy as np
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base


#################################################
# Database Setup
#################################################

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

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-23").all()
    session.close()
    precipitation = dict(results)
    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station, Station.name).all()
    session.close()
    stations = list(results)
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= "2016-08-23", Measurement.station == 'USC00519281').all()
    session.close()
    tobs_data = dict(results)
    return jsonify(tobs_data)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def start_end(start=None, end=None):
    session = Session(engine)
    if end != None:
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    else:
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close()
    temp_data = list(np.ravel(results))
    return jsonify(temp_data)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)