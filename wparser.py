# Parse (hopefully) relevent weather data from NOAA weather station data (CSV)

import time

class WeatherEvents(object):
    def __init__(self, eventstr):
        self.events = {
        'shallow':      0,
        'patches':      0,
        'partial':      0,
        't_storm':      0,
        'blowing':      0,
        'showers':      0,
        'drifting':     0,
        'freezing':     0,
        'drizzle':      0,
        'rain':         0,
        'snow':         0,
        'snow_grains':  0,
        'ice_crystals': 0,
        'ice_pellets':  0,
        'hail':         0,
        'sm_hail_snow': 0,
        'mist':         0,
        'fog':          0,
        'smoke':        0,
        'haze':         0,
        'spray':        0,
        'dust':         0,
        'squall':       0,
        'funnel_cloud': 0,
        'tornado':      0}
         
        for event in eventstr.split(' '):
            if 'MI' in event:
                self.events['shallow'] = self.intensity(event)
            elif 'BC' in event:
                self.events['patches'] = self.intensity(event)
            elif 'PR' in event:
                self.events['partial'] = self.intensity(event)
            elif 'TS' in event:
                self.events['t_storm'] = self.intensity(event)
            elif 'BL' in event:
                self.events['blowing'] = self.intensity(event)
            elif 'SH' in event:
                self.events['showers'] = self.intensity(event)
            elif 'DR' in event:
                self.events['drifting'] = self.intensity(event)
            elif 'FZ' in event:
                self.events['freezing'] = self.intensity(event)
            elif 'DZ' in event:
                self.events['drizzle'] = self.intensity(event)
            elif 'RA' in event:
                self.events['rain'] = self.intensity(event)
            elif 'SN' in event:
                self.events['snow'] = self.intensity(event)
            elif 'SG' in event:
                self.events['snow_grains'] = self.intensity(event)
            elif 'IC' in event:
                self.events['ice_crystals'] = self.intensity(event)
            elif 'PL' in event:
                self.events['ice_pellets'] = self.intensity(event)
            elif 'GR' in event:
                self.events['hail'] = self.intensity(event)
            elif 'GS' in event:
                self.events['sm_snow_hail'] = self.intensity(event)
            elif 'BR' in event:
                self.events['mist'] = self.intensity(event)
            elif 'FG' in event:
                self.events['fog'] = self.intensity(event)
            elif 'FU' in event:
                self.events['smoke'] = self.intensity(event)
            elif 'HZ' in event:
                self.events['haze'] = self.intensity(event)
            elif 'PY' in event:
                self.events['spray'] = self.intensity(event)
            elif 'SQ' in event:
                self.events['squall'] = self.intensity(event)
            elif 'FC' in event and not event.startswith('+'):
                self.events['funnel_cloud'] = self.intensity(event)
            elif 'FC' in event and event.startswith('+'):
                self.events['tornado'] = self.intensity(event[1:])
    
    def intensity(self, event):
        if '-' in event:
            return 1
        elif '+' in event:
            return 3
        else:
            return 2


def parse(fname):
    res = dict()
    with open(fname, 'r') as f:
        col_names = ''
        for line in f:
            l = [i.strip() for i in line.split(',')]
            if col_names and len(l) == len(col_names) and l.count('M') < 5:
                # Quantify trace observations and convert missing data
                for i in range(len(l)):
                    if l[i] == 'T':
                        l[i] = 0.005
                    elif l[i] == 'M':
                        l[i] = None
                raw = dict(zip(col_names, l))
                # Generate timestamp
                date = raw['YearMonthDay']
                tstamp = int(time.mktime(time.strptime(date, '%Y%m%d'))+time.timezone)
                # Add data
                try:
                    res[tstamp] = {'t_max': int(raw['Tmax']), 't_min': int(raw['Tmin']),
                                't_avg': int(raw['Tavg']), 'depart': int(raw['Depart']),
                                'dew_point': int(raw['DewPoint']), 
                                'wet_bulb': int(raw['WetBulb']),
                                'sunrise': int(raw['Sunrise']), 
                                'sunset': int(raw['Sunset']),
                                'depth': int(raw['Depth']), 
                                'snow_fall': float(raw['SnowFall']),
                                'precip_total': float(raw['PrecipTotal']), 
                                'stn_pressure': float(raw['StnPressure']),
                                'result_speed': float(raw['ResultSpeed']),
                                'result_dir' : int(raw['ResultDir']),
                                'avg_speed': float(raw['AvgSpeed']), 
                                'max_5_speed': int(raw['Max5Speed']),
                                'max_5_dir': int(raw['Max5Dir']), 
                                'max_2_speed': int(raw['Max2Speed']),
                                'max_2_dir': int(raw['Max2Dir'])}
                except TypeError:
                    # Ignore incomplete records
                    continue
                # Parse weather event codes
                wevents = WeatherEvents(raw['CodeSum'])
                for k in wevents.events:
                    res[tstamp][k] = wevents.events[k]
                               
            elif l[0] == 'WBAN':
                col_names = l
    return res
    
def merge(d, curs):
    fields = list()
    vals = list()
    for k in d:
        if not fields:
            fields += [i for i in d[k].keys()]
        vals += [[k] + [d[k][f] for f in fields]]
    fieldstr = ' (date,' + ','.join(fields) + ') '
    valstr = ' (' + ','.join(['?']*(len(fields)+1)) + ') '
    curs.executemany('INSERT INTO weather %s VALUES %s' % (fieldstr, valstr), vals)
    curs.connection.commit()