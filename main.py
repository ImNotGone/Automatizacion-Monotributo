from __future__ import print_function

import os.path
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# no se bien como funciona esto pero es facil de modificar
def get_category(balance):
    if balance < 1000000:
        return "A"
    if balance < 1486000:
        return "B"
    if balance < 2081000:
        return "C"
    if balance < 2584000:
        return "D"
    if balance < 3043000:
        return "E"
    if balance < 3803043:
        return "F"
    if balance < 4563652:
        return "G"
    if balance < 5650236:
        return "H"
    if balance < 6323918:
        return "I"
    if balance < 7247514:
        return "J"
    return "K"

def get_data(creds, spreadsheet_info):
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

def main():
    if not os.path.exists('sheets.json'):
        print("sheets.json not found!")
        exit(1)

    sheets = None
    with open('sheets.json') as json_file:
        sheets = json.load(json_file)

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
    values_expenses = get_data(creds, sheets['expenses'])
    if not values_expenses:
        print("No data for expenses found!")
        return

    # obtengo los ingresos para cada cliente
    values_earnings = get_data(creds, sheets['earnings'])
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
            clients_balance[client_id] = +earning

    for client_id, balance in clients_balance.items():
        if(balance < 0):
            # TODO: ALERT!
            pass
        # calculo la categoria del monotributo
        category = get_category(balance)
        # la agrego al diccionario
        clients_balance[client_id] = (balance, category)
        print(client_id, clients_balance[client_id])

if __name__ == '__main__':
    main()
