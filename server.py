import traceback
from pymongo import MongoClient
from flask import Flask, request , Response, send_from_directory, render_template
import uuid
from bson.json_util import dumps
import datetime as dt
import logging


logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level="DEBUG")

"""
    app configurations.
"""
app = Flask(__name__, static_folder="static")
client = MongoClient('mongodb://localhost:27017/',connect=False)
db = client.stbtester


"""
 stbt routes
"""


@app.route("/stbt/newjob/<job_name>", methods=["POST"])
def new_job(job_name):
    if request.method == 'POST':
        try:
            # Generate UUID
            new_job_uuid = str(uuid.uuid1())
            job_id = new_job_uuid
            # persist in db
            record_inserted = db.test_job.insert_one({'job_name': job_name, 'job_id': job_id}).inserted_id
            return dumps({'status': True, 'job_id': job_id, 'job_name': job_name})
        except Exception as e:
            traceback.print_exc()
            return Response({'status': False, 'message': 'Error, contact support'}, status=500,
                            mimetype='application/json')
    else:
        return Response({'status': False, 'message': 'invalid request method'}, status=403,
                        mimetype='application/json')


@app.route("/stbt/test/results/<job_id>", methods=["GET"])
def get_results(job_id):
    if request.method == 'GET':
        try:
            # persist in db
            records = db.test_results.find({'job_id': job_id}, {'_id': 0})
            # return_data = records
            # return_data[0]["time"] = records[0]["time"].strftime("%Y-%m-%dT%H-%M-%S")
            # print(return_data[0]["time"])
            return dumps({'status': True, 'data': records})
        except Exception as e:
            traceback.print_exc()
            return Response({'status': False, 'message': 'Error, contact support'}, status=500,
                            mimetype='application/json')
    else:
        return Response({'status': False, 'message': 'invalid request method'}, status=403,
                        mimetype='application/json')


@app.route("/stbt/test/results/", methods=["POST"])
def insert_result():
    if request.method == 'POST':
   	data = request.args
        try:
            print("data : {}".format(data))
	    time_parm = data['time'].encode('ascii','ignore')
	    job_id_parm = data['job_id'].encode('ascii','ignore')
	    test_no_parm = data['test_number'].encode('ascii','ignore')
	    test_result_parm = data['result'].encode('ascii','ignore')
	    test_link_parm = data['test_link'].encode('ascii','ignore')
	    name_parm =data['name'].encode('ascii','ignore')
	    reason_parm = data['failure_reason'].encode('ascii','ignore')

            date_time = dt.datetime.strptime(time_parm, "%Y-%m-%dT%H:%M:%S")
            results = db.test_results.insert_one({'job_id': job_id_parm, 'time': date_time,
                                                  'test_number': test_no_parm,
                                                  'name': name_parm, 'result': test_result_parm,
                                                  'test_link': test_link_parm,
                                                  'reason': reason_parm},
                                                 ).inserted_id
            print(results)
            return dumps({'status': True, 'message': 'success'})
        except Exception as e:
            traceback.print_exc()
            return Response({'status': False, 'message': 'Error, contact support'}, status=500,
                            mimetype='application/json')
    else:
        return Response({'status': False, 'message': 'invalid request method'}, status=403,
                        mimetype='application/json')


@app.route("/")
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
