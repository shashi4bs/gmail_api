import key
GMAIL = key.service

#f = open('tdata.txt','w')
threads = GMAIL.users().threads().list(userId='me').execute().get('threads',[])
for thread in threads:
    tdata = GMAIL.users().threads().get(userId='me',id=thread['id']).execute()
    #f.write(str(tdata))
    nmsgs = len(tdata['messages'])
    
    if nmsgs >0:
        msg = tdata['messages'][0]['payload']
        subject = ''
        for header in msg['headers']:
            if header['name'] == 'Subject':
                subject = header['value']
                break
        if subject :
            print(subject, nmsgs," msgs")       
    #f.close()
