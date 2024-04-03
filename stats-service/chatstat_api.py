import json
import os
from flask import Flask, Response

import chatstat_lib
import chatstat_loader

app = Flask(__name__)
workdir = "C:\\Users\\Daniel Rogowski\\Desktop\\elo"


def get_stats(chatstat: chatstat_lib.ChatStat):
    time_df = chatstat.generate_time_indexed_df(chatstat.msg_df)

    metrics = chatstat.biggest_chat()
    yield f"data: {json.dumps(metrics)}\n\n"

    metrics = chatstat.sent_from(omit_first=True)
    yield f"data: {json.dumps(metrics)}\n\n"

    metrics = chatstat.msg_types()
    yield f"data: {json.dumps(metrics)}\n\n"

    metrics = chatstat.yearly_graph(time_df)
    yield f"data: {json.dumps(metrics)}\n\n"

    metrics = chatstat.hourly_graph(time_df)
    yield f"data: {json.dumps(metrics)}\n\n"

    metrics = chatstat.monthly_graph(time_df)
    yield f"data: {json.dumps(metrics)}\n\n"

    metrics = chatstat.minutely_graph(time_df)
    yield f"data: {json.dumps(metrics)}\n\n"

    metrics = chatstat.daily_graph(time_df)
    yield f"data: {json.dumps(metrics)}\n\n"

    metrics = chatstat.weekday_graph(time_df)
    yield f"data: {json.dumps(metrics)}\n\n"

    metrics = chatstat.chat_counts()
    yield f"data: {json.dumps(metrics)}\n\n"

    metrics = chatstat.word_counts(length=3)
    yield f"data: {json.dumps(metrics)}\n\n"

    metrics = chatstat.word_counts(length=5)
    yield f"data: {json.dumps(metrics)}\n\n"

    metrics = chatstat.word_counts(length=7)
    yield f"data: {json.dumps(metrics)}\n\n"


@app.route("/stats/<dir_name>")
def hello_world(dir_name: str):
    dir_path = os.path.join(workdir, dir_name)
    chat_df, msg_df = chatstat_loader.parse_from_json(dir_path)
    chatstat = chatstat_lib.ChatStat(chat_df, msg_df)
    return Response(get_stats(chatstat), content_type="text/event-stream")


app.run(port=2137)
