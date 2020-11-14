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
