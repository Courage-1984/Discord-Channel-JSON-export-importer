# Discord Channel JSON export importer
Import Discord Channel JSON Exports created by `DiscordChatExporter` at: https://github.com/Tyrrrz/DiscordChatExporter

A Script/Bot to send messages (exported as json) to a Discord server channel.

See 'send_messages.py' for script.

## Steps for `DiscordChatExporter`

1. Download [DiscordChatExporter](https://github.com/Tyrrrz/DiscordChatExporter)
2. You need an authorisation token to access what your Discord account can access.
3. Head over to:

```sh
  https://discord.com/
```

on your browser and log in to your Discord account.

4. Press `Ctrl+Shift+I`
5. Navigate to the **Network** tab and then click on the **XHR** button.
6. In the table look at the **File** column and look for and click on either the line named "**library**" OR the line named "**country-code**". Refresh if you don't see anything.
7. In the right section, under headers, look for the authorisation line.
8. Copy the text next to authorisation.
9. If you struggle with step 2>8 try the following:

![dc auth token](https://github.com/Courage-1984/Discord-Channel-JSON-export-importer/assets/18268669/e200f652-856b-4cb5-9ab2-6c194a51623c)

10. Open `DiscordChatExporter` and paste your authorisation token at the top to access the servers and channels your account has access to.
11. Choose a channel you want to export
12. Click the download icon bottom right
13. Choose an output path (ideally this should be in the same directory as the script 'send_messages.py' from this repo)
14. Choose `JSON` as the export format
15. Make sure the following settings are on:

![2024-05-05 14 32 23 DiscordChatExporter v2 43 0](https://github.com/Courage-1984/Discord-Channel-JSON-export-importer/assets/18268669/74ded89c-b22f-4fdf-bb6b-46385985c64c)

16. Choose an `Assets directory path` (ideally this should be in a folder in the same directory as the script 'send_messages.py' from this repo)
17. Click `export` and wait for the process to finish

## DiscordChatExporter exported messsages (JSON) importer.

1. Download the [send_messages.py](https://github.com/Courage-1984/Discord-Channel-JSON-export-importer/blob/main/send_messages.py) script in the repo above.
2. Create a folder to put the `send_messages.py` script in.
3. Open a terminal in that folder location.
4. In that terminal run the following:
```sh
  pip install discord.py
```

5. Now edit the `send_messages.py` script and add the needed values being `YOUR_BOT_TOKEN`, `guild_id`, `channel_id`, `exported-channel.json` and `messages_sent_log.txt`.

**See the following:**

- [How to Get Your Discord Bot Token](https://www.youtube.com/watch?v=aI4OmIbkJH8)

OR:

![dc bot token](https://github.com/Courage-1984/Discord-Channel-JSON-export-importer/assets/18268669/7fbb1de2-1367-4f2a-af1d-17d6c1c12042)


- [How to Get Server ID, Channel ID, User ID in Discord - Copy ID's](https://www.youtube.com/watch?v=NLWtSHWKbAI)


6. Navigate to [https://discord.com/developers/applications](https://discord.com/developers/applications) and click on your application.
7. Click on the `Bot` option in the left navbar and make sure to enable the following: `Presence Intent`, `Server Members Intent` and `Message Content Intent`.
8. Now click on the `OAuth2` option in the left navbar and copy the `Client ID`.
9. Now open [https://discordapi.com/permissions.html](https://discordapi.com/permissions.html) in a new browser tab.
10. Tick the boxes next to: `Administrator`, `Manage Messages`, `Manage Channels`, `Manage Events`, `Send Messages`, `Embed Links`, `Attach Files`, `Read Message History`, `Manage Server`, `View Channels` and `Manage Server`.
11. Now paste your `Client ID` that you copied in the `Client ID:` field at the bottom of the page.
12. Now click on the link provided at the way bottom of the page.
13. Add your bot/application to your chosen server.
14. Click Continue
15. Now in the terminal that's in the directory which has your `send_messages.py` script run the following to excecute the script/bot:
16. 
```sh
  python send_messages.py
```

16. Wait a min for bot to start up and connect.
17. Now your script/bot should run smoothly and send all the exported messages in the JSON export you provided.
18. **If the script encounters an error and doesn't move on to the next message to send, just stop the script and run it again and it will continue on the last message sent**

**PS:**

`YOUR_BOT_TOKEN`, `guild_id`, `exported-channel.json` and `messages_sent_log.txt` should all be enclosed in single qoutations while:

`channel_id` should not be enclosed in qoutations at all.

***

