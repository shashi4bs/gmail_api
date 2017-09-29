from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file,client,tools

scope = 'https://www.googleapis.com/auth/gmail.readonly https://www.googleapis.com/auth/gmail.modify'
client_secret = 'client_secret.json'
http = Http()

store = file.Storage('storage.json')
credz = store.get()
if not credz or credz.invalid:
    flow = client.flow_from_clientsecrets(client_secret,scope)
    credz = tools.run_flow(flow,store)
    
service = build('gmail','v1',http=http)
