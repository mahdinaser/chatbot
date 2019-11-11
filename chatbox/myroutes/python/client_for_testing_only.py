# importing the requests library
import requests

# defining the api-endpoint
# API_ENDPOINT = "http://52.168.33.198/chatbot"
#129.118.163.28
API_ENDPOINT = "http://129.118.163.28/chatbot"
sampleQuery = 'Will muscle relaxers help me sleep and help rls at night during detox?'

# data to be sent to api
data = {'query': sampleQuery}

# sending post request and saving response as response object
r = requests.post(url=API_ENDPOINT, data=data)

# extracting response text
pastebin_url = r.text
print(pastebin_url)
