# Desafio Tecnico Monotributo

documentacion de [sheets-api](https://developers.google.com/sheets/api/quickstart/python) con python

## credentials.json
El archivo credentials.json proviente de las credenciales obtenidas desde google cloud

## sheets.json
El archivo sheets.json guarda la informacion de las hojas de google sheets. En el siguiente json de ejemplo habria que remplazar `<sheet_id>` por los ids de los respectivos archivos y luego tener una hoja llamada `Sheet1` donde en el rango `A2:B` tengamos los datos correspondientes
```json
{
    "expenses": {
        "spreadsheet_id": "<sheet_id>",
        "range_name": "Sheet1!A2:B"
    },
    "earnings": {
        "spreadsheet_id": "<sheet_id>",
        "range_name": "Sheet1!A2:B"
    }
}
```

## categories.json
El archivo categories.json contiene los rangos para cada categoria de monotributo segun los valores vigentes desde `01/07/2023` en la pagina de la [afip](https://www.afip.gob.ar/monotributo/categorias.asp). Es facil de modificar simplemente teniendo que cambiar el limite superior de acceso a una categoria
