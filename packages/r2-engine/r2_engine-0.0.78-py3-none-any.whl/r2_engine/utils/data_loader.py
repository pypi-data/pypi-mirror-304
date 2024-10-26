import pandas as pd
from sqlalchemy.engine import Engine
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from typing import Optional

def load_data_to_sqlite(
    engine: Engine,
    google_sheet_url: Optional[str] = None,
    excel_file_path: Optional[str] = None
):
    if google_sheet_url:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_url(google_sheet_url).sheet1
        data = sheet.get_all_records()
        df = pd.DataFrame(data)
    elif excel_file_path:
        df = pd.read_excel(excel_file_path)
    else:
        raise ValueError("Debe proporcionar un google_sheet_url o un excel_file_path.")

    df.to_sql('data_table', con=engine, if_exists='replace', index=False)
