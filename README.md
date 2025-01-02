# HighlightProcessor
This project uses RapidAPI to obtain NCAA game highlights using a Docker container and uses AWS Media Convert to convert the media file.

# Overview
The fetch.py script performs the following actions:

Establishes the date and league that will be used to find highlights. We are using NCAA in this example because it's included in the free version.
This will fetch the highlights from the API and store them in an S3 bucket as a JSON file (basketball_highlight.json)

process_one_video.py performs the following actions:

Connects to the S3 bucket and retrieves the JSON file.
Extracts the first video URL from within the JSON file.
Downloads the video fiel from the internet into the memory using the requests library.
Saves the video as a new file in the S3 bucket under a different folder (videos/)
Logs the status of each step

mediaconvert_process.py performs the following actions:

Creates and submits a MediaConvert job
Uses MediaConvert to process a video file - configures the video codec, resolution and bitrate. Also configured the audio settings
Stores the processed video back into an S3 bucket

# Prerequisites
Before running the scripts, ensure you have the following:

# 1 Create Rapidapi Account
Rapidapi.com account, will be needed to access highlight images and videos.

For this example we will be using NCAA (USA College Basketball) highlights since it's included for free in the basic plan.

# 2 Verify prerequites are installed 

Docker should be pre-installed in most regions docker --version

AWS CloudShell has AWS CLI pre-installed aws --version

Python3 should be pre-installed also python3 --version

# 3 Retrieve AWS Account ID

Copy your AWS Account ID Once logged in to the AWS Management Console Click on your account name in the top right corner You will see your account ID Copy and save this somewhere safe because you will need to update codes in the labs later

# 4: Retrieve Access Keys and Secret Access Keys
You can check to see if you have an access key in the IAM dashboard
Under Users, click on a user and then "Security Credentials"
Scroll down until you see the Access Key section
You will not be able to retrieve your secret access key so if you don't have that somewhere, you need to create an access key.


# START HERE 
# Step 1: Create an IAM role or user

In the search bar type "IAM" 
Click Roles -> Create Role
For the Use Case enter "S3" and click next
Under Add Permission search for AmazonS3FullAccess, MediaConvertFullAccess and AmazonEC2ContainerRegistryFullAccess and click next
Edit the Trust Policy and replace it with this:

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": [
          "ec2.amazonaws.com",
          "ecs-tasks.amazonaws.com",
          "mediaconvert.amazonaws.com"
        ],
        "AWS": "arn:aws:iam::<your-account-id>:user/<your-iam-user>"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}

Select Create Role


# Step 2: Create S3 Bucket
Navigate to the AWS Cloudshell console
Run this bash script to create an S3 Bucket, be sure to replace <your-bucket-name> and <region>

"aws s3api create-bucket --bucket <your-bucket-name> --region <region> --create-bucket-configuration LocationConstraint=<region>"

Verify the bucket exists
aws s3 ls

# Step 3: Set Up Project

Create the Project Directory: "mkdir game-highlight-processor cd game-highlight-processor"

Create the Necessary Files: "touch Dockerfile fetch.py requirements.txt process_one_video.py mediaconvert_process.py"

Add code to the files In the CLI enter "nano fetch.py"

In another browser navigate to the GitHub Repo and copy the contents within fetch.py

Reminder to replace with your S3bucket name, your RapidAPI key and region

Exit and Save file

In CLI enter "nano Dockerfile" Paste the code found within the Dockerfile on Github into the blank area Exit and Save file

In CLI enter "nano requirements.txt" Paste the code found within the requirements.txt file on Github into the blank area Exit and Save file

In CLI enter nano "process_one_video.py" Paste the code found within the process_one_video.py file on Github into the blank area 

Reminder to replace your S3bucket name

Exit and Save file

Retrieve MediaConvert Endpoint
"aws mediaconvert describe-endpoints"

In CLI enter nano "mediaconvert_process.py" Paste the code found within the mediaconvert_process.py file on Github into the blank area 

Reminder to replace your S3bucket name, mediaconvert endpoint & your account ID(above the print portion of the code)

Exit and Save file

# Step 4: Build and Run the Docker Container
Run:
"docker build -t highlight-processor ."

Run the Docker Container Locally:
docker run -e AWS_ACCESS_KEY_ID=<your-access-key-id> \
           -e AWS_SECRET_ACCESS_KEY=<your-secret-access-key> \
           -e AWS_DEFAULT_REGION=us-east-1 \
           highlight-processor
           
This will run fetch.py and there should be a file saved in your S3 bucket now

# Step 5: Process A Video From basketball_highlights.json
Run the process_one_video script
"python3 process_one_video.py"

Optional - Confirm there is a video uploaded to s3://<your-bucket-name>/videos/first_video.mp4

# Step 6: Use AWS MediaConvert to convert the file
Run mediaconvert_process.py
"python3 mediaconvert_process.py"

Optional - Confirm there is a video uploaded to s3://<your-bucket-name>/processed_videos/
