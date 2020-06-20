import json
import base64
import hashlib

def handler(event, context):
    # Log the event argument for debugging and for use in local development.
    print(json.dumps(event))

    try:
        if event['isBase64Encoded']:
            img_data = event['body'].encode()
            m = hashlib.md5()
            m.update(img_data)

            with open(m.hexdigest() + ".jpeg", "wb") as fh:
                fh.write(base64.decodebytes(img_data))
            

            return "You uploaded a base64encoded thing to this function and wrote a jpeg but never checked to make sure it was a jpeg"
        else:
            return "You didn't base64encode anything to this funciton"
    except KeyError:
        return "Something went terribly wrong."