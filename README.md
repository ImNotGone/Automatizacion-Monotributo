# Automatización Monotributo

## Tabla de contenidos

* [Objetivo](#objetivo)
* [Requerimientos](#requerimientos)
* [Implementación](#implementación)
* [Documentación](#documentación)
* [Uso de archivos de configuración](#uso-de-archivos-de-configuración)
* [Preguntas a desarrollar](#preguntas-a-desarrollar)

## Objetivo
- Validación de Gastos e Ingresos: A partir de un Google Sheets con gastos por cliente y otro con ingresos por cliente, desarrollar una validación mediante código Python que verifique que los gastos no son superiores a los ingresos. En caso contrario, enviar un email de alerta.
- Categorización de Monotributo: Como resultado del análisis anterior, publicar un archivo en Google Sheets con las categorizaciones de monotributo correspondientes a cada cliente, asumiendo que son monotributistas.

## Requerimientos
 * Python 3.10.7 o posterior
 * pip y las siguientes dependencias:
    1. google-api-python-client
    2. google-auth-httplib2
    3. google-auth-oauthlib
 * Un proyecto de Google Cloud
 * Una Cuenta de Google

## Implementación

Se utilizó parte del código presente en la documentación de [sheets-api](https://developers.google.com/sheets/api/guides/concepts) con Python

### Supuestos
Para la implementación se asumió que las columnas A y B contenían la información de client_id y gastos respectivamente en el caso del archivo de gastos. De igual forma, se asumió que las columnas A y B contenían la información de client_id e ingresos respectivamente para el caso del archivo de ingresos.
Por último como salida se asumió como suficiente que en la columna A estén los client_id y en la columna B la categoría de monotributo.

## Documentación 

### Proceso y decisiones tomadas
Comencé creando un proyecto en Google Cloud, el cual configure para utilizar la api de Sheets y del que obtuve las credenciales presentes en el archivo de configuración `credentials.json`. Continué leyendo la documentación oficial de la api de Sheets y su uso en Python modificando el código acorde a mis necesidades. Incrementalmente, fui probando que las cosas funcionaran correctamente. Me crucé con mi primer error debido a que en mi `range_name` estaba utilizando la hoja `Sheet1` y al crear los Sheets de prueba en mi cuenta de Google los mismos tenían como primera hoja `Hoja 1`. Una vez lo resolví fui probando que los datos de los csv fuesen importados correctamente, validando que pudiese pasarlos a float e inicialmente cargando únicamente en un diccionario como key el id del cliente y como value su balance. Como ya estaba leyendo la documentación de la api de Sheets deje de lado la alerta por un momento para pasar a implementar la creación del csv de salida. Otra vez me crucé con que el default al crear el archivo era `Hoja 1`, pero simplemente cambiando la configuración en el body de la request de creación pude setearlo en `Sheet1`. Pase a buscar como se categorizaba el monotributo en Argentina, lo configure de forma simple inicialmente para poder probarlo y luego busque los datos más actuales en la página de la AFIP. Erróneamente asumí que el Monotributo se categorizaba a partir del balance. Cosa que al final corregí, calculándolo a partir de los ingresos únicamente. Configurar la alerta por mail fue sorprendentemente fácil, basto con buscar como enviar mails por SMTP en Python para encontrar la documentación adecuada. Al implementar el envío del email, decidí crear una clase para contener la información de los clientes y poder utilizar el `__str__` tanto en el cuerpo como en el asunto del correo. Además, cree funciones para agregar ingresos y gastos que luego utilice para simplificar código repetido del main. Y aprovechando la clase creada, pase a utilizar el diccionario con el objeto de cliente directamente como value. El último freno que me encontré fue la autorización a la hora de mandar el email, para la cual tuve que crear un app-token que ingrese como contraseña en el archivo de configuración del SMTP.

## Uso de archivos de configuración

### Credenciales

#### credentials/credentials.json
El archivo credentials.json proviene de las credenciales obtenidas desde el proyecto de Google Cloud

#### credentials/email.json
Configuración de ejemplo en caso de uso de Gmail, donde smtp_password tiene que ser una [app-password](https://support.google.com/accounts/answer/185833?hl=en).
```json
{
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "smtp_username": "your_email@gmail.com",
    "smtp_password": "your_email_password"
}
```

### Configuración general
#### email_config.json
alert_email será el email que reciba las alertas correspondientes cuando el balance de un cliente es < 0
```json
{
    "alert_email": "recipient_email@example.com",
}
```

#### sheets.json
El archivo sheets.json guarda la información de las hojas de Google Sheets. En el siguiente JSON de ejemplo habría que remplazar `<sheet_id>` por los ids de los respectivos archivos y luego tener una hoja llamada `Sheet1` donde en el rango `A2:B` tengamos los datos correspondientes.
`<output-sheet-name>` se refiere a al nombre del Google Sheets que se va a crear como consecuencia de correr el código. Al final del nombre provisto se concatena tanto la fecha como la hora en la que se generó para evitar colisiones.
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

#### categories.json
El archivo categories.json contiene los rangos para cada categoría de monotributo según los valores vigentes desde `01/07/2023` en la página de la [AFIP](https://www.afip.gob.ar/monotributo/categorias.asp). Es fácil de modificar simplemente teniendo que cambiar el límite superior de acceso a una categoría

## Preguntas a desarrollar

- ¿Cómo mejorarías este sistema si tuvieses una semana más para trabajar en él?
    - Revisaría mejor el código para pulirlo lo más posible. Verificando si hay espacio para mejoras de eficiencia, implementando testeos, y revisando nuevamente los mensajes de error y las excepciones posibles.
- ¿Dónde harías deploy de esta solución y cómo automatizarías su ejecución cada mes?
    - En Google Cloud se presentan varias opciones, podría armar un contenedor para la aplicación y deployarlo en Google Cloud Run. Luego mediante una rutina, también en Google Cloud puedo hacer una request a mi Cloud Run Service en el intervalo deseado