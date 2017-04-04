from itertools import repeat
import csv

'''
Created on Nov 17, 2016

@author: ThomasC
'''

print "Parsing the training set of help desk tickets...\n"

with open('../data/tickets-slim.tsv','rb') as tsvin, open('../data/result-slim.tsv', 'wb') as csvout:
    tsvin = csv.reader(tsvin, delimiter='\t')
    csvout = csv.writer(csvout, delimiter='\t')

    for row in tsvin:
        csvout.writerow(row[9:11])
        print(row[9:11]);

