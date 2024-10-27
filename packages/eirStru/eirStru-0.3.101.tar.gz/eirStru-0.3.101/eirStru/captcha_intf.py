import asyncio
import base64
from io import BytesIO

import httpx
from PIL import Image
from loguru import logger

from eirStru import is_json


class CaptchaIntf:

    def __init__(self, host):
        self.host = host

    async def b64captcha(self, b64):
        """
        b64验证码识别
        :param b64:
        :return:
        """
        url = f'{self.host}/b64captcha'
        params = {'b64': b64}
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(url, headers={'accept': 'application/json'}, data=params)
                logger.info(resp.text)
                r_json = resp.json()
                if r_json.get('code') == 1:
                    return r_json.get('data')
        except Exception as e:
            logger.error(e)

    async def bytes_captcha(self, byte_stream: BytesIO, file_name='captcha.jpg'):
        byte_stream.seek(0)
        url = f'{self.host}/captcha'
        headers = {
            'accept': 'application/json'
        }
        files = {'file': (file_name, byte_stream, 'image/png')}
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=headers, files=files)
                logger.info(response.text)
                r_json = is_json(response.text)
                if r_json.get('code') == 1:
                    return r_json.get('data')
        except Exception as e:
            logger.error(e)

    async def captcha(self, file_name):

        url = f'{self.host}/captcha'
        headers = {
            'accept': 'application/json'
        }
        files = {'file': (file_name, open(file_name, 'rb'), 'image/png')}
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=headers, files=files)
                logger.info(response.text)
                r_json = is_json(response.text)
                if r_json.get('code') == 1:
                    return r_json.get('data')
        except Exception as e:
            logger.error(e)


if __name__ == '__main__':
    eir_tools = CaptchaIntf('http://captcha.e-hhl.com:8001')

    # b64 验证码解析
    image_b64 = 'data:image/gif;base64,/9j/4AAQSkZJRgABAgAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAAkAG8DASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD03VBrDWc72UsMLpkoioXZwPc8AkdsH681Q8NXTX8Kz78sB5UiPdSMwAGS+CSMk7QAAMDPzHO2t2YSOxRCEcKWjc7iN2CPmAwCORxnnnpjNctM48OeJzcKGWwu22S5UhVbg5HqBnOR6sOoNcyfRHMrSi49TS1eR7rUNLtVQBGuhIrNuDEx7t4KkdPu4OTnPYYJ2jFvMbOzbo3LLsYqOhGCAeeD0PGcHGQMYWxZPE0BgEjFLWS7QTyP99yFwd2SgwOgHHpXQMSoyFLcgYGPXrzTe+hM9NCrcypZW00k7t5IUsXLHI46cdPw/nXF2UN+PE+mvPNi7lhL/vVdlQYbjDNnoM/e4J9q6LUZRf6gttsZ7O1dGuSuMM5IwpyQNq/ebr9M1iX17Z23jS3uluIvIWPmRPnAO1hzgnPYduMUo3WiNacdG+tjqI9QnYDNkZdyh1a2mR0ZT0ILFT+mPesmXUNT1m6ltrGKe2t4WMcsgKBy+emcnA91yfbtW1aNBd2sckbs2EUBixyOMg8k9Qc+/fNc5oeqQaVqWpWF9MqbrhpElY8Mc4OT+A/WhERWj01IprjUtFu447q5u5bKR9kh35YNjO1ZGAyMEcjGOQDkGujRDEFEF020SbmVnLkgjGCXJIA64BH3fcg8x4q1H+07T/RvMa0gk+aVIyyM54AzjjA3c9OQOSRXV6eIp7RLkjc9wqyuGYsA21RwCflHA4GBnJ6k03tcclZJ9TP1fUr2G7ttOtDELm5BO/bnYo74PU8H8qyNYguNNsxe2+sX7TRsu5ZZOCSem3t9DxVnxXYrbR2+pW8rxXET7VYEe5Axn8BgHrzxkjIv77V0ns5NZst8MB3kbANxI4JI4yCRx+HehLaxcFdJo7VC09kjXG9VkUF9rlCjd8EEHGff9KaYp4JFitrpwr5wJ4mmAx6MCCOv8RPtjFVdKvbeaETo7mGZtw3sQFOMEYJOOnIHGee+a0RGlvI0qRZDgAlV5ABJA9SMk/TJqdjF6MmZFZGRlBVgQVI4OetZ2oaRFqGjiy8uOHagEap92MgcAdOB06dM9M1olAzKxLfKcgA4HQjn169/ao1Fta4RRHFxgBQBxz/if1pehKbWxzfhKG9L3kt4jLLGi28TyL0C5yB6gHHT0rpIXMzyM0OwI5SNjnLDjJwQMc5HvgHuKz31nS9LjigmvmIxhGbdISOwLAHJx6nPc560z/hKdFzn7b/5Df8AwqmuboVJOT5rCT+GdNdp5/sgnuHZ5B5szKpYknBx0GeOh49axbiwt7LxvbxQt5MckLMNqLiMlWHy8e2fmzz7YA6HTNRjuzFFarALZIcHa20o6nbsCgFcD1DHqvUEGrrPG7REiX/WFVwrAZAYHd7cHBPB4xzindopTkmQCB0ACMPPRAXKx7Vc+3bqDxk4/Wq8lrYMttDd2EIWD5YhsGxQFIwB0xjt9PTi7H5lupErb03EhlGNozwCMnoMc/Xp0qtqGljUY0UXc0CK24CBtoYHGc+p64Pv37xa2xNzL1pIrpY9Gs1jWSd1yIW4SIYJZgMAc9B3/StdYEkiRo0iljKjY8bY3Ljg8cdKgg8O6ZboRFbbd20nLFslTkHknnPf/AVJNNc24bDFlXu6jgepOfx/D607qxTatZHOavd+VrWkSytILQHzB9oRhg+4OCMcfT0PSti81vTjZTpNNHLKMqsSDJYkZUDrngjn+XSq897Z3titvfvHOgIBmABxxwTjp9R69MVUsDpen3JMCIS0gyzId0Yxj5crnrzkkdT7Cn01RbSfyLeh6OItGWyvRLHK7NKNkjIRuXGMjHOPyPPUA1fWX7He+Wzl/LjJCKxyAx4JXOOqkAkdjg9c2NvnFcSAqwJVyCSx46c8YwcjHPXjBpsGI0FvcRwpHGNqAdAAeOwHTH06c0nrqRe+rIdak/s3Rrm5t1wyyJJt3MBu3r6EcHqR0OTnOTnD0FpvEhuBqlzLLFBtxEpCK+c/e2gZxtBFFFXH4WwgvdbOthght4/LgiSJOu1FCj8hUlFFZmZiano9nbwS6jZx/ZLu3hZlkt8JkAbtpHQgkDPHOBWT4U1q71HU5bO6WF0ijNwjiMKwYtg9OO57Z5PNFFabxuabw1OlvbuS2u9OiQKVubgxPkcgCKR+PfKD8M02dFtNphVVRmYmPaNpb727Hrnn8aKKyJSKniTU7jS9LSa22CR5BHlhnGVJyPfiqHh2NtahbUNQmkmkjkMapkKnAByQoGTyRz2oorVfCy18FzpkjSJAkaKijsowKV0WRGR1DIwwysMgj0NFFZmRz/iGyjstMmvrN5LWVAqkQnargkLyPYE4x0Jqv4Y1GfUnuoZz/qY4pFcMxYly4OdxIx8g4+tFFafZua2vG5//2Q=='
    asyncio.run(eir_tools.b64captcha(image_b64))

    # 文件名 验证码解析
    image_data = image_b64.split(",")[1]
    image_bytes = base64.b64decode(image_data)
    image = Image.open(BytesIO(image_bytes))
    image.save("ocr.png", "PNG")
    asyncio.run(eir_tools.captcha('ocr.png'))

    image = Image.open('ocr.png')
    byte_stream = BytesIO()
    image.save(byte_stream, format='PNG')
    byte_stream.seek(0)
    asyncio.run(eir_tools.bytes_captcha(byte_stream))
