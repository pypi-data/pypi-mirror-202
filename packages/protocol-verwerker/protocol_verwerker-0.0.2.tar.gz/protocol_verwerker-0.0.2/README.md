# Sequentietabel Generator

## Installatie
Installeer het programma met het volgende commando's (copy-paste in de terminal):
```
# check voor updates en update programma's indien mogelijk
sudo apt update && sudo apt upgrade -y
# installeer python
sudo apt install python3 python3-pip
pip install 
```

## Gebruik
1. Download het bestand met je protocol (als Excel- of CSV-bestand) toe aan Linux-Bestanden in de bestanden-app op je chromebook.
    - Als je dit bestand in een mapje binnen Linux-Bestanden zet, voer eerst het commando `cd <map-naam>` uit voordat je verder gaat met stap 2.
2. Voer het volgende commando uit: `sequentietabel-generator`
3. Vervolgens krijg je een paar opties deze bestaan uit:
    - Excel (xlxs) of CSV (csv) bestand? (xlxs/csv)
        - Kies het bestand type dat jij gebruikt door xlsx of csv in te typen en vervolgens op enter te drukken.
    - Naam van het bestaande bestand
        - Naam van het bestand van je protocol, zonder extensies (bijv. protocol, maar **NIET** protocol.csv).
    - Heeft het bestand headers?
        - Heeft je protocol headers, zoals tijdseenheden, die niet in de sequentietabel thuishoren. Zie deze [spreadsheet](https://docs.google.com/spreadsheets/d/1igtuUOigLqRWvZau0G3IBDdJu1WwTdV-Qrl9ERvkScE/edit?usp=sharing) met de voorbeelden van een protocol. Alleen deze vormen worden correct verwerkt door het programma. ('ja', 'yes', 'j' of 'y' wordt gezien als een ja (dus wel headers), enige andere input wordt gezien als een nee (dus geen headers)).
    - Naam van het nieuwe bestand
        - Zonder extensies (bijv. resultaat, maar **NIET** resultaat.csv).
4. Hierna wordt het bestand gegenereerd en kan het geïmporteerd worden in een google spreadsheet.
