import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import logging
import json
import requests
from clickup_client import ClickUpClient
from cbr_system import CBRSystem

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
class TaskProcessor:
    def __init__(self, clickup_client, cbr_system):
        self.clickup_client = clickup_client
        self.cbr_system = cbr_system

    def process_tasks(self):
        lists = self.clickup_client.get_lists()
        for lst in lists:
            tasks = self.clickup_client.get_tasks_from_list(lst['id'])
            for task in tasks:
                self.process_task(task)

    def process_task(self, task):
        task_id = task['id']
        description = task['name']
        details = task.get('description', '')
        tags = [tag['name'] for tag in task.get('tags', [])]
        solution = ''
        for field in task.get('custom_fields', []):
            if field['name'] == 'Solution':
                solution = field.get('value', '')

        comments = self.clickup_client.get_task_comments(task_id)
        logger.info("Processing task: %s", task_id)
        logger.info("Details: %s", details)
        logger.info("Tags: %s", tags)
        logger.info("Solution: %s", solution)
        logger.info("Comments: %s", comments)

        if details and tags and not solution and not comments:
            start_time = time.time()
            cases = self.cbr_system.get_cases()
            logger.info("Retrieved cases: %s", cases)
            most_similar_case, search_time = self.cbr_system.find_most_similar_case(details, cases)
            logger.info("Most similar case: %s", most_similar_case)
            comment_text = f"За CBR-аналізом було знайдено наступне схоже рішення:\n{most_similar_case['Solution']}"
            try:
                response = self.clickup_client.add_comment_to_task(task_id, comment_text)
                logger.info("Added comment to task: %s", task_id)
                logger.info("Response from ClickUp: %s", response)
            except Exception as e:
                logger.error("Error adding comment to task: %s, %s", task_id, str(e))

            offer_time = time.time() - start_time
            logger.info("Offer time: %s ms", offer_time * 1000)
        else:
            logger.info(f'Task {task_id} does not meet the criteria for CBR analysis.')

def setup_google_sheets(creds_path):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    client = gspread.authorize(creds)
    sheet = client.open("Project Problems and Solutions").worksheet('CaseBase')
    return sheet

if __name__ == '__main__':
    import json

    with open('access_token.txt', 'r') as f:
        access_token = f.read().strip()
    logger.info("Access Token: %s", access_token)

    with open('config.json', 'r') as f:
        config = json.load(f)
    logger.info("Config: %s", config)

    clickup_client = ClickUpClient(access_token=access_token, folder_id=config['folder_id'])
    google_sheets_client = setup_google_sheets(config['google_credentials'])
    cbr_system = CBRSystem(google_sheets_client)
    task_processor = TaskProcessor(clickup_client, cbr_system)

    while True:
        try:
            task_processor.process_tasks()
        except requests.exceptions.HTTPError as e:
            logger.error("HTTPError: %s", str(e))
        except Exception as e:
            logger.error("General Error: %s", str(e))
        time.sleep(60)  # Poll every 1 minute
