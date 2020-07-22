# make an ID-column
# maybe need to change the csv-files 

import csv

with open('jsonformatter.csv','rb') as input, open('current.csv','wb') as output:
    reader = csv.reader(input, delimiter = ',')
    writer = csv.writer(output, delimiter = ',')

    all = []
    row = next(reader)
    row.insert(0, 'ID')
    all.append(row)
    for k, row in enumerate(reader):
        all.append([str(k+1)] + row)
    writer.writerows(all)
