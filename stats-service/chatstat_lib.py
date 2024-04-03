from datetime import datetime
import pandas as pd


class ChatStat:

    def __init__(self, chat_df: pd.DataFrame, msg_df: pd.DataFrame):
        self.chat_df = chat_df
        self.msg_df = msg_df

    def biggest_chat(self, top=10, include_groups=True):
        """ 
        returns the largest chats overall. by default, only returns top 10
        """
        count_df = self.msg_df.groupby("thread_path").count()
        count_df.sort_values("msg", inplace=True, ascending=False)
        count_df = count_df.join(self.chat_df)
        if not include_groups:
            count_df = count_df[count_df.thread_type == 'Regular']
        count_df = count_df[:top]
        return count_df.msg.to_dict()

    def sent_from(self, chat=None, top=10, omit_first=False):
        """ 
        returns the number of messages received based on sender for the DF passed in. 
        Can be used on filtered DataFrames. by default, only returns top 10 senders
        """
        chat = self.msg_df if chat is None else chat
        start = int(omit_first)
        count_df = chat.groupby("sender").count()
        count_df.sort_values("msg", inplace=True, ascending=False)
        count_df = count_df[start:top]
        count_df = count_df.join(self.chat_df)
        return count_df.msg.to_dict()

    def msg_types(self, chat=None):
        """ 
        Takes a filtered msg_df (based on sender or chat title) and breaks down the type of messages
        """
        chat = self.msg_df if chat is None else chat
        type_dict = {
            "type": {"stickers": chat.sticker.count(), "photos": chat.photos.count(), "videos": chat.videos.count(),
                     "links": chat[[("http" in str(msg)) for msg in chat.msg]].msg.count()}}
        type_df = pd.DataFrame(type_dict)
        return type_df.type.to_dict()

    def generate_time_indexed_df(self, messages):
        """
        turns a message df to a time-indexed df with columns for
        year, month, hour and minute
        """
        time_indexed = messages.set_index('timestamp')
        time_indexed['year'] = time_indexed.index.year
        time_indexed['month'] = time_indexed.index.strftime("%b")
        time_indexed['hour'] = time_indexed.index.hour
        time_indexed['minute'] = time_indexed.index.minute
        time_indexed['weekday'] = time_indexed.index.strftime("%a")

        return time_indexed

    def yearly_graph(self, time_indexed):
        """
        generates an aggregated message count by year
        """
        yearly_df = time_indexed.groupby("year").count()
        return yearly_df.msg.to_dict()

    def hourly_graph(self, time_indexed):
        """
        generates an aggregated message count by hour
        """
        hourly_df = time_indexed.groupby("hour").count()
        hourly_df['hour_str'] = [datetime.strptime(str(hour), '%H').strftime("%I %p") for hour in hourly_df.index]
        return hourly_df.msg.to_dict()

    def monthly_graph(self, time_indexed):
        """
        generates an aggregated message count by month
        """
        monthly_df = time_indexed.groupby("month").count()
        monthly_df = monthly_df.reindex(
            ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
        return monthly_df.msg.to_dict()

    def minutely_graph(self, time_indexed):
        """
        generates an aggregated message count by minute
        """
        minutely_df = time_indexed.groupby("minute").count()
        return minutely_df.msg.to_dict()

    def daily_graph(self, time_indexed, top=15):
        """
        generates an aggregated message count by minute
        """
        daily_df = time_indexed.resample("D").count().sort_values("msg", ascending=False)
        daily_df = daily_df[:top]
        return {
            date.strftime("%d-%m-%Y"): mess_count for date, mess_count in daily_df.msg.to_dict().items()
        }

    def weekday_graph(self, time_indexed):
        """
        generates an aggregated message count by minute
        """
        weekday_df = time_indexed.groupby("weekday").count()
        weekday_df = weekday_df.reindex(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
        return weekday_df.msg.to_dict()

    def chat_counts(self, top=10, omit_first=True):
        """ 
        counts the number of chats each person is in and returns the top x people in the most chats
        """
        start = int(omit_first)
        counts = self.msg_df.groupby(["sender", "thread_path"]).size().reset_index().groupby(
            "sender").count().sort_values('thread_path', ascending=False)
        counts = counts[start:top]
        return counts.thread_path.to_dict()

    def word_counts(self, chat=None, length=1, top=10):
        """
        counts the word usage based on the passed in DataFrame `chat` and returns words that are longer than `length`
        """
        chat = self.msg_df if chat is None else chat
        # filter out multimedia
        messages = chat['msg'][pd.isnull(chat.sticker) & pd.isnull(chat.photos) & pd.isnull(chat.videos)]
        words = {'count': {}}
        for msg in messages:
            msg = str(msg).encode('latin1').decode('utf8')  # to get around encoding problems
            for word in msg.split(" "):
                word = word.lower()
                word = word.rstrip('?:!.,;')
                if word in words['count']:
                    words['count'][word] += 1
                else:
                    words['count'][word] = 1

        word_df = pd.DataFrame(words).sort_values("count", ascending=False)

        def len_filtered_wdf(length):
            mask = [len(word) >= length for word in word_df.index]
            return word_df[mask][:top]

        filtered_df = len_filtered_wdf(length)
        return filtered_df["count"].to_dict()
