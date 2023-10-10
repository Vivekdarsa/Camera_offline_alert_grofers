import requests
from datetime import datetime, time

def send_mail(client_data, html_str):
    # if datetime.now().hour < 23 and datetime.now().hour > 7:
        return requests.post(
            "https://api.mailgun.net/v3/mg.darsa.ai/messages",
            auth=("api", "7b0eb98ceb8aa476a819f7b1e7d9bd0b-203ef6d0-8a6dc04b"),
            data={
                    "from": "alerts@darsa.ai",
                    "to": client_data['email_addresses'][0].lower(),
                    "subject": 'Camera Offline Alert - ' + client_data['company_name'],
                    "html": html_str
                })

            