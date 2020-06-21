import boto3
import botocore
import json
import base64
import hashlib
import os
import email.parser
import cgi, cgitb
import numpy as np
from PIL import Image


def handler(event, context):
    # Log the event argument for debugging and for use in local development.
    print(json.dumps(event))

    try:
        if event['isBase64Encoded']:
            # b64_form_data = event['body'].encode()
            # form_data = base64.decodebytes(b64_form_data)
            body = event["body"]

            content_type = event["headers"]["content-type"]

            body_dec = base64.b64decode(body)

            multipart_data = decoder.MultipartDecoder(body_dec, content_type)

            binary_content = []

            for part in multipart_data.parts:
                binary_content.append(part.content)

            imageStream = io.BytesIO(binary_content[0])
            imageFile = Image.open(imageStream)
            imageArray = np.array(imageFile)
            # Create new image from the Numpy array and save
            result = Image.fromarray(imageArray)
            # return str(form_data)
            m = hashlib.md5()
            # m.update(img_data)
            imageName = m.hexdigest() + ".jpg"
            imagePath = "/tmp/" + imageName
            result.save(imagePath)
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
    except KeyError as e:
        return "Something went terribly wrong." + str(e)