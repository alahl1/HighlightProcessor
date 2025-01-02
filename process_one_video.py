import json  # For parsing JSON data
import boto3  # AWS SDK for interacting with AWS services
import requests  # For downloading video data from the URL
from io import BytesIO  # For handling in-memory file-like objects

# Constants
S3_BUCKET_NAME = "<your_bucket_name>"  # Replace with your S3 bucket name
INPUT_KEY = "highlights/basketball_highlights.json"  # Path to the JSON file in your S3 bucket
OUTPUT_KEY = "videos/first_video.mp4"  # Path to save the video in your S3 bucket
REGION = "<your_aws_region>"  # AWS region where your bucket is located

def process_one_video():
    """
    Fetch a highlight URL from the JSON file in S3, download the video, and save it back to S3.
    """
    try:
        # Create an S3 client (assumes IAM role "HighlightProcessorRole")
        s3 = boto3.client("s3", region_name=REGION)

        # Retrieve the JSON file from the S3 bucket
        print("Fetching JSON file from S3...")
        response = s3.get_object(Bucket=S3_BUCKET_NAME, Key=INPUT_KEY)
        json_content = response['Body'].read().decode('utf-8')  # Read and decode the file
        highlights = json.loads(json_content)  # Parse the JSON content

        # Extract the first video URL from the JSON data
        video_url = highlights["data"][0]["url"]  # Adjust the key path as per your JSON structure
        print(f"Processing video URL: {video_url}")

        # Download the video from the URL
        print("Downloading video...")
        video_response = requests.get(video_url, stream=True)  # Stream the video to avoid memory overflows
        video_response.raise_for_status()  # Raise an error if the download fails

        # Prepare the video for upload to S3
        video_data = BytesIO(video_response.content)  # Load the video content into an in-memory file object

        # Save the video back to the S3 bucket
        print("Uploading video to S3...")
        s3.put_object(
            Bucket=S3_BUCKET_NAME,  # Specify the target bucket
            Key=OUTPUT_KEY,  # Specify the key (file path) for the video in the bucket
            Body=video_data,  # Pass the video data to the S3 client
            ContentType="video/mp4"  # Specify the content type
        )
        print(f"Video uploaded successfully: s3://{S3_BUCKET_NAME}/{OUTPUT_KEY}")
    except Exception as e:
        # Handle errors during processing
        print(f"Error during video processing: {e}")

# Entry point for the script
if __name__ == "__main__":
    process_one_video()  # Start processing the video
