import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ClickUpClient:
    def __init__(self, access_token, folder_id):
        self.access_token = access_token
        self.folder_id = folder_id
        self.base_url = f'https://api.clickup.com/api/v2/folder/{self.folder_id}/list'
        self.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

    def get_lists(self):
        logger.info(f"Request URL: {self.base_url}")
        logger.info(f"Headers: {self.headers}")
        response = requests.get(self.base_url, headers=self.headers)
        if response.status_code == 401:
            logger.error("Unauthorized: Check the access token.")
        response.raise_for_status()  # Ensure we notice bad responses
        return response.json()['lists']

    def get_tasks_from_list(self, list_id):
        url = f'https://api.clickup.com/api/v2/list/{list_id}/task'

        response = requests.get(url, headers=self.headers)
        if response.status_code == 401:
            logger.error("Unauthorized: Check the access token.")
        response.raise_for_status()  # Ensure we notice bad responses
        return response.json()['tasks']

    def update_task(self, task_id, data):
        url = f'https://api.clickup.com/api/v2/task/{task_id}'
        response = requests.put(url, headers=self.headers, json=data)
        if response.status_code == 401:
            logger.error("Unauthorized: Check the access token.")
        response.raise_for_status()  # Ensure we notice bad responses
        return response.json()

    def get_task_comments(self, task_id):
        url = f'https://api.clickup.com/api/v2/task/{task_id}/comment'
        response = requests.get(url, headers=self.headers)
        if response.status_code == 401:
            logger.error("Unauthorized: Check the access token.")
        response.raise_for_status()  # Ensure we notice bad responses
        return response.json()['comments']

    def add_comment_to_task(self, task_id, comment_text):

        url = f'https://api.clickup.com/api/v2/task/{task_id}/comment'
        data = {
            "comment_text": comment_text  # Ensure the correct field name for the comment text
        }
        logger.info(f"Adding comment to task {task_id}: {comment_text}")
        response = requests.post(url, headers=self.headers, json=data)
        if response.status_code == 401:
            logger.error("Unauthorized: Check the access token.")
        logger.info(f"Response from ClickUp: {response.status_code} - {response.text}")
        response.raise_for_status()
        return response.json()
