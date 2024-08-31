import requests

# Define the API URL (replace with your local server address if different)
api_url = "http://127.0.0.1:8000/ask"

# Define the payload with the question and session_id
payload = {
    "question": "Explain further",
    "session_id": "test_session_1"
}

# Make the POST request to the API
response = requests.post(api_url, json=payload)

# Check if the request was successful
if response.status_code == 200:
    # Print the response from the API
    print("AI Response:", response.json()["answer"])
else:
    print(f"Error: {response.status_code}, {response.text}")
