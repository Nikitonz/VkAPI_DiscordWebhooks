
import vk_api
import requests
import json
import os
logi = ''
passw = ''

GROUP_ID = ''
grid = 218717760
DISCORD_WEBHOOK_URL = ''
POSTS_FILE = 'posts.txt'
ACCESS_TOKEN = ''

vk_session = vk_api.VkApi(token=os.environ.get(ACCESS_TOKEN), )
vk = vk_session.get_api()

vk_session = vk_api.VkApi(login=logi, password=passw)
vk_session.auth(token_only=True)

#-------------------
vk = vk_session.get_api()
vk_news = vk.newsfeed.get(filters='post', source_ids='-' + GROUP_ID, count=10)
vk_news_json = json.loads(json.dumps(vk_news))
#----------------------


try:
    user_info = vk.users.get()
    print(f"Successfully connected to VK API. User ID: {user_info[0]['id']}")
except vk_api.exceptions.ApiError as e:
    print(f"API error occurred: {e}")
except vk_api.exceptions.AuthError:
    print("Authorization failed. Check your access token.")



try:
    response = vk.wall.get(owner_id='-' + GROUP_ID, count=10, filter='owner')
    with open(POSTS_FILE, 'a+') as f:
        f.seek(0)
        published_posts = f.read().splitlines()
    if 'items' in response:
        posts = response['items']
        for post in reversed(posts):
            post_id = str(post['id'])
            if post_id in published_posts:
                continue
            post_date = post['date']
            post_text = post['text']

            attachments = []
            if 'attachments' in post:
                for attachment in post['attachments']:
                    if attachment['type'] == 'photo':
                        sizes = attachment['photo']['sizes']
                        max_size = max(sizes, key=lambda x: x['width'])
                        attachments.append(max_size['url'])
                    elif attachment['type'] == 'link':
                        attachments.append(attachment['link']['url'])
                    elif attachment['type'] == 'doc':
                        attachments.append(attachment['doc']['url'])

            discord_data = {
                "username": "VK Group",
                "avatar_url": "https://i.imgur.com/AIU9QIv.png",
                "content": f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n{post_text}\n{' '.join(attachments)}▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n",
                "embeds": []
            }


            response = requests.post(DISCORD_WEBHOOK_URL, data=json.dumps(discord_data),
                                     headers={"Content-Type": "application/json"})


            if response.status_code != 204:
                print(f"Error posting to Discord: {response.text}")
            else:
                print(f"Successfully posted VK post {post_id} to Discord")

                with open(POSTS_FILE, 'a') as f:
                    f.write(str(post_id) + '\n')
    else:
        print('No posts...')
except vk_api.exceptions.AuthError as e:
    print("Auth fail..."+e)
except vk_api.exceptions.ApiError as e:
    print(f"API error occurred: {e}")
