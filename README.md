
# Quick.Share

**Corso**: Tecnologie Web <br/>
**Autori**: Mattia Lazzarini, Andrea Grassi <br/>

Questo modulo contiene la parte Back-end del progetto


## Indice:

 - Tecnologie usate e versioni testate
 - Deployment del Back-end
 
### 1. Tecnologie e versioni utilizzate

Pre-requisiti:
- **Python**: 3.8.10
- **Pip**: 20.0.2
- **Pipenv**: 2023.4.20

Segue una lista delle librerie:
```
django = "==4.2.2"
djangorestframework = "==3.14.0"
drf-extra-fields = "==3.5.0"
djangorestframework-simplejwt = "==5.2.2"
django-cors-headers = "==4.1.0"
psycopg2 = "==2.9.6"
django-rest-swagger = "==2.2.0"
```
Per evitare problematiche inerenti a possibili conflitti con versioni diverse, il progetto è stato inserito in un Virtual Environment.

Per abilitare l'ambiente virtuale:
 - Assicurarsi di essere nella directory principale ``projectenv``
 - Per abilitare il VirtualEnv, usare il comando:
```
 pipenv shell
```

### 2. Deployment del Back-end

1. Entrare nella cartella contenente i file del progetto:
```
 cd QuickShare_Backend
```

2. Avviare il server:
```
python3 manage.py runserver
```

3. Se tutto è andato a buon fine dovrebbe comparire il seguente messaggio:
```
    Watching for file changes with StatReloader
    Performing system checks...

    System check identified no issues (0 silenced).
    June 27, 2023 - 21:17:47
    Django version 4.2.2, using settings 'quickshare.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.
```
