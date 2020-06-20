import json
def handler(event, context):
    # Log the event argument for debugging and for use in local development.
    print(json.dumps(event))

    try:
        if event['isBase64Encoded']:
            return "You uploaded a base64encoded thing to this function"
        else:
            return "You didn't base64encode anything to this funciton"
    catch:
        return "Something went terribly wrong."