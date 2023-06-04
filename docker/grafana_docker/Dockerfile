# Use a base image for Raspberry Pi OS (Debian-based)
FROM 2000cubits/raspbian:buster

# Install dependencies
RUN apt-get update && apt-get install -y wget apt-transport-https

# Add the APT key used to authenticate packages
RUN wget -q -O - https://packages.grafana.com/gpg.key | apt-key add -

# Add the Grafana APT repository
RUN echo "deb https://packages.grafana.com/oss/deb stable main" | tee -a /etc/apt/sources.list.d/grafana.list

# Install Grafana
RUN apt-get update && apt-get install -y grafana

# Expose Grafana port
EXPOSE 3000

# Start the Grafana server
CMD grafana-server --config=/etc/grafana/grafana.ini --homepath=/usr/share/grafana
