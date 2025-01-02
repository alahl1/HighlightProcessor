import boto3  # AWS SDK for interacting with AWS services
import requests  # HTTP library for making API calls
import json  # For handling JSON data

# Constants
API_URL = "https://sport-highlights-api.p.rapidapi.com/basketball/highlights"  # API endpoint for fetching highlights
RAPIDAPI_KEY = "<your_rapidapi_key>"  # Replace with your RapidAPI key (required for authentication)
S3_BUCKET_NAME = "<your_bucket_name>"  # Replace with your S3 bucket name (where data will be stored)
REGION = "<your_aws_region>"  # AWS region where the S3 bucket is located (e.g., us-east-1)

# Query parameters for the API request
QUERY_PARAMS = {
    "date": "2023-12-01",  # The date of highlights to fetch in YYYY-MM-DD format
    "leagueName": "NCAA",  # Specify the league name (adjust based on your API plan)
    "limit": 10  # Maximum number of highlights to fetch
}

# Headers for the API request
HEADERS = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,  # Authentication key for the RapidAPI service
    "X-RapidAPI-Host": "sport-highlights-api.p.rapidapi.com"  # The host for the API endpoint
}

def fetch_highlights():
    """
    Fetch basketball highlights from the API.
    """
    try:
        # Make an HTTP GET request to the API endpoint with headers and query parameters
        response = requests.get(API_URL, headers=HEADERS, params=QUERY_PARAMS, timeout=120)
        response.raise_for_status()  # Raise an exception if the HTTP status code indicates an error
        highlights = response.json()  # Parse the API response JSON data
        print("Highlights fetched successfully!")  # Log success message
        return highlights  # Return the parsed highlights data
    except requests.exceptions.RequestException as e:
        # Handle exceptions that occur during the API call
        print(f"Error fetching highlights: {e}")  # Log the error message
        return None  # Return None if the fetch fails

def save_to_s3(data, file_name):
    """
    Save data to an S3 bucket.
    """
    try:
        # Create an S3 client to interact with Amazon S3
        s3 = boto3.client("s3", region_name=REGION)

        # Ensure the S3 bucket exists
        try:
            s3.head_bucket(Bucket=S3_BUCKET_NAME)  # Check if the bucket exists
            print(f"Bucket {S3_BUCKET_NAME} exists.")  # Log if the bucket exists
        except Exception:
            print(f"Bucket {S3_BUCKET_NAME} does not exist. Creating...")  # Log if the bucket needs to be created
            # Create the bucket in the specified region
            if REGION == "us-east-1":  # Special case for us-east-1 (no LocationConstraint needed)
                s3.create_bucket(Bucket=S3_BUCKET_NAME)
            else:
                s3.create_bucket(
                    Bucket=S3_BUCKET_NAME,
                    CreateBucketConfiguration={"LocationConstraint": REGION}  # Specify bucket region
                )
            print(f"Bucket {S3_BUCKET_NAME} created successfully.")  # Log bucket creation success

        # Define the key (path) for the file in the S3 bucket
        s3_key = f"highlights/{file_name}.json"  # The file will be stored under 'highlights/' folder in the bucket

        # Upload the JSON data to the S3 bucket
        s3.put_object(
            Bucket=S3_BUCKET_NAME,  # Specify the target bucket
            Key=s3_key,  # Specify the key (file path) in the bucket
            Body=json.dumps(data),  # Convert the data to JSON string format
            ContentType="application/json"  # Specify the content type as JSON
        )
        print(f"Highlights saved to S3: s3://{S3_BUCKET_NAME}/{s3_key}")  # Log success message
    except Exception as e:
        # Handle exceptions that occur during the S3 operation
        print(f"Error saving to S3: {e}")  # Log the error message

def process_highlights():
    """
    Main function to fetch and process basketball highlights.
    """
    print("Fetching highlights...")  # Log the start of the fetch process
    highlights = fetch_highlights()  # Call the fetch_highlights function to get the data
    if highlights:  # Check if highlights were fetched successfully
        print("Saving highlights to S3...")  # Log the start of the save process
        save_to_s3(highlights, "basketball_highlights")  # Call save_to_s3 to upload the data to S3

# Entry point for the script
if __name__ == "__main__":
    process_highlights()  # Execute the process_highlights function when the script is run
