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

(1) Rapidapi.com account, will be needed to access highlight images and videos.

For this example we will be using NCAA (USA College Basketball) highlights since it's included for free in the basic plan.

(2) Verify prerequites are installed Docker should be pre-installed in most regions docker --version

AWS CloudShell has AWS CLI pre-installed aws --version

Python3 should be pre-installed also python3 --version

(3) Copy your AWS Account ID Once logged in to the AWS Management Console Click on your account name in the top right corner You will see your account ID Copy and save this somewhere safe because you will need to update codes in the labs later


# START HERE 
# Step 1: 



# Step 2: 



# Step 3: 


# Step 4: 

