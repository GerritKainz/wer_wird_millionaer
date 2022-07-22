import csv, json
from time import sleep

with open('fragen_antworten2.json', 'w') as f:
    data = {
    "telephone": ["Ich glaube, es ist Antwort ", "Ich bin mir sicher, es ist ", "Ich meine zu wissen, es sei "],
    "1": [],
    "2": [],
    "3": [],
    "4": [],
    "5": [],
    "6": [],
    "7": [],
    "8": [],
    "9": [],
    "10": [],
    "11": [],
    "12": [],
    "13": [],
    "14": [],
    "15": []
}
    json.dump(data, f, indent=1)

with open('fragen5.csv', newline='\n') as csvfile:
    reader = csv.reader(csvfile, delimiter='*')
    for i, row in enumerate(reader):
        if i > 0: #don't convert first line
            print(i)#, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            if   str(row[6]) == 'A': j = 2
            elif str(row[6]) == 'B': j = 3
            elif str(row[6]) == 'C': j = 4
            elif str(row[6]) == 'D': j = 5
            else: sleep(10)
            with open('fragen_antworten2.json', 'w') as f:
                data[f"{row[0]}"].append([f"{row[1]}", f"{row[2]}", f"{row[3]}", f"{row[4]}", f"{row[5]}", f"{row[j]}"])
                json.dump(data, f, indent=-1)
print('\n\nDone!')



# {
#     "1": [],
#     "2": [],
#     "3": [],
#     "4": [],
#     "5": [],
#     "6": [],
#     "7": [],
#     "8": [],
#     "9": [],
#     "10": [],
#     "11": [],
#     "12": [],
#     "13": [],
#     "14": [],
#     "15": [],
#     "telephone": ["Ich glaube, es ist Antwort ", "Ich bin mir sicher, es ist ", "Ich meine zu wissen, es sei "]
# }