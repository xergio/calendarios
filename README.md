Generador de calendarios de Comunidades Autónomas a partir 
de una fuente, inicialmente el BOE.

En la carpeta [Calendarios]() están en formato `.ics` para 
descargar.

# BOEs

- Festivos de 2024: https://www.boe.es/diario_boe/txt.php?id=BOE-A-2023-22014

# Development

Inicialización del proyecto:

```shell
$ python3 -m venv venv
$ source venv/bin/activate
venv $ pip install ics requests beautifulsoup4
venv $ pip freeze > requirements.txt
venv $ deactivate
```
