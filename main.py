import requests, random, threading, time, datetime, os


class Checker:
    def __init__(self, threads, length, webhook) -> None:
        self.threads = (threads,)
        self.length = length
        self.hook = webhook
        self.start = time.time()
        # proxies      = open('proxies.txt', 'r').read().splitlines()

        self.hits = 0
        self.fails = 0

    def username(self) -> str:
        """Returns generated legit username"""
        l1 = random.choice("abcdefghijklmnopqrstuvwxyz")
        l2 = "".join(
            random.choices(
                "abcdefghijklmnopqrstuvwxyz01234567890-_.", k=self.length - 2
            )
        )
        l3 = random.choice("abcdefghijklmnopqrstuvwxyz")

        username = f"{l1}{l2}{l3}"

        return username

    def webhook(self, username) -> None:
        """_summary_

        Args:
            username (_type_): _description_
        """
        data = {
            "content": "@here",
            "embeds": [
                {
                    "title": "CLAIMABLE",
                    "description": f"*Precision* : **{random.randint(98, 99)}%**\n*Username* : **{username}**\n*Date & Time* : **{str(datetime.datetime.now()).split('.')[0]}**\n",
                    "color": 5242880,
                    "image": {
                        "url": "https://cdn.discordapp.com/attachments/988228169117106236/991900970105712781/standard.gif"
                    },
                    "thumbnail": {
                        "url": "https://cdn.discordapp.com/attachments/988228169117106236/991902513391489024/final_size-snap_20210321235118_2.gif"
                    },
                }
            ],
            "attachments": [],
        }

        requests.post(url=self.hook, json=data)

    def worker(self) -> None:
        """
        Worker loop
        """

        while True:
            try:
                username = self.username()
                proxy = "m00nd4rk:m00nd4rk@geo.iproyal.com:12323"

                req = requests.post(
                    url="https://app.snapchat.com/loq/suggest_username_v3",
                    headers={
                        "User-Agent": "Snapchat/10.25.0.0 (Agile_Client_Error; Android 5.1.1#500181103#22; gzip)"
                    },
                    data={
                        "requested_username": username,
                        "x-niggers": "RE8gTk9UIERFQ09ERSA6IFpHbHpZMjl5WkM1blp5OXZibXh3SURzZ0tRPT0=",
                    },
                    proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"},
                )
                print(req.text)
                if "429 Too Many Requests" in req.text:
                    time.sleep(20)
                    continue
                elif "OK" in req.text:
                    self.hits += 1
                    with open("./usernames.txt", "r") as _:
                        _.write(username)
                    self.webhook(username)
                    continue
                else:
                    self.fails += 1
            except:
                continue

    def title(self) -> None:
        """_summary_
        Title loop threaded for stats
        """
        while True:
            speed = round((self.hits + self.fails) / (time.time() - self.start), 1)
            curr_time = str(
                datetime.timedelta(seconds=(time.time() - self.start))
            ).split(".")[0]

            os.system(
                f"title [Snapchat Checker] ^| Hits: {self.hits} ^| Fails: {self.fails} ^| Speed: {speed}/s ^| Elapsed: {curr_time}"
            )
            time.sleep(0.2)

    def main_thread(self):
        # threading.Thread(target=self.title).start()

        while True:
            if threading.active_count() < int(self.threads[0]) + 1:
                threading.Thread(target=self.worker).start()


if __name__ == "__main__":
    check = Checker(
        threads=500,
        length=4,  # username length
        webhook="",
    )
    check.main_thread()
