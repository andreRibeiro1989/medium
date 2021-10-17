import os 
import re
import time
import json
import boto3
import praw

S3BUCKET = os.getenv('S3BUCKET')
S3PREFIX = os.getenv('S3PREFIX')
CLIENTID = os.getenv('CLIENTID')
CLIENTSECRET = os.getenv('CLIENTSECRET')
USERAGENT = os.getenv('USERAGENT')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

s3 = boto3.resource("s3").Bucket(S3BUCKET)

reddit = praw.Reddit(
    client_id=CLIENTID,
    client_secret=CLIENTSECRET,
    user_agent=USERAGENT,
    username=USERNAME,
    password=PASSWORD,
)


# Save unread requests from messages or mentions
def save_unread_requests():
    for msg in reddit.inbox.unread():
        print([msg.id, msg.author.id, msg.subject, msg.body])

        if msg.was_comment:
            parsed_time = re.findall(
              '/u/copyreminder remindme ([0-9]+) ?([a-z]+)',
              msg.body.lower()
            )
        else:
            parsed_time = re.findall(
              'remindme ([0-9]+) ?([a-z]+)', 
              msg.subject.lower()
            )

        if len(parsed_time) > 0:
            if parsed_time[0][1] in ('m', 'min', 'minute', 'minutes'):
                remind_ts = msg.created_utc + int(parsed_time[0][0]) * 60
            elif parsed_time[0][1] in ('h', 'hour', 'hours'):
                remind_ts = msg.created_utc + int(parsed_time[0][0]) * 60 * 60
            elif parsed_time[0][1] in ('d', 'day', 'days'):
                remind_ts = msg.created_utc + int(parsed_time[0][0]) * 24 * 60 * 60

            msg_dict = {
                'created_ts':msg.created_utc,
                'author':msg.author.id, 
                'was_comment':msg.was_comment,
                'remind_ts':remind_ts,
                'remind_id':msg.id, 
            }
            
            s3.Object(key=os.path.join(S3PREFIX, msg.id)).put(Body=json.dumps(msg_dict))
            
            msg.reply(
                "Hi. I'll remind you of this message in {} {}".format(
                    parsed_time[0][0], parsed_time[0][1])
            )
            
        msg.mark_read()
        

# check if there are any requests to be fullfilled
def realise_requests():
    for f in s3.objects.filter(Prefix=S3PREFIX):
        job = json.load(f.get()["Body"])
    
        if int(time.time()) > job['remind_ts']:
            if job['was_comment'] == 1:
                msg = reddit.comment(id=job['remind_id'])
            else:
                msg = reddit.inbox.message(message_id=job['remind_id'])

            msg.reply(
                "Hi. Here goes the message you requested to be reminded of."
            )
            
            f.delete()
                

# lambda function handler
def lambda_handler(event, context):
  """
  Main lambda function. 
  This is a Reddit bot that checks for mentions or PMs to remind users
  of a given message.

  Args:
    event (dict): Contains the main information for the request
    context (dict): Context in which the lambda function was called

  Returns:
    dict: Dictionary with response headers, body, status_code, isBase64Encoded
  """
  
  # save any unread messages to db
  save_unread_requests()

  # checks for any actions to be taken
  realise_requests()
                      
  # in the case we call this lambda directly
  # let's add a basic response
  response = {
      'headers':{
        "Content-Type": "application/json"
      },
      'statusCode':200,
      'body':None,
      'isBase64Encoded': False
  }
  
  return response