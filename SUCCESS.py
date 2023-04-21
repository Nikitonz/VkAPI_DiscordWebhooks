'''



публиковать записи, начиная от самой старой, заканчивая самой недавней.
не публиковать запись, если она уже существует в discord канале
'''
import vk_api
import requests
import json

# Параметры для авторизации в VK API
login = '+375295747029'
password = 'rather_good1212343455'
group_id = '218717760'
access_token = 'qKlPXt5e43RC0OjHa6AX'

# Авторизация в VK API
vk_session = vk_api.VkApi(login=login, password=password)
vk_session.auth(token_only=True)

# Получение последних 10 новостей из сообщества
vk = vk_session.get_api()
vk_news = vk.newsfeed.get(filters='post', source_ids='-' + group_id, count=10)
vk_news_json = json.loads(json.dumps(vk_news))

# Перебор новостей и отправка в Discord-канал
for item in vk_news_json['items']:
    message = item['text']
    # Если новость содержит прикрепленные файлы, добавляем их в сообщение
    if 'attachments' in item:
        for attach in item['attachments']:
            # Если вложение - фотография
            if attach['type'] == 'photo':
                sizes = attach['photo']['sizes']
                # Находим ссылку на самую большую фотографию
                max_size = sizes[0]
                for size in sizes:
                    if size['width'] > max_size['width']:
                        max_size = size
                message += '\n' + max_size['url']
            # Если вложение - видео
            elif attach['type'] == 'video':
                message += '\n' + 'https://vk.com/video{}_{}'.format(
                    attach['video']['owner_id'], attach['video']['id'])
            # Если вложение - документ
            elif attach['type'] == 'doc':
                message += '\n' + attach['doc']['url']
            # Если вложение - архив
            elif attach['type'] == 'audio_message':
                message += '\n' + attach['audio_message']['link_mp3']
    # Отправляем сообщение в Discord-канал
    webhook_url = 'https://discord.com/api/webhooks/1080543128387321906/E5KWy8Mnf_VB-V25ayvF38z2X2kP_-udBf45CxZFPLe1pbhR3E0DvGhlgkiwCSCuM9NP'
    data = {
        'content': message
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(webhook_url, data=json.dumps(data), headers=headers)
    if response.status_code != 204:
        print('Ошибка отправки сообщения:', response.text)
