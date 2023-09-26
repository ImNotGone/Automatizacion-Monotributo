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

def main():
    if not os.path.exists('sheets.json'):
        print("sheets.json not found!")
        exit(1)

    data = None
    with open('sheets.json') as json_file:
        data = json.load(json_file)

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

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()

        result_expenses = sheet.values().get(spreadsheetId=data['expenses']['spreadsheet_id'],
                                    range=data['expenses']['range_name']).execute()
        values_expenses = result_expenses.get('values', [])

        if not values_expenses:
            print('No data for expenses found.')
            return

        print('CLIENT_ID, EXPENSES')
        for row in values_expenses:
            # Imprimo el client_id en conjunto con los gastos
            print(f"{row[0]}, {row[1]}")

        result_earnings = sheet.values().get(spreadsheetId=data['earnings']['spreadsheet_id'],
                                    range=data['earnings']['range_name']).execute()
        values_earnings = result_earnings.get('values', [])

        print('CLIENT_ID, EARNINGS')
        for row in values_earnings:
            # Imprimo el client_id en conjunto con los ingresos
            print(f"{row[0]}, {row[1]}")

        if not values_earnings:
            print('No data for earnings found.')
            return

    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()
