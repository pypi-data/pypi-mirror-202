import pandas as pd
import os

# Function to read CSV file and generate sequence table
def generate_frequencetable():
    # Open CSV file
    csv_file_pathGekozen = False
    while csv_file_pathGekozen == False:
        csv_file_pathType = (input('Excel (xlxs) of CSV (csv) bestand? (xlxs/csv): ')).lower()
        if(csv_file_pathType == "excel" or csv_file_pathType == "xlxs"):
            csv_file_path = input('Naam van het bestaande bestand (Excel-bestand, zonder .xlxs): ') + '.xlsx'
        elif(csv_file_pathType == "csv"):
            csv_file_path = input('Naam van het bestaande bestand (csv-bestand, zonder .csv): ') + '.csv'
        else:
            print('Dat is geen geldig bestandstype, probeer het opnieuw.')
            continue
        if(os.path.isfile(csv_file_path)):
            break
        else:
            print("bestand bestaat niet, probeer het opnieuw.")
    
    
    headerPrompt = (input('Heeft het bestand headers? (J(a), N(ee)): ')).lower()
    if(headerPrompt == "ja" or headerPrompt == "j" or headerPrompt == "y" or headerPrompt == "yes"):
        headers = True
    else:
        headers = False
    
    cijfer = False
    while cijfer == False:
        minuteInterval = input('Welke interval moet de frequentietabel hebben? (in minuten, cijfer: bijvoorbeeld 5): ')
        if(minuteInterval.isdigit()):
            minuteInterval = int(minuteInterval)
            cijfer = True
        else:
            print('Ongeldige input, probeer het opnieuw.')
    
    if(csv_file_pathType == "csv"):
        if(headers):
            df = pd.read_csv(csv_file_path)
            first_column = df.columns[0]
            df = df.drop([first_column], axis=1)
        else:
            df = pd.read_csv(csv_file_path, header=None)
    else:
        if(headers):
            df = pd.read_excel(csv_file_path)
            first_column = df.columns[0]
            df = df.drop([first_column], axis=1)
        else:
            df = pd.read_excel(csv_file_path, header=None)
    
    df = df.to_numpy()

    elements = []
    for row in df:
        for i in row:
            i = (i.lower()).strip()
            try:
                elements.index(i)
            except ValueError:
                elements.append(i)

    gedragBlueprintTable = {}
    tabel = {}

    for element in elements:
        gedragBlueprintTable[element] = 0

    gedrag = []
    for x in range(0, len(df),minuteInterval):
        gedrag = df[x:x+minuteInterval]
        blueprint = {}
        blueprint = gedragBlueprintTable.copy()
        for i in gedrag:
            for j in i:
                j = (str(j).lower()).strip()
                blueprint[j] = blueprint[j] + 1
        tabel.update({f'{x+1}-{x+minuteInterval}' : blueprint})
    
    if((len(df) % minuteInterval) != 0):
        for x in range(minuteInterval * (len(df) // minuteInterval), len(df), len(df) % minuteInterval):
            gedrag = df[x:(x + (len(df) % minuteInterval))]
            blueprint = {}
            blueprint = gedragBlueprintTable.copy()
            for i in gedrag:
                for j in i:
                    j = (str(j).lower()).strip()
                    blueprint[j] = blueprint[j] + 1
            tabel.update({f'{x+1}-{x + (len(df) % minuteInterval)}' : blueprint})

    path = input("Naam nieuwe bestand: ") + '.csv'
    
    csv = pd.DataFrame.from_dict(tabel, orient='index')
    
    csv.to_csv(path)
    
    print("Frequentietabel gegenereerd!")