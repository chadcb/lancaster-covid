# lancaster-covid
Quick script to scrape website for county covid dial and feed to mqtt for HA Sensors

Example Message:  
{"timestamp": "2020-07-13T20:14:35.339673", "pre_week": "2.5", "cur_week": "4.5", "gauge_caption": "Updated Friday, July 10"}  

Example Crontab:  
0 * * * * cd /home/hass/scripts/lancaster_covid && bin/python ./lancaster_covid.py >/dev/null 2>&1
