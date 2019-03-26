import json

class CustomError(Exception):
    pass

def lambda_handler(event, context):
    num_of_winners = event['input']
    exception = event['exception']
    
    # Trigger the Failed process
    if exception == 1:
        raise CustomError("An error occurred!!")
    else:
        pass
    
    return {
        "body": {
            "num_of_winners": num_of_winners
        }
    }
