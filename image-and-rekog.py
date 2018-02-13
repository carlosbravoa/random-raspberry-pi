import boto3
import picamera
import time

BUCKET = "raspibucket2"
REGION = "eu-west-1"

def take_picture():
   print("Attempting to take the picture. Smile! :)")
   ts = int(time.time())
   filename = 'image-'+ str(ts) + '.jpg'
   camera = picamera.PiCamera()
   camera.capture(filename)
   print("Picture taken")
   return filename

def upload_picture(filename):
   print("Attempting to upload the picture")
   s3_client = boto3.client('s3', REGION)
   s3_client.upload_file(filename, BUCKET, filename)
   print("Picture uploaded")

def detect_labels(bucket, key, max_labels=10, min_confidence=90, region=REGION):
        print("Attempting to call the Rekognition service :O")
	rekognition = boto3.client("rekognition", region)
	response = rekognition.detect_labels(
		Image={
			"S3Object": {
				"Bucket": bucket,
				"Name": key,
			}
		},
		MaxLabels=max_labels,
		MinConfidence=min_confidence,
	)
        print("Done!")
	return response['Labels']

def show_labels(labels):
   for label in labels:
     print "{Name} - {Confidence}%".format(**label)


def start():
  filename = take_picture()
  upload_picture(filename)
  res = detect_labels(BUCKET, filename, 10, 80)
  show_labels(res)

start()

