import os
import json

from yandex_tracker_client import TrackerClient

def handler(event, context):
 client = TrackerClient(token=os.environ['TOKEN'], org_id=os.environ['ORG'])
 issue = client.issues[event['queryStringParameters']['id']]

 links = issue.links
 if not links:
  exit()
 
 for link in links:
  if link.direction == "outward" and link.type.id == "subtask" and link.status.key != "closed":
   sub_issue_id = link.object.key
   issue_to_update = client.issues[sub_issue_id]
   #issue_to_update.transitions['close'].execute()
   # or transition with resolution
   transition = issue_to_update.transitions['close']
   transition.execute(comment='Closed/Fixed automaticly, parent issue ' + issue.key + ' closed', resolution='fixed')
   
 return {
        'statusCode': 200,
        'body': issue_to_update.key + ' closed',
    }
