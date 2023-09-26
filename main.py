from __future__ import print_function

import os.path
import json
import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_category(balance, categories):
    # si cae dentro del rango esperado retorno esa categoria
    for i in range(len(categories)):
        if balance < categories[i]["threshhold"]:
            return categories[i]["category"]
    # si me excedi de todas, retorno la ultima
    return categories[-1]["category"]

def get_sheet_data(creds, spreadsheet_info):
    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()

        result = sheet.values().get(spreadsheetId=spreadsheet_info['spreadsheet_id'],
                                    range=spreadsheet_info['range_name']).execute()
        values = result.get('values', [])

        return values

    except HttpError as err:
        print(err)

# snip from (https://developers.google.com/sheets/api/guides/create#python)
def create_sheet(creds, title):
    """
    Creates the Sheet the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
        """
    try:
        service = build('sheets', 'v4', credentials=creds)
        spreadsheet = {
            'properties': {
                'title': title
            },
            'sheets': [
                {
                    'properties': {
                        'title': 'Sheet1'
                    }
                }
            ]
        }
        spreadsheet = service.spreadsheets().create(body=spreadsheet,
                                                    fields='spreadsheetId').execute()
        return spreadsheet.get('spreadsheetId')
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error

def get_json_file(file_name):
    if not os.path.exists(file_name):
        print(f"{file_name} not found!")
        exit(1)

    with open(file_name, 'r') as json_file:
        info = json.load(json_file)

    return info

def main():
    sheets = get_json_file('sheets.json')
    categories = get_json_file('categories.json')

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # obtengo los gastos para cada cliente
    values_expenses = get_sheet_data(creds, sheets['expenses'])
    if not values_expenses:
        print("No data for expenses found!")
        return

    # obtengo los ingresos para cada cliente
    values_earnings = get_sheet_data(creds, sheets['earnings'])
    if not values_earnings:
        print("No data for earnings found!")
        return

    # inicio el diccionario para guardar los balances de los clientes
    clients_balance = {}

    # resto los gastos
    for row in values_expenses:
        try:
            client_id, expense = row[0], float(row[1])
        except ValueError as e:
            print(f"Error converting {row[1]} to float: {e}")
            exit(2)
        if client_id in clients_balance:
            clients_balance[client_id] -= expense
        else:
            clients_balance[client_id] = -expense

    # sumo los ingresos
    for row in values_earnings:
        try:
            client_id, earning = row[0], float(row[1])
        except ValueError as e:
            print(f"Error converting {row[1]} to float: {e}")
            exit(2)
        if client_id in clients_balance:
            clients_balance[client_id] += earning
        else:
            clients_balance[client_id] = earning

    output_rows = [["CLIENT_ID", "CATEGORY"]]
    for client_id, balance in clients_balance.items():
        if(balance < 0):
            # TODO: ALERT!
            pass
        # calculo la categoria del monotributo
        category = get_category(balance, categories)

        # la agrego al diccionario
        clients_balance[client_id] = (balance, category)
        output_rows += [[client_id, category]]

    # Creo la Sheet para cargar los datos de cada cliente y su cat de monotributo
    formatted_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    spreadsheet_id = create_sheet(creds, sheets['category']['sheet_name'] + formatted_datetime)

    body = {
        'values': output_rows
    }

    range_name = f"Sheet1!A1:B{len(output_rows)}"

    service = build('sheets', 'v4', credentials=creds)
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption="RAW",
        body=body
    ).execute()



if __name__ == '__main__':
    main()
