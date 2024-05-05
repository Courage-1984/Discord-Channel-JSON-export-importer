import discord
import json
import os
import asyncio  # Import asyncio module for sleep function
import aiohttp

# Load the JSON file
with open("exported-channel.json", encoding="utf-8") as f:
    data = json.load(f)

# Create a discord client
# client = discord.Client()

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
TOKEN = "YOUR_BOT_TOKEN"

# Counter variable to keep track of the message number
message_number = 0

# File to store the last sent message number
message_log_file = "messages_sent_log.txt"

# Replace 'guild_id' and 'channel_id' with your server and channel IDs
guild_id = "guild_id"  # Replace with your server ID
channel_id = channel_id  # Replace with your channel ID

# Define intents
intents = discord.Intents.all()
intents.messages = True
# Create a discord client
client = discord.Client(intents=intents)


async def log_message_number(message_number):
    """Log the message number to a file."""
    with open(message_log_file, "w") as f:
        f.write(str(message_number))


def get_last_message_number():
    """Read the last sent message number from the file."""
    if os.path.exists(message_log_file):
        with open(message_log_file, "r") as f:
            last_message_number = f.read()
            if last_message_number.isdigit():
                return int(last_message_number)
    return 0


async def send_message_with_retry(channel, content, files, embeds, retry_count=4):
    global message_number  # Access the global message_number variable
    for i in range(retry_count):
        try:

            # Recreate the discord.File objects from file paths
            reopened_files = []
            for file in files:
                if isinstance(file, discord.File):
                    reopened_files.append(file)  # Append existing discord.File objects
                else:
                    if os.path.exists(file):
                        with open(file, "rb") as f:
                            file_data = f.read()
                        reopened_files.append(
                            discord.File(file_data, filename=os.path.basename(file))
                        )
                    else:
                        print(f"File not found: {file}")

            # message = await channel.send(content=content, files=files, embeds=embeds) # old without reopened
            message = await channel.send(content=content, files=reopened_files, embeds=embeds)

            message_number += (
                1  # Increment the message number when a message is successfully sent
            )
            print(f"Message {message_number} sent successfully.")

            await log_message_number(message_number)  # Log the message number

            return message  # Return the message object

        except discord.errors.HTTPException as e:
            print(f"Error sending message (Attempt {i + 1}/{retry_count}): {e}")
            await asyncio.sleep(3)  # Wait for 3 seconds before retrying

        except asyncio.TimeoutError:
            print(
                f"Timeout error occurred while sending message (Attempt {i + 1}/{retry_count}). Retrying..."
            )
            await asyncio.sleep(3)  # Wait for 3 seconds before retrying

    print(f"Failed to send message {message_number + 1} after multiple attempts.")
    return None  # Message sending failed after all retries


@client.event
async def on_ready():
    global message_number
    message_number = get_last_message_number()  # Get the last sent message number
    print(f"Resuming from message number {message_number}")

    # Get the channel you want to send the messages to
    guild = client.get_guild(int(guild_id))  # Make sure you define guild_id somewhere
    channel = guild.get_channel(
        int(channel_id)
    )  # Make sure you define channel_id somewhere

    # Maintain a set to keep track of the files that have been sent
    sent_files = set()

    # Loop through the messages in the JSON file
    for index, msg in enumerate(
        data["messages"][message_number:], start=message_number
    ):
        # for msg in data["messages"]:

        # Prepare attachments
        attachments = []
        for attachment in msg.get("attachments", []):
            if "path" in attachment:

                file_path = attachment["path"]
                _, ext = os.path.splitext(file_path)
                if ext:
                    with open(file_path, "rb") as f:
                        file_data = f.read()
                    attachments.append(
                        discord.File(file_data, filename=os.path.basename(file_path))
                    )
                    if os.path.exists(file_path):
                        with open(file_path, 'rb') as file:
                            file_data = f.read()
                        attachments.append(discord.File(file_data, filename=os.path.basename(file_path)))
                    else:
                        print(f"File not found: {file_path}")

                        print(f"Skipping file path without extension: {file_path}")

            elif "url" in attachment:
                # Check if the URL is a well-formed URL
                if attachment["url"].startswith("http://") or attachment[
                    "url"
                ].startswith("https://"):
                    attachments.append(
                        discord.File(attachment["url"])
                    )  # If it's a URL, add it as an attachment
                else:
                    # If it's not a URL, assume it's a file path and add it as an attachment
                    attachments.append(discord.File(attachment["url"]))

        # Prepare embeds
        embeds = []
        for embed in msg.get("embeds", []):

            # if "description" not in embed:
            #     continue  # Skip this embed if description is missing

            # Check if "description" is present in embed
            if "description" not in embed or not embed["description"]:
                embed["description"] = (
                    "lorem ipsum"  # Set description to an empty string if it's missing or empty
                )

            # Check if the color value is a string
            if "color" in embed and isinstance(embed["color"], str):
                # Convert the color value to an integer using the int() function with base 16 for hexadecimal conversion
                color_value = int(embed["color"].lstrip("#"), 16)
                embed["color"] = color_value

            # Check if "image" is present in embed and contains a "url"
            if "image" in embed and "url" in embed["image"]:
                image_url = embed["image"]["url"]
                if image_url.startswith("http://") or image_url.startswith("https://"):
                    # If the URL is a valid web URL, add it as an attachment
                    attachments.append(discord.File(image_url))
                else:

                    # Check if the file has an extension
                    _, ext = os.path.splitext(image_url)
                    if ext:

                        if os.path.isfile(image_url):
                            try:
                                # Attempt to open the file
                                with open(image_url, "rb") as f:
                                    file_data = f.read()
                                attachments.append(
                                    discord.File(
                                        file_data, filename=os.path.basename(image_url)
                                    )
                                )
                            except UnicodeDecodeError:
                                # Skip adding the file if it cannot be opened
                                print(
                                    f"UnicodeDecodeError: Error opening image_url: {image_url}"
                                )
                            # except Exception as e:
                            #     # Skip adding the file if it raises any other exception
                            #     print(f"Exception as e: Error processing image_url: {e}")

                        else:
                            # If the file does not exist locally, skip adding it
                            print(f"image_url file not found: {image_url}")

                    else:
                        print(f"Skipping file path without extension: {image_url}")

            # Check if "thumbnail" is present in embed and contains a "url"
            if "thumbnail" in embed and "url" in embed["thumbnail"]:

                thumbnail_url = embed["thumbnail"]["url"]
                print(f"thumbnail_url {thumbnail_url}")

                # Normalize the file path to ensure it's in a valid format
                thumbnail_url_normalized = os.path.normpath(thumbnail_url)
                print(f"thumbnail_url_normalized {thumbnail_url_normalized}")

                thumbnail_url_fixed = thumbnail_url.replace("\\\\", "\\")
                print(f"thumbnail_url_fixed {thumbnail_url_fixed}")
                file_path_old = embed["thumbnail"]["url"]
                print(f"file_path_old {file_path_old}")

                file_path = file_path_old.replace("\\", "/")
                print(f"file_path {file_path}")

                # Add the fixed thumbnail URL to the embed
                embed["thumbnail"]["url"] = file_path

                file_path_org = file_path_old.replace("\\", "\\\\")
                print(f"file_path_org {file_path_org}")

                #! Remove the "thumbnail" field from the embed
                # del embed["thumbnail"]

                if (
                    file_path_old not in sent_files
                    and file_path not in sent_files
                    and file_path_org not in sent_files
                    and thumbnail_url_fixed not in sent_files
                    and thumbnail_url not in sent_files
                    and thumbnail_url_normalized not in sent_files
                ):  # Check if the file has not been sent already

                    print(f"sent_files {sent_files}")

                    sent_files.add(
                        thumbnail_url_fixed
                    )  # Add the file to the set of sent files
                    sent_files.add(
                        file_path_old
                    )  # Add the file to the set of sent files
                    sent_files.add(file_path)  # Add the file to the set of sent files
                    sent_files.add(
                        file_path_org
                    )  # Add the file to the set of sent files
                    sent_files.add(
                        thumbnail_url
                    )  # Add the file to the set of sent files
                    sent_files.add(
                        thumbnail_url_normalized
                    )  # Add the file to the set of sent files

                    print(f"{sent_files}")

                    # Print the thumbnail URL before attempting to send the message
                    print(f"Sending message with thumbnail URL: {file_path}")

                    # Check if the thumbnail URL is a web URL
                    if thumbnail_url.startswith("http://") or thumbnail_url.startswith(
                        "https://"
                    ):
                        # If the URL is a valid web URL, add it as an attachment
                        attachments.append(discord.File(thumbnail_url))
                        sent_files.add(
                            thumbnail_url
                        )  # Add the file to the set of sent files
                    else:
                        # If it's not a URL, assume it's a file path

                        # Check if the file has an extension
                        _, ext = os.path.splitext(thumbnail_url)
                        if ext:
                            if os.path.isfile(thumbnail_url):
                                try:
                                    # Attempt to open the file
                                    with open(thumbnail_url, "rb") as f:
                                        file_data = f.read()
                                    attachments.append(
                                        discord.File(
                                            file_data,
                                            filename=os.path.basename(thumbnail_url),
                                        )
                                    )
                                except UnicodeDecodeError:
                                    # Skip adding the file if it cannot be opened
                                    print(
                                        f"UnicodeDecodeError: Error opening thumbnail file: {thumbnail_url}"
                                    )
                                # except Exception as e:
                                #     # Skip adding the file if it raises any other exception
                                #     print(f"Exception as e: Error processing thumbnail file: {e}")

                            else:
                                # If the file does not exist locally, skip adding it
                                print(f"Thumbnail file not found: {thumbnail_url}")

                        else:
                            print(
                                f"Skipping file path without extension: {thumbnail_url}"
                            )

            # Check if "video" is present in embed and contains a "url"
            if "video" in embed and "url" in embed["video"]:
                video_url = embed["video"]["url"]
                if video_url.startswith("http://") or video_url.startswith("https://"):
                    # If the URL is a valid web URL, add it as an attachment
                    attachments.append(discord.File(video_url))
                else:
                    # If it's not a URL, assume it's a file path and add it as an attachment

                    # Check if the file has an extension
                    _, ext = os.path.splitext(video_url)
                    if ext:

                        if os.path.isfile(video_url):
                            try:
                                # Attempt to open the file

                                with open(video_url, "rb") as f:
                                    file_data = f.read()
                                attachments.append(
                                    discord.File(
                                        file_data, filename=os.path.basename(video_url)
                                    )
                                )
                            except UnicodeDecodeError:
                                # Skip adding the file if it cannot be opened
                                print(
                                    f"UnicodeDecodeError: Error opening video_url: {video_url}"
                                )
                            # except Exception as e:
                            #     # Skip adding the file if it raises any other exception
                            #     print(f"Exception as e: Error processing video_url: {e}")

                        else:
                            # If the file does not exist locally, skip adding it
                            print(f"video_url not found: {video_url}")

                    else:
                        print(f"Skipping file path without extension: {video_url}")

            # !########################

            # Add the embed to the list of embeds
            print(embed)  # Print the embed object for debugging purposes
            embeds.append(discord.Embed.from_dict(embed))

        # Send the message with attachments and embeds with retry logic
        # For each message sent, you would increment message_number and log it to the file
        sent_message = await send_message_with_retry(
            channel, content=msg["content"], files=attachments, embeds=embeds
        )

        if sent_message:
            if (
                sent_message.content.startswith("http://")
                or sent_message.content.startswith("https://")
            ) and not (
                sent_message.content.startswith("http://you")
                or sent_message.content.startswith("https://you")
            ):
                await channel.send(sent_message.content)
                # Increment message number and log it
                message_number += 1
                await log_message_number(message_number)
        else:
            print("Failed to send message after multiple attempts.")

        # # Send the message with attachments and embeds with retry logic
        # if not await send_message_with_retry(
        #     channel, content=msg["content"], files=attachments, embeds=embeds
        # ):
        #     print("Failed to send message after multiple attempts.")

        # Add a delay of 3 seconds between sending messages
        await asyncio.sleep(3)
        # await asyncio.sleep(422)

    # After sending all messages, close the client
    await client.close()


# Run the bot
client.run(TOKEN)
