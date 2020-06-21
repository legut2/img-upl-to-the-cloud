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
from requests_toolbelt.multipart import decoder
import io

def handler(event, context):
    # Log the event argument for debugging and for use in local development.
    print(json.dumps(event))

    try:
        if event['isBase64Encoded']:

            body = event["body"] # body that is base64 encoded
            content_type = event["headers"]["content-type"] # what kind of content type it is, presumably it is multipart dataform
            # decode base  64
            body_dec = base64.b64decode(body)

            #decode form-data from multipart form
            #multipart forms are very common due to html forms
            multipart_data = decoder.MultipartDecoder(body_dec, content_type)
            binary_content = []
            for part in multipart_data.parts:
                binary_content.append(part.content)

            imageStream = io.BytesIO(binary_content[0])
            imageFile = Image.open(imageStream)
            imageArray = np.array(imageFile)

            # Create new image from the Numpy array and save to sanitize the image to help prevent something malicious as payload
            result = Image.fromarray(imageArray)

            m = hashlib.md5()

            # m.update(img_data) # Make hash specific to image

            imageName = m.hexdigest() + ".jpg" # image name is now hash + jpg
            imagePath = "/tmp/" + imageName # tmp is one of the few places where you can write a file, keep in mind container reuse is possible with lambdas.
            result.save(imagePath)

            # Upload to s3 bucket finally that is in env variable
            s3 = boto3.resource('s3')
            print("Storing thumbnail %s to ObjectStore 'Uploaded Image'" % imagePath)
            targetBucket = os.environ['BUCKET_NAME']
            try:
                s3.Bucket(targetBucket).upload_file(imagePath, imageName)
            except botocore.exceptions.ClientError as e:
                print("Error uploading %s to bucket %s" % (imageName, targetBucket))
                raise
            return {
                "status": "success",
                "statusCode": "200",
                "body": {
                    "message": "Uploaded to s3."
                }
            }
        else:
            return {
                "status": "error",
                "statusCode": "400",
                "body": {
                    "error": {
                        "message": ""
                }
            }
        }
    except KeyError as e:
        return {
            "status": "error",
            "statusCode": "400",
            "body": {
                "error": {
                    "message": str(e)
                }
            }
        }