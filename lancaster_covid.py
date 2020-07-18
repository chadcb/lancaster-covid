import json
import re

from datetime import datetime
import paho.mqtt.client as mqtt
import requests
from bs4 import BeautifulSoup


MQTT_HOST = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "covid/lancaster"
URL = "https://lincoln.ne.gov/city/covid19/"
COVID_DIAL_REGEX = re.compile(
    r"\D+ (\d*\.?\d+) on a scale of 0-8 \(0 is low risk; 8 is severe risk\). \D+ (\d*\.?\d+)."
)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
}


class DateTimeEncoder(json.JSONEncoder):
    """https://stackoverflow.com/questions/11875770/how-to-overcome-datetime-datetime-not-json-serializable"""

    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)


def parse_covid_message(response):
    soup = BeautifulSoup(response.text, "lxml")
    covid_status = soup.find("div", {"class": "obscure"}).text
    gauge_caption = soup.find("div", {"class": "gauge-caption"}).text.replace("\n", "")

    data = re.search(COVID_DIAL_REGEX, covid_status)
    timestamp = datetime.now()

    try:
        pre_week = data.group(1)
        cur_week = data.group(2)
    except:
        pre_week = None
        cur_week = None

    return {
        "timestamp": timestamp,
        "pre_week": pre_week,
        "cur_week": cur_week,
        "gauge_caption": gauge_caption,
    }


def publish_message(msg):
    client = mqtt.Client()
    try:
        client.connect(MQTT_HOST, MQTT_PORT, 60)
        client.publish(
            MQTT_TOPIC, json.dumps(msg, cls=DateTimeEncoder), retain=True, qos=1
        )
    except:
        return


def main():
    try:
        r = requests.get(URL, headers=HEADERS)
        msg = parse_covid_message(r)
        publish_message(msg)
    except:
        print("Error Occured")


if __name__ == "__main__":
    main()
