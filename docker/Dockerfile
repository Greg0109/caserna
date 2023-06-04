FROM 2000cubits/raspbian:buster

# Install dependencies
RUN apt-get update && \
    apt-get install -y python3-pip python3-rpi.gpio aptitude && \
    aptitude install libjpeg62 libopenjp2-7 libtiff5 libpq5 libjpeg62-turbo -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip3 install --upgrade pip

# Copy requirements
COPY requirements.txt /tmp/

# Copy caserna wheel
COPY dist/*.whl /tmp/

# Install caserna
RUN python3 -m pip install --no-cache-dir -r /tmp/requirements.txt && \
    python3 -m pip install --no-cache-dir /tmp/*.whl && \
    rm -rf /tmp/*.whl /tmp/requirements.txt

# Start caserna service
CMD ["caserna", "-w", "weather_station"]
