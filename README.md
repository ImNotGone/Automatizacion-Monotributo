# Desafio Tecnico Monotributo

Se utilizo parte del codigo presente en la documentacion de [sheets-api](https://developers.google.com/sheets/api/quickstart/python) con python

## Credentials

### credentials/credentials.json
El archivo credentials.json proviente de las credenciales obtenidas desde google cloud

### credentials/email.json
Configuracion de ejemplo en caso de uso de gmail
smtp_password tiene que ser una [app-password](https://support.google.com/accounts/answer/185833?hl=en), por lo menos usando gmail
```json
{
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "smtp_username": "your_email@gmail.com",
    "smtp_password": "your_email_password"
}
```

## General configuration
### email_config.json
alert_email sera el email que reciba las alertas correspondientes cuando el balance de un cliente es < 0
```json
{
    "alert_email": "recipient_email@example.com",
}
```

### sheets.json
El archivo sheets.json guarda la informacion de las hojas de google sheets. En el siguiente json de ejemplo habria que remplazar `<sheet_id>` por los ids de los respectivos archivos y luego tener una hoja llamada `Sheet1` donde en el rango `A2:B` tengamos los datos correspondientes.
`<output-sheet-name>` se refiere a al nombre del google sheets que se va a crear como consecuencia de correr el codigo. Al final de el nombre provisto se concatena tanto la fecha como la hora en la que se genero para evitar colisiones.
```json
{
    "expenses": {
        "spreadsheet_id": "<sheet_id>",
        "range_name": "Sheet1!A2:B"
    },
    "earnings": {
        "spreadsheet_id": "<sheet_id>",
        "range_name": "Sheet1!A2:B"
    },
    "category": {
        "sheet_name": "<output-sheet-name>"
    }
}
```

### categories.json
El archivo categories.json contiene los rangos para cada categoria de monotributo segun los valores vigentes desde `01/07/2023` en la pagina de la [afip](https://www.afip.gob.ar/monotributo/categorias.asp). Es facil de modificar simplemente teniendo que cambiar el limite superior de acceso a una categoria
