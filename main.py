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

    for client, balance in clients_balance.items():
        if(balance < 0):
            # TODO: ALERT!
            pass
        print(client, balance)

if __name__ == '__main__':
    main()
