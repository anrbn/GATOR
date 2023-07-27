import requests
import json

def get_and_print_access_token(project_id, function_name):
    url = f"https://us-central1-{project_id}.cloudfunctions.net/{function_name}"
    response = requests.get(url)

    if response.status_code == 200:
        json_data = json.loads(response.text)
        access_token = json_data.get("access_token")

        if access_token:
            print(f"Access Token: {access_token}")
        else:
            print("Error: The 'access_token' key is not present in the response.")
    else:
        print(f"Error: The request to {url} returned status code {response.status_code}.")

def main():
    # Replace 'your_project_id' and 'your_function_name' with your specific values
    get_and_print_access_token('coastal-height-389305', 'my-functionaax')

if __name__ == "__main__":
    main()
