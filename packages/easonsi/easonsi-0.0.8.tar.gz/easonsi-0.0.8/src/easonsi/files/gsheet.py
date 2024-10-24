""" 
gsheet-pandas: https://github.com/iakov-kaiumov/gsheet-pandas
Cloud页面: https://console.cloud.google.com/welcome?project=loyal-bit-422811-q3
另见官方文档: https://developers.google.com/sheets/api/quickstart/python?hl=zh-cn ⭐️
sheet: https://docs.google.com/spreadsheets/u/0/
doc: https://docs.google.com/document/u/0/

NOTE: 需要在cloud中设置和下载证书, 但是token有时效会过期! 需要按照下面main中的方法来更新token

DEBUG: 
1. Access blocked: Eason has not completed the Google verification process
    注意需要将自己添加到测试用户中 https://stackoverflow.com/questions/75454425/access-blocked-project-has-not-completed-the-google-verification-process
"""

from pathlib import Path
# import gsheet_pandas
import pandas as pd
import easonsi.files.google_sheet.connection as gsheet_pandas

secret_path = Path('/apdcephfs/private_easonsshi/easonsshi_base/config/google').resolve()
credentials_dir = secret_path / 'credentials.json'
token_dir = secret_path / 'token.json'
gsheet_pandas.setup(credentials_dir, token_dir)     # 注入 pandas.DataFrame.to_gsheet 方法
drive_connection = gsheet_pandas.DriveConnection(credentials_dir, token_dir)


class GSheet:
    """ 
    Usage:
        gsheet = GSheet()
        gsheet.to_gsheet(df)
    """
    spreadsheet_id = "1p36xAuhiv9siLo7Lw7bFGk9U33rBBKZOKUetYcLQQt4"
    sheet_name = "Sheet1"
    
    def __init__(self, spreadsheet_id=None, sheet_name=None):
        if spreadsheet_id: self.spreadsheet_id = spreadsheet_id
        if sheet_name: self.sheet_name = sheet_name

    @property
    def url(self):
        return f"https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}/edit#gid=0"

    def to_gsheet(self, df:pd.DataFrame, sheet_name=None, spreadsheet_id=None, drop_columns=False):
        """ 将pandas.DataFrame写入Google Sheet, 默认保存到 https://docs.google.com/spreadsheets/d/1p36xAuhiv9siLo7Lw7bFGk9U33rBBKZOKUetYcLQQt4/ """
        spreadsheet_id = spreadsheet_id or self.spreadsheet_id
        sheet_name = sheet_name or self.sheet_name
        # 若没有, 新建sheet! 
        drive_connection.create_sheet(spreadsheet_id, sheet_name)
        df.to_gsheet(spreadsheet_id, sheet_name=sheet_name, drop_columns=drop_columns)
        # range_name='!A1:C100' # Range in Sheets; Optional
        print(f"Saved to {sheet_name} in {self.url}")

    def from_gsheet(self, spreadsheet_id=None, sheet_name=None) -> pd.DataFrame:
        """ 从Google Sheet读取数据 """
        spreadsheet_id = spreadsheet_id or self.spreadsheet_id
        sheet_name = sheet_name or self.sheet_name
        return pd.from_gsheet(spreadsheet_id, sheet_name=sheet_name)



def local_file_to_gsheet(fn, sheet_name="tmp"):
    gs = GSheet()
    df = pd.read_csv(fn)
    gs.to_gsheet(df, sheet_name=sheet_name)
    print(f"Saved to {sheet_name}")


if __name__ == '__main__':
    # fn = "/work/aval/ref/FastChat/fastchat/llm_judge/data/mt_bench_zh/model_judgment/wizardLM-8x22B_pair_results.csv"
    # local_file_to_gsheet(fn, "mt_bench_zh-wizardLM-8x22B_pair")
    
    """ 
    更新token, 见 https://developers.google.com/sheets/api/quickstart/python?hl=zh-cn
    权限列表: https://developers.google.com/identity/protocols/oauth2/scopes?hl=zh-cn
    """
    import os
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError

    # If modifying these scopes, delete the file token.json.
    # SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_dir):
        creds = Credentials.from_authorized_user_file(token_dir, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        # if creds and creds.expired and creds.refresh_token:
        if creds and creds.expired and False:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_dir, SCOPES
            )
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(token_dir, "w") as token:
                token.write(creds.to_json())