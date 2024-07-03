import sys
import time
import threading
from flask import Flask, jsonify, request
import psutil
from fanshim import FanShim

app = Flask(__name__)

def print_to_console(msg: str):
    print(f"{msg}\n\n")

class FanController:
    def __init__(self, on_temp=65, off_temp=55, poll_interval=1):
        print_to_console(f"Setting temperature thresholds: on={on_temp}°C, off={off_temp}°C")
        self.fan_shim = FanShim()
        self.on_temp = on_temp
        self.off_temp = off_temp
        self.poll_interval = poll_interval
        self.thread = None
        self.fan_shim.set_fan(False)

    def get_cpu_temp(self):
        # Get the current CPU temperature
        return psutil.sensors_temperatures()['cpu_thermal'][0].current

    def fan_on(self):
        if not self.fan_shim.get_fan():
            print_to_console("Turning fan on")
            self.fan_shim.set_fan(True)
        else:
            print_to_console("Fan is already on")

    def fan_off(self):
        if self.fan_shim.get_fan():
            print_to_console("Turning fan off")
            self.fan_shim.set_fan(False)
        else:
            print_to_console("Fan is already off")

    def monitor_temp(self):
        while True:
            cpu_temp = self.get_cpu_temp()
            print_to_console(f"CPU temperature: {cpu_temp}°C")
            if cpu_temp >= self.on_temp:
                self.fan_on()
            elif cpu_temp < self.off_temp:
                self.fan_off()
            time.sleep(self.poll_interval)

    def start(self):
        self.thread = threading.Thread(target=self.monitor_temp)
        self.thread.start()

    def stop(self):
        self.thread.join()
        self.fan_off()  # Turn off the fan when stopping

controller = FanController(on_temp=50, off_temp=40, poll_interval=30)

@app.route('/fan/on', methods=['POST'])
def turn_fan_on():
    controller.fan_on()
    return jsonify({"status": "fan turned on"}), 200

@app.route('/fan/off', methods=['POST'])
def turn_fan_off():
    controller.fan_off()
    return jsonify({"status": "fan turned off"}), 200

@app.route('/fan/status', methods=['GET'])
def fan_status():
    status = controller.fan_shim.get_fan()
    return jsonify({"fan_status": "on" if status else "off"}), 200

@app.route('/temp/status', methods=['GET'])
def temp_status():
    temp = controller.get_cpu_temp()
    return jsonify({"cpu_temperature": temp}), 200

@app.route('/temp/set', methods=['POST'])
def set_temp_thresholds():
    data = request.json
    on_temp = data.get('on_temp')
    off_temp = data.get('off_temp')

    if on_temp is not None:
        controller.on_temp = on_temp
    if off_temp is not None:
        controller.off_temp = off_temp

    return jsonify({
        "status": "thresholds updated",
        "on_temp": controller.on_temp,
        "off_temp": controller.off_temp
    }), 200

def main():
    # Start the fan controller
    controller.start()

    # Start the Flask server in a separate thread
    server_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000))
    server_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        controller.stop()
        sys.exit()

if __name__ == "__main__":
    main()
