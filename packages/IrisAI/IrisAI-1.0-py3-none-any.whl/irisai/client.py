
from requests import get, post
import json, sys


class excs:
    class ErrorRequest(Exception):
        def __init__(self, msg):
            super().__init__(msg)
            self.msg = msg

class api:
    class chat:
        class completions:
            def __init__(self, baseUrl, token):
                self.baseUrl = baseUrl,
                self.token = token
            def create(self,
                       *,
                       message: str,
                       model: str,
                       stream: bool = False,
                       temperature: float = 1.0,
                       maxtokens: int = 4096):
                resp = post(self.baseUrl[0]+"/api/chat/completions", 
                    json={
                        "message": message,
                        "model": model,
                        "temperature": temperature,
                        "max_tokens": maxtokens,
                        "stream": stream
                    },
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {self.token}"
                    },
                    stream=stream)
                if resp.status_code == 200:
                    if stream:
                        def gen(resp):
                            for chunk in resp.iter_content(chunk_size=1024, decode_unicode=True):
                                data = json.loads(chunk)
                                yield data["data"]["message"]
                                sys.stdout.flush()
                        return gen(resp)
                    else:
                        return resp.json()["data"]["message"]
                else:
                    raise excs.ErrorRequest(resp.json()["data"]["message"])

        
    class info:
        def __init__(self, baseUrl, token):
            self.baseUrl = baseUrl
            self.token = token
        def models(self):
            resp = get(self.baseUrl+"/api/models")
            return resp.json()
        def token(self):
            resp = get(self.baseUrl+"/api/token/info", headers={"Authorization": f"Bearer {self.token}"})
            return resp.json()
                


class IrisAI:
    def __init__(self, token: str, **kwrags):
        self.token = token
        print(kwrags)
        self.baseUrl = kwrags["baseUrl"] if "baseUrl" in kwrags else "https://irisai.tesnpe.ru"
        self.chat_completions = api.chat.completions(self.baseUrl, self.token)
        self.info = api.info(self.baseUrl, self.token)