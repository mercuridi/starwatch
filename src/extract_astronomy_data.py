import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv('src/.env')


user_pass = f"{os.environ.get('applicationId')}:{os.environ.get("applicationSecret")}"
auth_string = base64.b64encode(user_pass.encode()).decode()
headers = {
    'Authorization': f'Basic {auth_string}'
}

url = "https://api.astronomyapi.com/api/v2/bodies"

response = requests.get(url, headers=headers)

print(response.json())
