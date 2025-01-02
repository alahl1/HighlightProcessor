import subprocess
import time

def run_script(script_name, retries=3, delay=30):
    """
    Run a script with retry logic and a delay.
    
    Args:
        script_name (str): Name of the script to execute.
        retries (int): Number of retry attempts if the script fails.
        delay (int): Time (in seconds) to wait between retries.
    """
    attempt = 0
    while attempt < retries:
        try:
            print(f"Running {script_name} (attempt {attempt + 1}/{retries})...")
            subprocess.run(["python", script_name], check=True)  # Run the script
            print(f"{script_name} completed successfully.")
            return
        except subprocess.CalledProcessError as e:
            print(f"Error running {script_name}: {e}")
            attempt += 1
            if attempt < retries:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)  # Wait before retrying
            else:
                print(f"{script_name} failed after {retries} attempts.")
                raise e  # Re-raise the exception after all retries

def main():
    """
    Main function to run all scripts in sequence with retry logic.
    """
    try:
        # Step 1: Run fetch.py
        run_script("fetch.py", retries=3, delay=30)

        # Step 2: Add a buffer time to ensure fetch results are available
        print("Waiting for resources to stabilize...")
        time.sleep(60)  # Wait for 1 minute before running the next script

        # Step 3: Run process_one_video.py
        run_script("process_one_video.py", retries=3, delay=30)

        # Step 4: Add a buffer time to ensure the processed video is ready
        print("Waiting for resources to stabilize...")
        time.sleep(60)  # Wait for 1 minute before running the next script

        # Step 5: Run mediaconvert_process.py
        run_script("mediaconvert_process.py", retries=3, delay=30)

        print("All scripts executed successfully.")
    except Exception as e:
        print(f"Pipeline failed: {e}")

if __name__ == "__main__":
    main()
