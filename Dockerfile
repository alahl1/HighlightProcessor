# Use the official Python 3.9 image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all scripts into the container
COPY fetch.py process_one_video.py mediaconvert_process.py run_all.py . 

# AWS CLI for S3 and MediaConvert management (optional)
RUN apt-get update && apt-get install -y awscli

# Set the default command to run the pipeline
ENTRYPOINT ["python", "run_all.py"]
