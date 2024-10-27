import asyncio

import httpx

from eirStru import is_json


class SendEmailIntf:
    def __init__(self, host):
        self.host = host

    async def send_email(self, subject, body, recipient, files=None):
        if files is None:
            files = []
        url = f'http://{self.host}/send-email'
        headers = {
            'accept': 'application/json'
        }
        data = {
            'subject': subject,
            'body': body,
            'recipient': recipient,
            'sender': None}

        # files = [
        #     ('files', ('test.py', open('test.py', 'rb'))),
        #     ('files', ('utils.py', open('utils.py', 'rb')))
        # ]

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, data=data, files=files)
            if is_json(response.text):
                return response.json()



if __name__ == '__main__':
    send_email = SendEmailIntf('api.e-hhl.com:8002')
    asyncio.run(send_email.send_email('hi 18', 'test', 'wangwh@victop.com'))
