from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from accounts.models import UserFile, Tag
import json
import base64
import requests
import logging


logger = logging.getLogger(__name__)


@method_decorator(login_required, name='dispatch')
class FileTagEditView(View):
    def get(self, request, file_id):
        try:
            user_file = UserFile.objects.get(id=file_id)
        except UserFile.DoesNotExist:
            return JsonResponse({'error': 'File not found'}, status=404)

        file_path = user_file.file.path

        with open(file_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')

        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Твоя задача распознать ключевые объекты на изображении, и вернуть теги по ним. Верни их в формате JSON. Формат: tags:"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                                "detail": "low"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 150
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer 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"
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers)

        if response.status_code == 200:
            data = response.json()
            content = data.get('choices', [{}])[0].get('message', {}).get('content', '')
            json_str = content.replace('```json', '').replace('```', '').strip()
            try:
                tags_data = json.loads(json_str)
                tags = tags_data.get('tags', [])
                return JsonResponse({'message': 'Tags processed successfully.', 'tags': tags}, status=200)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Failed to decode JSON from API response'}, status=500)
        else:
            return JsonResponse({'error': 'Failed to get response from the API'}, status=response.status_code)
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        file_id = data.get('file_id')
        tags = data.get('tags', [])

        try:
            user_file = UserFile.objects.get(id=file_id, user=request.user)
            for tag_name in tags:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                user_file.tags.add(tag)
            return JsonResponse({'message': 'Tags added successfully.'}, status=200)
        except UserFile.DoesNotExist:
            return JsonResponse({'error': 'File does not exist or you do not have permission to access it.'}, status=404)

    def delete(self, request, *args, **kwargs):
        data = json.loads(request.body)
        file_id = data.get('file_id')
        tags = data.get('tags', [])

        try:
            user_file = UserFile.objects.get(id=file_id, user=request.user)
            for tag_name in tags:
                tag = Tag.objects.get(name=tag_name)
                user_file.tags.remove(tag)
            return JsonResponse({'message': 'Tags removed successfully.'}, status=200)
        except UserFile.DoesNotExist:
            return JsonResponse({'error': 'File does not exist or you do not have permission to access it.'}, status=404)
        except Tag.DoesNotExist:
            return JsonResponse({'error': 'One of the tags does not exist.'}, status=404)

    def put(self, request, *args, **kwargs):
        data = json.loads(request.body)
        file_id = data.get('file_id')
        new_tags = data.get('tags', [])

        try:
            user_file = UserFile.objects.get(id=file_id, user=request.user)
            user_file.tags.clear()
            for tag_name in new_tags:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                user_file.tags.add(tag)
            return JsonResponse({'message': 'Tags updated successfully.'}, status=200)
        except UserFile.DoesNotExist:
            return JsonResponse({'error': 'File does not exist or you do not have permission to access it.'}, status=404)
