import json
import os
import pandas as pd
from datetime import datetime
from pathlib import Path


JSON_FILENAME = "message_"


def parse_from_json(path=None):

    path = path or os.getcwd()
    path = Path(path)
    if not os.path.isdir(path):
        raise NotADirectoryError(f"{path} is not a directory")
    messages_dir = [path / mdir for mdir in os.listdir(path)]
    all_files = [msg_dir / json_file for msg_dir in messages_dir for json_file in os.listdir(msg_dir) if json_file.startswith(JSON_FILENAME)]

    chat_data = []
    threads = set()
    chat_cols = ['participants', 'title',
                 'is_still_participant', 'thread_type', 'thread_path']
    message_data = []
    msg_cols = ['thread_path', 'timestamp', 'msg',
                'sender', 'msg_type', 'sticker', 'photos', 'videos']

    for json_file in all_files:
        with open(json_file) as json_file:
            current_chat = json.load(json_file)

        thread_path = current_chat['thread_path']
        
        participants = [x['name']
                        for x in current_chat.get('participants', '')]
        title = current_chat.get('title', '')
        is_still_participant = current_chat.get('is_still_participant', '')
        thread_type = current_chat.get('thread_type', '')

        # avoid duplicate chat entries for chats with multiple message_x.json files
        if thread_path not in threads:
            threads.add(thread_path)
            chat_data.append(
                [participants, title, is_still_participant, thread_type, thread_path])

        for msg in current_chat['messages']:
            ts = msg.get('timestamp_ms', 0) // 1000
            body = msg.get('content', None)
            sender = msg.get('sender_name', None)
            msg_type = msg.get('type', None)
            sticker = msg.get('sticker', None)
            photos = msg.get('photos', None)
            videos = msg.get('videos', None)

            message_data.append(
                [thread_path, ts, body, sender, msg_type, sticker, photos, videos])

    chat_df = pd.DataFrame(chat_data, columns=chat_cols)
    chat_df.set_index('thread_path', inplace=True)
    msg_df = pd.DataFrame(message_data, columns=msg_cols)
    msg_df['timestamp'] = msg_df['timestamp'].apply(datetime.fromtimestamp)

    return chat_df, msg_df
