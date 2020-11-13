#! /usr/local/bin/python
# -*- coding: utf-8 -*-
from calendar import timegm
from contextlib import contextmanager
from datetime import datetime
import _strptime  # https://bugs.python.org/issue7980
from flask import Flask, request, jsonify, _app_ctx_stack
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from models.models import Base, Sensor, LoraEvent

db_url = "sqlite:///../ttn/src/sensors/target/data/lora.mqtt.db"
engine = create_engine(db_url, echo=False)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = Flask(__name__)
app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)
app.debug = True


@contextmanager
def session_scope():
    """ Provide a transactional scope around a series of operations"""
    session = app.session
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def convert_to_time_ms(timestamp):
    return 1000 * timegm(datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ').timetuple())


@app.route('/')
def health_check():
    with session_scope() as session:
        sensors = session.query(Sensor).all()
        lora_events = session.query(LoraEvent).all()
    return f'This datasource is healthy. There are {len(sensors)} sensors and {len(lora_events)} Lora Events'


@app.route('/search', methods=['POST'])
def search():
    return jsonify(['my_series', 'another_series'])


@app.route('/query', methods=['POST'])
def query():
    req = request.get_json()
    data = [
        {
            "target": req['targets'][0]['target'],
            "datapoints": [
                [861, convert_to_time_ms(req['range']['from'])],
                [767, convert_to_time_ms(req['range']['to'])]
            ]
        }
    ]
    return jsonify(data)


@app.route('/annotations', methods=['POST'])
def annotations():
    req = request.get_json()
    data = [
        {
            "annotation": 'This is the annotation',
            "time": (convert_to_time_ms(req['range']['from']) +
                     convert_to_time_ms(req['range']['to'])) / 2,
            "title": 'Deployment notes',
            "tags": ['tag1', 'tag2'],
            "text": 'Hm, something went wrong...'
        }
    ]
    return jsonify(data)


@app.route('/tag-keys', methods=['POST'])
def tag_keys():
    data = [
        {"type": "string", "text": "City"},
        {"type": "string", "text": "Country"}
    ]
    return jsonify(data)


@app.route('/tag-values', methods=['POST'])
def tag_values():
    req = request.get_json()
    if req['key'] == 'City':
        return jsonify([
            {'text': 'Tokyo'},
            {'text': 'São Paulo'},
            {'text': 'Jakarta'}
        ])
    elif req['key'] == 'Country':
        return jsonify([
            {'text': 'China'},
            {'text': 'India'},
            {'text': 'United States'}
        ])

def main():
    print("Running the main program")
    app.run(host='192.168.1.16', port='8080')


if __name__ == '__main__':
    print("Running the main")
    main()