import json
import boto3
import urllib3
import os
http = urllib3.PoolManager() 
ssm = boto3.client('ssm', 'us-east-1')
sns = boto3.client('sns', 'us-east-1')
snsArn = os.environ["SNS_ARN"]

def get_parameters():
    response = ssm.get_parameters(
        Names=['FridgeState']
    )
    for parameter in response['Parameters']:
        return parameter['Value']

def put_parameters(value):
    response = ssm.put_parameter(
    Name='FridgeState',
    Value=value,
    Overwrite=True)
    return response

def sendSNS(message):
    response = sns.publish(
        TargetArn = snsArn,
        Message=json.dumps({'default': json.dumps(message)}),
        MessageStructure = 'json'
    )
    return response
    
def sendWebhook(applet):
    url = "https://maker.ifttt.com/trigger/"+applet+"/with/key/"+os.environ["IFTTT_KEY"]
    resp = http.request('POST',url)
    return resp

def lambda_handler(event, context):
    
    value = get_parameters()
    print("Fridge State = " + value)

    temp = event['temperature']
    print("temp: " + str(temp))    

    if value == 'Off' and temp > 38:
        print("Fridge Off - Temp > 38. Should be On.  Turning On")
        
        snsMessage = "Turning the Fridge On"
        response = sendSNS(snsMessage)
        print(response)
        
        applet = "TurnOnFridge"
        response = sendWebhook(applet)

        put_parameters("On")
    elif value == 'Off' and temp < 38:
        print("Fridge Off - Temp < 38 - Do Not Turn On")
    elif value == 'On' and temp < 38:
        print("Fridge On - Temp < 38 - Should be Off.  Turning Off")
        
        snsMessage = "Turning the Fridge Off"
        response = sendSNS(snsMessage)
        print(response)
        
        applet = "TurnOnFridge"
        response = sendWebhook(applet)

        put_parameters("Off")
    elif value == 'On' and temp > 38:
        print("Fridge On - Temp > 38 - Do Not Turn Off")
    else:
        print("Do Nothing")

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
