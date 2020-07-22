# maybe need to change csv-files which you would open
# programm choose specific columns and make it to a new csv-file
# maybe you should use cols[].strip()

with open('jsonformatter.csv','r') as r, open ('current.csv', 'w') as f_out:
    for line in r:
        cols = line.split(',')
        f_out.write(cols[7] + ',' + cols[0] + ',' + cols[1] + '\n')
