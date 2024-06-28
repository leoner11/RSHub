import requests
import json

# URL of the Flask server endpoint
url = "http://127.0.0.1:5000/check_job_status"

# Data to send in the POST request
data = {
    "username": "user1",
    "project_name": "projectA",
    "task_name": "task1"
}

# Headers for the request
headers = {
    "Content-Type": "application/json"
}


def check_job_status(url, data, headers):
    try:
        # Send POST request
        response = requests.post(url, headers=headers, data=json.dumps(data))

        # Check the response status code
        if response.status_code == 200:
            print("Job status retrieved successfully:")
            print(response.json())
        elif response.status_code == 400:
            print("Error: Missing required parameters")
        elif response.status_code == 404:
            print("Error: No jobs found for the given parameters")
        else:
            print(f"Error: Unexpected response {response.status_code}")
            print(response.json())
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    check_job_status(url, data, headers)
