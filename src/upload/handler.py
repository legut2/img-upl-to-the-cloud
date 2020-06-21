import boto3
import botocore
import json
import base64
import hashlib
import os
import email.parser





def handler(event, context):
    # Log the event argument for debugging and for use in local development.
    print(json.dumps(event))

    try:
        if event['isBase64Encoded']:
            b64_form_data = event['body'].encode()
            form_data = base64.decodebytes(b64_form_data)
            msg = email.parser.BytesParser().parsebytes(form_data, headersonly=False)
            d = {}
            for part in msg.get_payload():
                d[part.get_param('name', header='content-disposition')] = part.get_payload(decode=True)
            print(d)
            return str(form_data)
            m = hashlib.md5()
            m.update(img_data)
            imageName = m.hexdigest() + ".jpg"
            imagePath = "/tmp/" + imageName
            with open(imagePath, "wb") as fh:
                fh.write(base64.decodebytes(img_data))

            s3 = boto3.resource('s3')
            print("Storing thumbnail %s to ObjectStore 'Uploaded Image'" % imagePath)
            targetBucket = os.environ['BUCKET_NAME']
            try:
                s3.Bucket(targetBucket).upload_file(imagePath, imageName)
            except botocore.exceptions.ClientError as e:
                print("Error uploading %s to bucket %s" % (imageName, targetBucket))
                raise
            return "You uploaded a base64encoded thing to this function and wrote a jpeg but never checked to make sure it was a jpeg then tried to upload it to s3 bucket"
        else:
            return "You didn't base64encode anything to this funciton"
    except KeyError:
        return "Something went terribly wrong."