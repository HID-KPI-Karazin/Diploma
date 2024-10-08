# Diploma
ClickUp/CBR BSc diploma project
Цей посібник пояснює, як розгорнути CBR-функціонал в ClickUp.
CBR-cистема призначена для автоматизації процесу управління завданнями,
пропонуючи рішення на основі схожих минулих проблем завдань за допомогою
алгоритмів найближчого сусіда за косинусною подібністю і векторизації TF-IDF.
Система інтегрує ClickUp з Google Sheets для зберігання даних про прецеденти
та використовує сервер Flask для внутрішньої логіки.

Етапи розгортання:
1. Налаштуйте 'config.json'
{
    "client_id": "YOUR_CLICKUP_CLIENT_ID",
    "client_secret": "YOUR_CLICKUP_CLIENT_SECRET",
    "redirect_uri": "http://localhost:5000/callback",
    "folder_id": "YOUR_CLICKUP_FOLDER_ID",
    "google_credentials": "path/to/creds.json"
}
1.1) Ідентифікатор та секретний ключ клієнта можна отримати при створенні додатку
у ClickUp: Settings -> ClickUp API -> + Create an App -> Create App
1.2) Ідентифікатор папки проекту, можна отримати з посилання на
папку: https://app.clickup.com/YOUR_CLICKUP_PROJECT_ID/v/o/f/YOUR_CLICKUP_FOLDER_ID
1.3) Створіть Google Cloud Project у Google Cloud Console
1.4) Під'єднайте Google Sheets API та Google Drive API: APIs & Services -> Library
-> Пошук певного API -> Enable
1.5) Створіть повноваження для сервісного аккаунту: APIs & Services -> Credentials
-> Create Credentials -> Service Account -> Create -> Continue -> Done
1.6) Згенеруйте файл з повноваженнями 'creds.json': YOUR_SERVICE_ACCOUNT -> Email
-> Keys -> Add Key -> Create new key -> JSON -> Create
1.7) Встановіть повноваження Google у вигляді 'creds.json' у будь-яку папку для
CBR-системи за шляхом path/to/

2. Налаштування CBR-системи до роботи з проектом
2.1) Завантажте Python 3.7
2.2) Введіть у консолі на Windows 'pip install -r requirements.txt' для встановлення
необхідних бібліотек
2.3) Для ручного тестування системи, необхідно встановити Postman
2.4) Запустіть 'auth.py' для отримання токену доступу до проекту ClickUp та перейдіть
за посиланням: http://127.0.0.1:5000
2.5) З'єднайте CBR-систему з проектом в ClickUp та покиньте сторінку, коли отримання
токену доступу підтверджено
2.6) Для роботи з CBR-системою запустіть Flask сервер 'app.py'

3. Робота з проектом за допомогою CBR-системи
3.1) Для автономної обробки завдань запустіть 'task_processor.py'
3.2) Для ручної обробки завдань у Postman сформуйте запит на створення/оновлення
завдання в ClickUp: метод POST: http://127.0.0.1:5000/new_task (або http://127.0.0.1:5000/update_task), Headers: Content-Type - application/json, Body:
{
  "id": "YOUR_TASK_ID",
  "name": "YOUR_TASK_NAME",
  "description": "YOUR_TASK_DESC",
  "tags": [{"name": "YOUR_TASK_TAG_1"}, {"name": "YOUR_TASK_TAG_2"}],
  "custom_fields": [{"name": "Solution", "value": ""}, {"name": "Story Points", "value": "YOUR_TASK_STORYPOINTS"}]
}
