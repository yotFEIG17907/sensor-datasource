# sensor-datasource

A Flask App will provide a REST API to access the data that is collected by the ttn-explore program. The API will be that required by the Grafana 
SimpleJSONDataSource. I started running these applications in Docker Desktop for Windows in a Windows 10 VM on the MAC (which I had installed for other reasons). But then I hit some weird problem executing the Docker Run command to run Graphite; it just wouldn't parse the port mappings, e.g. -p 80:80. So I uninstalled Docker Desktop for Windows and installed Docker Desktop for the MAC directly. (Incidentally, I got the same problem with the command-line for graphite on the MAC; so I switched to using a compose file for both)

Grafana will be run in docker container in Docker Desktop for the MAC; and the Flask App inside PyCharm on the same iMac host (not the VM). 

`docker run -d -p 3000:3000 --name=grafana -e 'GF_INSTALL_PLUGINS=grafana-simple-json-datasource' grafana/grafana`

Then access it from Safari running in OSX like this: 

`http://<my mac ip address>:3000/`
  
  use admin/admin for first access changing the password after that to the usual one.

The Flask application is running on the Pycharm on the local host but is listening to 127.0.0.1 which means it is not accessible from the VM; so will
need to make the flask app listen on 0.0.0.0

Within PyCharm flask is run using the command-line, need to add --host 0.0.0.0 to the run configuration.

https://github.com/Jonnymcc/grafana-simplejson-datasource-example

The URL to put into Grafana for the datasource needs to use a hostname that works from the VM: [http://hostname:5000](http://hostname:5000) but I have found that it is a bit unreliable. When I started grafana using a compose file I found I had to use the IP address. Click "Save and Test" and sometimes it is ok and sometimes not.  Note; this is the URL that Grafana will use to reach the datasource so it needs to be a host that is accessible to Grafana.

To summarize, this first flow is :

1. Grabbed from TTN via MQTT and stored to a SQLite database
2. Made available as a JSON datasource via a Flask App running locally on port 5000
3. Grabbed from the datasource and visualized by Grafana running on a Windows 10 VM on port 3000

Next I want try sending the data to Graphite and using either Graphite's own dashboard to view the graphs or use Graphite as a DataSource into Grafana.

## Docker Compose for running Grafana and Graphite

Information on Graphite: [https://hub.docker.com/r/graphiteapp/graphite-statsd/](https://hub.docker.com/r/graphiteapp/graphite-statsd/)

I left the internal GUNICORN port 8080 unexposed; and externally use port 8080 to access the Graphite dashboard

```yaml
version: "3"
services:
  # Install the Simple JSON Datasource
  grafana:
    image: grafana/grafana
    environment:
    - GF_INSTALL_PLUGINS=grafana-simple-json-datasource
    container_name: grafana
    restart: always
    ports:
      - 3000:3000
    networks:
      - grafana-net
    volumes:
      - grafana-volume

  graphite:
    image: graphiteapp/graphite-statsd
    container_name: graphite
    restart: always
    ports:
    ports:
      - 8080:80
      - 2003:2003
      - 2004:2004
      - 2023:2023
      - 2024:2024
      - 8125:8125
      - 8126:8126
    networks:
      - grafana-net

networks:
  grafana-net:

volumes:
  grafana-volume:
    external: true
```

