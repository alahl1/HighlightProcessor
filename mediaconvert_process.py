import boto3  # AWS SDK for interacting with AWS services
import json  # For handling JSON data

# Constants
REGION = "<your_aws_region>"  # AWS region where MediaConvert and S3 are located
MEDIACONVERT_ROLE = "HighlightProcessorRole"  # IAM role for MediaConvert
INPUT_S3_URL = "s3://<your_bucket_name>/videos/first_video.mp4"  # Input video file in S3
OUTPUT_S3_URL = "s3://<your_bucket_name>/processed_videos/"  # Output folder in S3
MEDIACONVERT_ENDPOINT = "<your_mediaconvert_endpoint>"  # MediaConvert endpoint URL

def create_job():
    """
    Create a MediaConvert job to process a video.
    """
    try:
        # Initialize MediaConvert client
        mediaconvert = boto3.client(
            "mediaconvert", 
            region_name=REGION, 
            endpoint_url=MEDIACONVERT_ENDPOINT
        )

        # Define the MediaConvert job settings
        job_settings = {
            "Role": f"arn:aws:iam::<your_account_id>:role/{MEDIACONVERT_ROLE}",
            "Settings": {
                "Inputs": [
                    {
                        "AudioSelectors": {
                            "Audio Selector 1": {
                                "DefaultSelection": "DEFAULT"
                            }
                        },
                        "FileInput": INPUT_S3_URL,  # Input video file from S3
                        "VideoSelector": {}
                    }
                ],
                "OutputGroups": [
                    {
                        "Name": "File Group",
                        "OutputGroupSettings": {
                            "Type": "FILE_GROUP_SETTINGS",
                            "FileGroupSettings": {
                                "Destination": OUTPUT_S3_URL  # Output folder in S3
                            }
                        },
                        "Outputs": [
                            {
                                "ContainerSettings": {
                                    "Container": "MP4",  # Output format
                                    "Mp4Settings": {}
                                },
                                "VideoDescription": {
                                    "CodecSettings": {
                                        "Codec": "H_264",
                                        "H264Settings": {
                                            "Bitrate": 5000000,  # Bitrate for the video
                                            "RateControlMode": "CBR",  # Constant bitrate
                                            "QualityTuningLevel": "SINGLE_PASS",  # Quality level
                                            "CodecProfile": "MAIN"  # H.264 profile
                                        }
                                    },
                                    "ScalingBehavior": "DEFAULT",
                                    "TimecodeInsertion": "DISABLED"
                                },
                                "AudioDescriptions": [
                                    {
                                        "CodecSettings": {
                                            "Codec": "AAC",
                                            "AacSettings": {
                                                "Bitrate": 64000,  # Audio bitrate
                                                "CodingMode": "CODING_MODE_2_0",  # Stereo
                                                "SampleRate": 48000  # Sampling rate
                                            }
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            "AccelerationSettings": {"Mode": "DISABLED"},
            "StatusUpdateInterval": "SECONDS_60",
            "Priority": 0
        }

        # Create the MediaConvert job
        response = mediaconvert.create_job(Settings=job_settings)
        print("MediaConvert job created successfully:")
        print(json.dumps(response, indent=4))  # Print job response
    except Exception as e:
        # Handle errors during MediaConvert job creation
        print(f"Error creating MediaConvert job: {e}")

# Entry point for the script
if __name__ == "__main__":
    create_job()  # Create a MediaConvert job
