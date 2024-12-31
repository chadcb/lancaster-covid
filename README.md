# lancaster-covid
Python script to scrape website for county covid data. Data is sent via MQTT and picked up by [Home Assistant](https://home-assistant.io) to mimic the risk dial. Main use is [TileBoard](https://community.home-assistant.io/t/tileboard-new-dashboard-for-homeassistant/57173) gauge on Amazon Fire Tablets.  

## Example Message:  
{"timestamp": "2020-07-13T20:14:35.339673", "pre_week": "2.5", "cur_week": "4.5", "gauge_caption": "Updated Friday, July 10"}  

## Example Crontab:  
0 * * * * cd /home/hass/scripts/lancaster_covid && bin/python ./lancaster_covid.py >/dev/null 2>&1

## Home Assistant Sensor Config:  
``` yaml
sensor:
  - platform: mqtt
    name: mqtt_lancaster_covid_pre_week
    state_topic: "covid/lancaster"
    value_template: "{{ value_json.pre_week }}"
  - platform: mqtt
    name: mqtt_lancaster_covid_cur_week
    state_topic: "covid/lancaster"
    value_template: "{{ value_json.cur_week }}"
  - platform: mqtt
    name: mqtt_lancaster_covid_timestamp
    state_topic: "covid/lancaster"
    value_template: "{{ value_json.timestamp }}"
  - platform: mqtt
    name: mqtt_lancaster_covid_updated
    state_topic: "covid/lancaster"
    value_template: "{{ value_json.gauge_caption }}"
 ```
 
 ## Tileboard Config
 ```javascript
 {
   position: [1, 0],
   state: false,
   width: 1,
   height: 1,
   title: 'Covid Risk',
   subtitle: '',
   type: TYPES.GAUGE,
   id: 'sensor.mqtt_lancaster_covid_cur_week', // Assign the sensor you want to display on the gauge
   value: function(item, entity){
      return entity.state;
   },
   customStyles: {'backgroundColor': '#EEEEEE'},
   settings: {
      size: 150, // Defaults to 50% of either height or width, whichever is smaller
      type: 'semi', // Options are: 'full', 'semi', and 'arch'. Defaults to 'full'
      min: 0, // Defaults to 0
      max: 8, // Defaults to 100
      cap: 'butt', // Options are: 'round', 'butt'. Defaults to 'butt'
      thick: 24, // Defaults to 6
      //label: 'Current Week', // Defaults to undefined
      //append: '@attributes.unit_of_measurement', // Defaults to undefined
      //prepend: '$', // Defaults to undefined
      duration: 1500, // Defaults to 1500ms
      thresholds: {
                     0: { color: '#30B32D'},
                     1: { color: '#FFFF00'},
                     4: { color: '#FF6600'},
                     7: { color: '#FF0000'},
      },  // Defaults to undefined
      labelOnly: false, // Defaults to false
      foregroundColor: 'rgba(0, 150, 136, 1)', // Defaults to rgba(0, 150, 136, 1)
      backgroundColor: 'rgba(0, 0, 0, 0.1)', // Defaults to rgba(0, 0, 0, 0.1)
      fractionSize: 0, // Number of decimal places to round the number to. Defaults to current locale formatting
   },
}
``` 

## What the real Lancaster Covid Dial from [Website](https://www.lincoln.ne.gov/city/covid19/) looks like
![Image of Lancaster Covid Dial](/images/lancaster_covid_dial.png)

## Fire HD Tablet showing minimal dial using [Home Assistant](https://home-assistant.io) and [TileBoard](https://community.home-assistant.io/t/tileboard-new-dashboard-for-homeassistant/57173)
![Image of Fire HD 8](/images/fire_hd8.png)
