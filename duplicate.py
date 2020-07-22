# need to install more_itertools
# program delete duplicates (it's for the country.csv)
# need to change the csv-files which you would open

from more_itertools import unique_everseen
with open ('current.csv','r') as f, open ('now.csv','w') as out_file:
    out_file.writelines(unique_everseen(f))
