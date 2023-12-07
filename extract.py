# Extract daily net sales from Tropical Smoothie Cafe text data
import time

def extract(fname):
    """
    Extracts daily net sales data from text file
    :param fname:
    :rtype: <Dictionary> with Linux UTC timestamp keys
    """
    res = dict()
    with open(fname, 'r') as f:
        new_rec = True
        for line in f:
            l = line.split()
            if l[0] == 'MI-040' and new_rec:
                # Generate timestamp
                date = l[-1].split('/')
                # Add leading 0s to date
                for i in range(len(date)):
                    if len(date[i]) < 2:
                        date[i] = '0' + date[i]
                date = ''.join(date)
                tstamp = int(time.mktime(time.strptime(date, '%m%d%y'))+time.timezone)
                res[tstamp] = dict()
            elif l[0] == 'Returns':
                # Extract net sales
                for i in range(len(l)):
                    if l[i] == 'Sales':
                        sales = float(l[i+1].replace(',', ''))
                        break
                res[tstamp]['sales'] = sales
                new_rec = False
            elif l[0] == 'Smoothies':
                # Extract smoothies
                res[tstamp]['smoothies'] = int(l[1].replace(',', ''))
                res[tstamp]['smoothie_sales'] = float(l[2].replace(',', ''))
            elif l[0] == 'Food':
                # Extract food
                res[tstamp]['food'] = int(l[1].replace(',', ''))
                res[tstamp]['food_sales'] = float(l[2].replace(',', ''))
            elif l[0] == 'MI-040' and not new_rec:
                # Skip second page
                new_rec = True
    return res
    
def extract_lists(fname):
    # Same as extract but returns a set up lists instead of a dict
    raw = extract(fname)
    field_names = list(raw[raw.keys()[0]].keys())
    num_fields = len(field_names)
    res = [list() for i in range(num_fields+1)]
    for k in raw:
        res[0] += [k]
        for i in range(len(field_names)):
            res[i+1] += [raw[k][field_names[i]]]
    return res