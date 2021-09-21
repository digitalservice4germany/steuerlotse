# Steuerlotse

🇬🇧 This is the code repository of the [_Steuerlotse_ ](https://steuerlotse-rente.de) by DigitalService4Germany.
You can use this code under the terms of the provided license.
The _Steuerlotse_ is available at: https://steuerlotse-rente.de

With the _Steuerlotse_, taxable pensioners can submit their tax returns online from the tax year 2020 onwards. 
The _Steuerlotse_ was specially developed for the tax return of pensioners without additional income.

As early as 2019, four federal states (Brandenburg, Bremen, Mecklenburg-Western Pomerania and Saxony) developed 
a simplified tax return in paper form for pensioners. Based on the paper form a 
[digital prototype](https://github.com/tech4germany/steuerlotse) was developed as part of the Tech4Germany Fellowship 
2020. The fellowship is organized by [DigitalService4Germany GmbH](https://digitalservice4germany.com).

🇩🇪 Dies ist das Quellcodearchiv des [_Steuerlotse_ ](https://steuerlotse-rente.de) vom DigitalService4Germany.
Du kannst den Code unter den Bedingungen der angegeben Lizenz nutzen.
Der _Steuerlotse_ ist verfügbar unter: https://steuerlotse-rente.de

Mit dem _Steuerlotsen_ können steuerpflichtige Rentner:innen und Pensionär:innen ab dem Veranlagungsjahr 2020 ihre 
Steuererklärung online einreichen. Der _Steuerlotse_ wurde extra für die Steuererklärung von Rentner:innen und 
Pensionär:innen ohne Zusatzeinkünfte entwickelt. 

Bereits 2019 haben vier Bundesländer (Brandenburg, Bremen, Mecklenburg-Vorpommern und Sachsen) eine vereinfachte 
Steuererklärung in Papierform für Rentner:innen entwickelt. Auf Basis des Papiervordrucks wurde im Rahmen des 
Tech4Germany Fellowships 2020, das von der [DigitalService4Germany GmbH](https://digitalservice4germany.com) 
organisiert wird, von vier Fellows in Kooperation mit dem BMF ein 
[digitaler Prototyp](https://github.com/tech4germany/steuerlotse) entwickelt.

## General remarks

🇬🇧
The _Steuerlotse_ is actively being further developed. We plan on releasing new features and updates based on user 
research in the future in this repository.

🇩🇪
Der _Steuerlotse_ wird aktiv weiterentwickelt. Wir planen, in Zukunft neue Funktionen und Updates basierend auf 
Benutzerforschung in diesem Repository zu veröffentlichen.

## Contributing

🇬🇧
Everyone is welcome to contribute the development of the _Steuerlotse_. You can contribute by opening pull request, 
providing documentation or answering questions or giving feedback. Please always follow the guidelines and our 
[Code of Conduct](CODE_OF_CONDUCT.md).

🇩🇪  
Jede:r ist herzlich eingeladen, die Entwicklung der _Steuerlotse_ mitzugestalten. Du kannst einen Beitrag leisten, 
indem du Pull-Requests eröffnest, die Dokumentation erweiterst, Fragen beantwortest oder Feedback gibst. 
Bitte befolge immer die Richtlinien und unseren [Verhaltenskodex](CODE_OF_CONDUCT_DE.md). 

### Contributing code
🇬🇧 
Open a pull request with your changes and it will be reviewed by someone from the team. When you submit a pull request, 
you declare that you have the right to license your contribution to the DigitalService4Germany and the community. 
By submitting the patch, you agree that your contributions are licensed under the MIT license.

Please make sure that your changes have been tested befor submitting a pull request.

🇩🇪  
Nach dem Erstellen eines Pull Requests wird dieser von einer Person aus dem Team überprüft. Wenn du einen Pull-Request 
einreichst, erklärst du dich damit einverstanden, deinen Beitrag an den DigitalService4Germany und die Community zu 
lizenzieren. Durch das Einreichen des Patches erklärst du dich damit einverstanden, dass deine Beiträge unter der 
MIT-Lizenz lizenziert sind.

Bitte stelle sicher, dass deine Änderungen getestet wurden, bevor du einen Pull-Request sendest.

## For Developers 👩‍💻 👨‍💻

### Overview
The two main components are the webapp and erica.

The webapp handles user input, renders html and connects to the PostgreSQL database.

Erica provides an internal API to connect via ERiC (ELSTER Rich Client) with the ELSTER APIs. Part of Erica is Pyeric, a Python wrapper for ERiC.

### Run directly

For developing, we suggest running both webapp and erica locally. See here for instructions:
- [webapp/README.md](webapp/README.md)
- [erica_app/README.md](erica_app/README.md)

### Run with docker-compose

Alternatively, you can start the application with `docker-compose up`.

Run database migrations and create test data:
```
docker-compose exec web pipenv run flask db upgrade
docker-compose exec web pipenv run flask populate-database
```

Visit the application by pointing your browser at http://localhost.

### Enviroments
We support four different environments with different configurations:
- Testing
- Development
- Staging
- Production

In the testing environment a mocked version of Erica and the hashing algorithm is used.
