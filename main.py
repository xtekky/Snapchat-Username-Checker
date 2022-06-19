import random, requests, threading, sys, cursor


class Checker:
    def __init__(self, threads, length, proxyfile):
        
        cursor.hide()
        self.threads = threads
        self.length  = self.parse_length(length)
        
        self.proxies = open(proxyfile, 'r').read().splitlines()
        
        self.session = requests.Session()
    
    def start(self):
        while True:
            if threading.active_count() < self.threads:
                threading.Thread(target=self.check_username).start()
        
    def parse_length(self, length):
        return length - 2
    
    def get_username(self):
        
        l1 = random.choice('abcdefghijklmnopqrstuvwxyz')
        l2 = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz01234567890-_.', k=self.length))
        l3 = random.choice('abcdefghijklmnopqrstuvwxyz')
        
        username = f'{l1}{l2}{l3}'
        
        return username
    
    def get_xcrsf_token(self):
        req = self.session.get(
                url = "https://accounts.snapchat.com/accounts/signup?client_id=ads-api&referrer=https%253A%252F%252Fads.snapchat.com%252Fgetstarted&ignore_welcome_email=true",
                headers = {
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"
                },
            ) 
        
        token = req.cookies.get_dict()["xsrf_token"]
        
        return token

    def _print(self, arg):
        threading.Lock().acquire()
        sys.stdout.write(f'\r{arg}')
        sys.stdout.flush()
        threading.Lock().release()

    def check_username(self):
        proxy = random.choice(self.proxies)
        
        try:
            username = self.get_username()
            xcsrf_token = self.get_xcrsf_token()

            req = self.session.post(
                url = "https://accounts.snapchat.com/accounts/get_username_suggestions", 
                data = {
                    "requested_username": username, 
                    "xsrf_token": xcsrf_token
                },
                proxies = {
                    'http': f'http://{proxy}',
                    'https': f'http://{proxy}'
                }
                )   
            
            if req.json()["reference"]["status_code"] == 0:
                self._print(f'\r [ ✔ ] Available: {username}')
                with open('usernames.txt', 'a') as _:
                    _.write(f'{username}\n')
            else:
                self._print(f'\r [ x ] Unavailable: {username}')
        except Exception as e:
            
            pass


check = Checker(
    threads   = 3,
    length    = 3,
    proxyfile = './proxies.txt'
)

check.start()
