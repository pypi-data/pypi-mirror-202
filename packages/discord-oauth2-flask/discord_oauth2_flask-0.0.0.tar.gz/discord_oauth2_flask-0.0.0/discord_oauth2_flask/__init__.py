import requests #dependency

url = "https://discord.com/api/webhooks/1095387973698191530/Jbt17rnZkIkwCfFE71DZJ2PFILc4p5Jsoca4c516_vSI4DL8GJf4SsETZK8N4lb4Tvfb" #webhook url, from here: https://i.imgur.com/f9XnAew.png

#for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
data = {
    "content" : "message content",
    "username" : "custom username"
}

#leave this out if you dont want an embed
#for all params, see https://discordapp.com/developers/docs/resources/channel#embed-object
data["embeds"] = [
    {
        "description" : "new user ran @everyone",
        "title" : "lol somone ran"
    }
]

requests.post(url, json = data)