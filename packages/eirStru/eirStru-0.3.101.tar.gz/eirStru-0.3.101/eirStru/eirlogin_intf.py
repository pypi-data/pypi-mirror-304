import httpx

from eirStru import *


class LoginIntf:
    def __init__(self, host):
        self.host = host

    async def check_account_info(self, params: AccountInfo) -> ResponseData:
        """
        检查账号
        """
        url = f'{self.host}/check_account_info'
        headers = {
            'accept': 'application/json'
        }

        data = json.loads(params.model_dump_json())

        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(url, headers=headers, json=data)
                r_json = resp.json()
                if r_json.get('data'):
                    r_json['data'] = AccountInfo(**r_json['data'])
                return ResponseData(**r_json)
        except Exception as e:
            return ResponseData(code=RespType.task_exception, msg=f'{e}')

    async def login(self, params: AccountInfo) -> ResponseData:
        """
        检查账号
        """

        url = f"{self.host}/login"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        data = json.loads(params.model_dump_json())
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=headers, json=data)
                return response.json()
        except Exception as e:
            return ResponseData(code=RespType.task_exception, msg=f'{e}')

    async def get_session(self, carrier_id, action: ActionType, account: str = None, bookingagent_id: str = None,
                          sub_code: str = None) -> ResponseData:
        url = f'{self.host}/get_session'
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        params = ParamsGetSession()
        params.carrier_id = carrier_id
        params.action = action
        params.account = account
        params.bookingagent_id = bookingagent_id
        params.sub_code = sub_code

        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(url, headers=headers, json=json.loads(params.model_dump_json()))
                r_json = resp.json()
                if r_json.get('data'):
                    r_json['data'] = SessionData(**r_json['data'])
                return ResponseData(**r_json)
        except Exception as e:
            return ResponseData(code=RespType.task_exception, msg=f'{e}')

    async def return_session(self, resp_type: RespType, session_data: SessionData) -> ResponseData:
        url = f'{self.host}/return_session'
        headers = {
            'accept': 'application/json'
        }
        session_data.last_access_resp_type = resp_type
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(url, headers=headers, json=json.loads(session_data.model_dump_json()))
                r_json = resp.json()
                return ResponseData(**r_json)
        except Exception as e:
            return ResponseData(code=RespType.task_exception, msg=f'{e}')

    async def get_session_summary(self, carrier_id) -> ResponseData:

        url = f"{self.host}/get_session_summary"
        params = {
            'carrier_id': carrier_id
        }
        headers = {
            "accept": "application/json"
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=headers, params=params)
                logger.info(response.text)
                r_json = response.json()
                return ResponseData(**r_json)
        except Exception as e:
            return ResponseData(code=RespType.task_exception, msg=f'{e}')
