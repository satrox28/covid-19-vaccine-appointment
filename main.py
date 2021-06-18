import requests
import json
import http.client as httplib, urllib.parse
import logging

import datetime
curr_date = datetime.datetime.now()
date_Array = []
for i in range(7):
    curr_date += datetime.timedelta(days=1)
    date_Array.append(curr_date.strftime("%Y-%m-%d"))


url = 'https://apis.mdnius.com/booking/api/v1/public/getSlots'
headers = {'authority': 'apis.mdnius.com'}

logging.basicConfig(filename='message_push.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
for date_obj in date_Array:
    data = { 'date': date_obj,'clinicId': '609be7f8f132c1001fb007c4'}
    r = requests.post(url, json=data, headers=headers)
    response_json = json.loads(r.text)
    message_push = ""

    for i in response_json["data"]:
        i["remainingSlots"] = i["totalSlots"]-i["filledSlots"]
        if i["remainingSlots"] > 0:
            message_push = message_push+ " TimeSlotStart: "+ i["timeSlotStart"] + " RemainingSlots: " + str(i["remainingSlots"]) + "\n"




    if bool(message_push):
        conn = httplib.HTTPSConnection("api.pushover.net:443")
        conn.request("POST", "/1/messages.json",
        urllib.parse.urlencode({
        "token": "$TOKEN",
        "user": "$USER_KEY",
        "message": "Date: "+ date_obj + "  \n\n" + (message_push),
        }), { "Content-type": "application/x-www-form-urlencoded" })
        a=conn.getresponse()
        print(a.reason)
    else:
        logging.info("No Slots Available for " + date_obj)
#print(conn.getresponse())
