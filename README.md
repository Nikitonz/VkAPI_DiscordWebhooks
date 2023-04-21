# VkAPI_DiscordWebhooks
 sends content from VK group to Discord group via webhooking

- Introduction
  -This code provides you to copy content of your posts of vk groups and move it into discord channels(this channels, groups must be specified, read Configuration branch) 
- Requirements
  -Python ver. 3.8 or above installed
  -vk_api module installed. (in cmd, use ```pip install vk_api```)
-Configuration
  -First, input your login & password into *logi*, *passw* variables, to get acess to VK API Dev
  -Second, go to https://vk.com/apps?act=manage, and create your own app (standalone). Go to settings, and copy your Secure key into ACCESS_TOKEN in the *exec.py*. 
  -Third, move to your channel in Discord. Pick a branch -> integration, and create your webhook. Copy it's URL into DISCORD_WEBHOOK_URL in exec.py
  -Fourthly, get ID of vk group. To get it, you need copy int value after public, or group in address bar, or move to settings of your group
  ![image](https://user-images.githubusercontent.com/100299461/233678695-c0c067cb-b883-4d31-a583-4b82e59fbd89.png)
  

After all, just launch startbot.bat & enjoy the result like this:![image](https://user-images.githubusercontent.com/100299461/233679271-92b72a67-6001-48b6-851c-9e7823b08beb.png)

