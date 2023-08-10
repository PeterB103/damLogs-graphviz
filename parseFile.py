import json
import os
import sqlite3

#globals
dotCode = ""
unique_labels = set()
simulatedTime = 0

color_dict = {
    "GeneratorContext": "red",
    "Array": "green",
    "CompressedCrdRdScan": "green",
    "CompressedWrScan": "orange",
    "Union": "purple"
}

def clear_database(conn):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM nodes;")
    conn.commit()

def read_json_file_and_fill_database(conn, file_name, trait, node_name):
    global simulatedTime, dotCode
    cursor = conn.cursor()
    data_to_insert_batch = []

    with open(file_name, 'r') as f:
        for line in f:
            timestamp, json_str = line.split('\t', 1)
            timestamp = int(timestamp.strip('[]'))
            data = json.loads(json_str)

            # Time adjustment
            if "Incr" in data:
                simulatedTime += data["Incr"]
                cursor.execute("""
                    UPDATE nodes
                    SET simulated_time = simulated_time + ?
                    WHERE trait = 'Sender' AND CAST(timestamp AS INTEGER) > ?
                """, (data["Incr"], timestamp))

            # Dot representation creation
            if "Created" in data:
                createDotRepresentation(node_name, trait, data["Created"])
            elif "Send" in data:
                createDotRepresentation(node_name, trait, data["Send"], "Send")
            elif "Recv" in data:
                createDotRepresentation(node_name, trait, data["Recv"], "Recv")

            # Batch data for insertion
            data_to_insert_batch.append((node_name, trait, str(timestamp), json_str.strip(), simulatedTime))

    # Batch insert data into the database
    cursor.executemany("INSERT INTO nodes (node_name, trait, timestamp, data, simulated_time) VALUES (?, ?, ?, ?, ?)", data_to_insert_batch)
    conn.commit()


def extractNames(filePath):
    fileName = os.path.basename(filePath)
    fileName = fileName.split("_")
    node_name = fileName[0] + "_" + fileName[1]
    if ".json" in node_name:
        node_name = node_name.replace(".json", "")
    trait = fileName[-1].replace(".json", "")
    return trait, node_name


def createDotRepresentation(node_name, trait, creationType, key = None):
    global dotCode
    global unique_labels

    if key == "Send":
        reciever_node = creationType["id"]
        node_number = int(str(node_name).split("_")[1])
        label = f' "Send: {node_number} to {reciever_node}" '
        line = f"   {node_number} -> {reciever_node} [label = {label}]\n"
        if line not in unique_labels:  # Check if the line has not been added before
            dotCode += line
            unique_labels.add(line)  # Add the line to the set of unique lines
    elif key == "Recv":
        reciever_node = creationType["id"]
        node_number = int(str(node_name).split("_")[1])
        label = f' "{node_number} receiving from {reciever_node}" '
        line = f"   {reciever_node} -> {node_number} [label = {label}]\n"
        if line not in unique_labels:  # Check if the line has not been added before
            dotCode += line
            unique_labels.add(line)  # Add the line to the set of unique lines
    else:
        label = f' "nodeName: {node_name}\\ncreationType: {creationType}" '
        color = color_dict[creationType]
        dotCode += f"   {trait} [label={label}color={color} shape=box style=filled id={trait}]\n"


def read_all_json_files_in_directory(directory):
    file_paths = [os.path.join(directory, file_name) for file_name in os.listdir(directory)]
    for file_path in file_paths:
        if file_path.endswith(".json"):
            trait, node_name = extractNames(file_path)
            read_json_file_and_fill_database(conn, file_path, trait, node_name)

conn = sqlite3.connect('data.db')
clear_database(conn)  # Call the function to clear the database before inserting new data

#use for debugging
#directories = ["/home/pbeni/Research/damLogs-graphviz/addLogs/addLogs/baseCaseLogs"] 

#medium test case
directories = ["/home/pbeni/Research/damLogs-graphviz/practiceLogs"]

#stress test 
#directories = ["/home/pbeni/Research/damLogs-graphviz/addLogs/addLogs/log"]

for directory in directories:
    dotCode = 'digraph SAM {\n'
    unique_labels = set()
    read_all_json_files_in_directory(directory)
    dotCode += '}'
conn.close()

print(dotCode)
