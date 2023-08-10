import json
import os

#globals
nodes = {}
dotCode = ""
simulatedTime = 0
simulatedStates = {}
realStates = {}

#object declaration for node information
class DataObject:
    def __init__(self, id):
        self.id = id
        self.states = {}
        self.realTimes = {}

    def add_state(self, simulatedTime, trait, timestamp, data):
        if simulatedTime not in self.states:
            self.states[simulatedTime] = []
            simulatedStates[simulatedTime] = []
        self.states[simulatedTime].append({trait: {timestamp: data}})
        simulatedStates[simulatedTime].append({self.id: {trait: {timestamp: data}}})

    def add_real_time(self, timestamp, data):
        self.realTimes[timestamp] = data
        realStates[timestamp] = {self.id: data}

    def get_state_at_time(self, time):
        return self.states.get(time)

    def get_states_in_range(self, start, end):
        return {time: self.states[time] for time in range(start, end+1) if time in self.states}
    
    def get_realTimes_in_range(self, start, end):
        start = int(start)
        end = int(end)
        return {int(time): self.realTimes[time] for time in self.realTimes.keys() if start <= int(time) <= end}
    
    def get_all_states(self):
        return self.states
    
    def get_all_realTimes(self):
        return self.realTimes


color_dict = {
    "GeneratorContext": "red"
}

#reads in a specific file and fills in the appropriate information of the Nodes object
#returns: nodes variable
def read_json_file(file_name, trait, nodeName):
        global simulatedTime
        if nodeName not in nodes:
            nodes[nodeName] = DataObject(nodeName)
        
        data_object = nodes[nodeName]

        with open(file_name, 'r') as f:
            for line in f:
                timestamp, json_str = line.split('\t', 1)
                timestamp = timestamp.strip('[]')
                data = json.loads(json_str)
                data_object.add_real_time(timestamp, data)
                if "Incr" in data:
                    simulatedTime += data["Incr"]
                #handles third type of file
                if "Created" in data:
                    creationType = data["Created"]  # Update the creationType variable
                    createDotRepresentation(nodeName, trait, creationType)
                    return nodes
                data_object.add_state(simulatedTime, trait, timestamp, data)
            return nodes
        
def extractNames(filePath):
    fileName = os.path.basename(filePath)
    fileName = fileName.split("_")
    nodeName = fileName[0] + "_" + fileName[1]
    if ".json" in nodeName:
        nodeName = nodeName.replace(".json", "")
    trait = fileName[-1].replace(".json", "")
    return trait, nodeName

#helper function for reading in a single file to create the DOT
def createDotRepresentation(nodeName, trait, creationType):
    global dotCode  # Declare 'dotCode' as a global variable within the function
    label = f' "nodeName: {nodeName}\\ncreationType: {creationType}" '
    color = color_dict[creationType]
    dotCode += f"   {trait} [label={label}color={color} shape=box style=filled id={trait}]\n"
    

def get_dot_code():
    return dotCode

def get_global_states_in_range(states_dict, start, end):
    start = int(start)
    end = int(end)
    return {int(time): states_dict[time] for time in states_dict.keys() if start <= int(time) <= end}

def read_all_json_files_in_directory(directory):
    global nodes, dotCode
    dotCode = 'digraph SAM {\n'
    file_paths = [os.path.join(directory, file_name) for file_name in os.listdir(directory)]
    for file_path in file_paths:
        if file_path.endswith(".json"):
            trait, nodeName = extractNames(file_path)
            nodes = read_json_file(file_path, trait, nodeName)
    dotCode += '}'

directories = ["/home/pbeni/Research/damLogs-graphviz/practiceLogs"]
for directory in directories:
    read_all_json_files_in_directory(directory)

#print(simulatedStates)
print(realStates)
