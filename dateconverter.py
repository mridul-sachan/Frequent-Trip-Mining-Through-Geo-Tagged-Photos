import csv
import time
'''
with open('selfmadedata.csv', 'rb') as csvfile:
    for line in csvfile.readlines():
        array = line.split(',')
        date = array[3]
        print date '''

date1 = []

f1 = open ("ProcessedData.csv","r") # open input file for reading

with open('ProcessedData_out.csv', 'wb') as f: # output csv file
    writer = csv.writer(f)
    with open('ProcessedData.csv','r') as csvfile: # input csv file
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if row[3] != 'datetaken':
                date_time = row[3]
                pattern = '%d-%m-%Y %H:%M'
                epoch = int(time.mktime(time.strptime(date_time, pattern)))
                row[3] = epoch
                date1.append(epoch)
            print row
            writer.writerow(row)
f1.close()