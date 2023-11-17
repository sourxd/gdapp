import base64

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import service_account
from googleapiclient.http import MediaInMemoryUpload
from googleapiclient.discovery import build

from gdapp.settings import SERVICE_ACCOUNT_FILE, SCOPES, FOLDER_ID


def index(request):
    return JsonResponse({'message': 'go to */upload/'})

@csrf_exempt
def create_file_in_drive(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        name = request.POST.get('name')
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

        # Создаем экземпляр API Google Drive
        drive_service = build('drive', 'v3', credentials=credentials)

        # Создаем пустой документ в Google Drive
        file_metadata = {
            'name': name,
            'parents': [FOLDER_ID]
        }
        # Создаем содержимое файла
        media = MediaInMemoryUpload(data.encode(), mimetype='text/plain')
        # Создаем файл на Google Drive
        file = drive_service.files().create(
            body=file_metadata, media_body=media, fields='id').execute()
        return JsonResponse({'file_id': file['id']})
    else:
        return JsonResponse({'message': 'Invalid request method.'})
