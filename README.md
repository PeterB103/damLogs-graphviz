# damLogs-graphviz
#Initialize the DB, Server, and HTMl using the following 
#click on link and go to /data
export FLASK_APP=server
flask run

#local server for html
python3 -m http.server 8000 

#start the SQL web server
sqlite_web data.db
