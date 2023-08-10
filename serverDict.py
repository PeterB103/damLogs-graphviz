from flask import Flask, jsonify, request
from flask_cors import CORS
import parseFile
import sys

app = Flask(__name__)
CORS(app)  # Allows cross-origin requests

@app.route('/data/<data_type>', methods=['GET'])
def get_data(data_type):
    # Collect the start and end times from the URL query parameters
    start_time = int(request.args.get('start', 0))
    end_time = int(request.args.get('end', 0))

    if data_type == "states":
        # Now states in range will contain both Sender and TimeManager data.
        #simulatedStatesInRange = parseFile.nodes["ID_0"].get_states_in_range(start_time, end_time)
        simulatedStates = parseFile.simulatedStates
        simulatedStatesInRange = parseFile.get_global_states_in_range(simulatedStates, start_time, end_time)
        return jsonify(simulatedStatesInRange)
    
    else:
        #realTimesInRange = parseFile.nodes["ID_0"].get_realTimes_in_range(start_time, end_time)
        realStates = parseFile.realStates
        realTimesInRange = parseFile.get_global_states_in_range(realStates, start_time, end_time)
        return jsonify(realTimesInRange)
 

@app.route('/all_data/<data_type>', methods=['GET'])
def get_all_data(data_type):
    if data_type == "states":
        # Now states in range will contain both Sender and TimeManager data.
        #allStates = parseFile.nodes["ID_0"].get_all_states()
        allStates = parseFile.simulatedStates
        return jsonify(allStates)
        
    else:
         #realTimes = parseFile.nodes["ID_0"].get_all_realTimes()
         realTimes = parseFile.realStates
         return jsonify(realTimes)


@app.route('/dotCode', methods=['GET'])
def get_dot_code():
    return parseFile.get_dot_code()

if __name__ == '__main__':
    app.run(port=5000)
