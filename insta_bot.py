from instabot import Bot  
bot=Bot()
bot.login(username=input("enter username: "),password=input("enter password: "))
bot.follow('yasikasyal')
bot.unfollow()
bot.send_message
