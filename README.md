# sensor-datasource

A Flask App will provide a REST API to access the data that is collected by the ttn-explore program. The API will be that required by the Grafana 
SimpleJSONDataSource.

Grafana will be run in docker container in a Windows 10 VM on the iMac; and the Flask App inside PyCharm on the same iMac host (not the VM). 

`docker run -d -p 3000:3000 --name=grafana -e 'GF_INSTALL_PLUGINS=grafana-simple-json-datasource' grafana/grafana`

Then access it from Safari running in OSX like this: 

`http://<my mac ip address>:3000/`
  
  use admin/admin for first access changing the password after that to the usual one.

The Flask application is running on the Pycharm on the local host but is listening to 127.0.0.1 which means it is not accessible from the VM; so will
need to make the flask app listen on 0.0.0.0

Within PyCharm flask is run using the command-line, need to add --host 0.0.0.0 to the run configuration.

https://github.com/Jonnymcc/grafana-simplejson-datasource-example

The URL to put into Grafana for the datasource needs to use a hostname that works from the VM: [http://`hostname`:5000](http://`hostname`:5000) but I have found that it is a bit unreliable. Click "Save and Test" and sometimes it is ok and sometimes not.  Note; this is the URL that Grafana will use to reach the datasource so it needs to be a host that is accessible to Grafana.

To summarize, this flow is :

1. Grabbed from TTN via MQTT and stored to a SQLite database
2. Made available as a JSON datasource via a Flask App running locally on port 5000
3. Grabbed from the datasource and visualized by Grafana running on a Windows 10 VM on port 3000

