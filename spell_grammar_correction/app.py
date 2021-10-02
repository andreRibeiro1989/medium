import json
from gingerit.gingerit import GingerIt


# lambda function handler
def lambda_handler(event, context):
  """
  Main lambda function. Receives a json with the user text
  and return the corrected text using gingerit.

  Args:
    event (dict): Contains the main information for the request (
                  headers, body, ...)
    context (dict): Context in which the lambda function was called

  Returns:
    dict: Dictionary with response headers, body, status_code, isBase64Encoded
  """
  
  # handle api gateway request (we will need this when adding API Gateway)
  if 'httpMethod' in event.keys():
    event = json.loads(event['body'])

    if isinstance(event, str):
      event = json.loads(event)

  # If 'text' is in the request fields "correct" it
  if 'text' in event.keys():
    
    # original text we want to correct
    text = event['text']
    
    # corrected text by gingerit
    corrected_text = GingerIt().parse(text)['result']
    
    # response from lambda must be a json so let's do that
    response_body = {
      'corrected_text': corrected_text
    }
    
    # make sure to include the following fields as they are
    # required by API Gateway
    response = {
        'headers':{
          "Content-Type": "application/json"
        },
        'statusCode':200,
        'body':json.dumps(response_body),
        'isBase64Encoded': False
    }

  # If 'text' is NOT in the request fields return an error message
  else:
    
    # Similarly to the success case we encode the error message as a json
    response_body = {
      'error_message': "The request 'Body' must follow this syntax: {'Body':{'text':TEXT TO BE CORRECTED}}"
    }
    
    response = {
      'headers':{
        "Content-Type": "application/json"
      },
      'statusCode':101,
      'body':json.dumps(response_body),
      'isBase64Encoded': False
    }

  return response
    