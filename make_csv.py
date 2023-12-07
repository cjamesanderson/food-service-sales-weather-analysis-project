# Functions to produce CSV from TSC database

import csv

def make_csv(col, curs):
    # Creates CSV file with sorted (date, col)
    # JOIN to exclude dates with no weather data
    curs.execute('SELECT weather.date, sales.%s FROM sales JOIN weather ON weather.date=sales.date' % col)
    output = sorted(curs.fetchall())
    with open('%s_data.csv' % col, 'w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerows(output)