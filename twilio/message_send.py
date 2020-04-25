ACCOUNT_SID = "AC3a8537ab94d7e7ae903ffb30f5fe9fa3"

AUTO_TOKEN = "3b0ece2fec69883f4ae1ba8f9c6d0783"

#(413) 314-2364

Phone_Number = 14133142364
import time
from twilio.rest import Client
text = '123'

auth_token = '3b0ece2fec69883f4ae1ba8f9c6d0783'   #去twilio.com注册账户获取token
account_sid = 'AC3a8537ab94d7e7ae903ffb30f5fe9fa3'

client = Client(account_sid,auth_token)

def sent_message(phone_number):
    mes = client.messages.create(
        from_='14133142364',  #填写在active number处获得的号码
        body=text,
        to=phone_number
    )
    print("OK")


sent_message("8619825302947")
