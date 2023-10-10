from datetime import datetime
import json
import schedule
import time

from api import get_client_list, get_token
from alert import OfflineAlert

with open('config.json','r') as conf_file:
    conf_data = json.load(conf_file)

alerts_to_send = {}
client_alert_list = get_client_list(conf_data['url'], conf_data['token'])
client_alert_list_ = []
for i in client_alert_list:
    if i['company_name'] == 'Cube':
        client_alert_list_.append(i)

client_alert_list = client_alert_list_

for i in client_alert_list:
    alerts_to_send[i['id']] = i
    alerts_to_send[i['id']]['status'] = 'running'

with open('alerts_to_send.json','w') as alerts_to_send_file:
    json.dump(alerts_to_send, alerts_to_send_file)

client_tokens = {}
try:
    with open("client_token_config.json", 'r') as client_token_config_file:
        client_tokens = json.load(client_token_config_file)
except Exception as e:
    pass
  
for alert_data in client_alert_list:
    client_email = alert_data['created_by']
    if client_email not in client_tokens:
        password = 'abcD123$'
        if 'internal' in client_email: password = 'efgH123$'
        client_token = get_token('http://cube.darsa.ai',{'username': client_email,'password' : password})
        client_tokens[client_email] = {'url': 'cube.darsa.ai', 'token': client_token['token']}

with open("client_token_config.json", 'w') as client_token_config_file:
    json.dump(client_tokens, client_token_config_file)

with open("alerts_to_send.json", 'r') as alerts_to_send_file:
    alerts_to_send = json.load(alerts_to_send_file)

for alert_data in alerts_to_send:
    url = 'http://cube.darsa.ai'
    token = client_tokens[alerts_to_send[alert_data]['created_by']]['token']
    OfflineAlert(alerts_to_send[alert_data], url, token).start()


def refresh():
    print(datetime.now(), 'refreshing',"CUBE OF ALERT MAIL")

    with open('config.json','r') as conf_file:
        conf_data = json.load(conf_file)

    alerts_to_send = {}
    client_alert_list = get_client_list(conf_data['url'], conf_data['token'])

    for i in client_alert_list:
        alerts_to_send[i['id']] = i
        alerts_to_send[i['id']]['status'] = 'not_running'

    prev_to_send = {}
    with open('alerts_to_send.json','r') as alerts_to_send_file:
        prev_to_send = json.load(alerts_to_send_file)
    
    for i, j in alerts_to_send.items():
        if str(i) not in prev_to_send:
            prev_to_send[i] = j
            prev_to_send[i]['status'] = 'not_running'

    with open('alerts_to_send.json','w') as alerts_to_send_file:
        json.dump(prev_to_send, alerts_to_send_file)

    client_tokens = {}
    try:
        with open("client_token_config.json", 'r') as client_token_config_file:
            client_tokens = json.load(client_token_config_file)
    except Exception as e:
        pass
    
    for alert_data in client_alert_list:
        client_email = alert_data['created_by']
        if client_email not in client_tokens:
            password = 'abcD123$'
            if 'internal' in client_email: password = 'efgH123$'
            client_token = get_token('http://cube.darsa.ai',{'username': client_email,'password' : password})
            client_tokens[client_email] = {'url': 'cube.darsa.ai', 'token': client_token['token']}

    with open("client_token_config.json", 'w') as client_token_config_file:
        json.dump(client_tokens, client_token_config_file)

    with open("alerts_to_send.json", 'r') as alerts_to_send_file:
        alerts_to_send = json.load(alerts_to_send_file)

    for alert_data in alerts_to_send:
        if alerts_to_send[alert_data]['status'] == 'not_running':
            url = 'http://cube.darsa.ai'
            token = client_tokens[alerts_to_send[alert_data]['created_by']]['token']
            OfflineAlert(alerts_to_send[alert_data], url, token).start()

    updated_alerts_to_send = {}
    with open("alerts_to_send.json", 'r') as alerts_to_send_file:
        old_to_send = json.load(alerts_to_send_file)
    
    for i in old_to_send:
        if old_to_send[i]['status'] != 'running':
            updated_alerts_to_send[i] = old_to_send[i]
            updated_alerts_to_send[i]['status'] = 'running'

    with open("client_token_config.json", 'w') as client_token_config_file:
        json.dump(client_tokens, client_token_config_file)

# refresh()

schedule.every().day.at("23:58").do(refresh)

while 1:
    schedule.run_pending()
    time.sleep(5)

    