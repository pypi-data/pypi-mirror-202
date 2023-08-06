import pyimclsts.network as n
import pyimc_generated as pg

import pandas as pd
import numpy as np

import xarray as xra
import csv

csv_delimiter = '\x01'#'; '
json_delimiter = ', '

# \copy lauvxplore1 from 'output.csv' delimiter E'\x01';

def tolist(msg_or_value) -> list:
    if isinstance(msg_or_value, pg._base_templates.base_message):
        fields = msg_or_value.Attributes.fields
        values = [tolist(getattr(msg_or_value, f)) for f in fields if tolist(getattr(msg_or_value, f)) is not None]
        
        return [[f, v] for (f, v) in zip(fields, values)]
    elif isinstance(msg_or_value, list):
        return [tolist(i) for i in msg_or_value]
    elif isinstance(msg_or_value, int) or isinstance(msg_or_value, float):
        return msg_or_value
    else: # ignore plaintext and rawdata
        return None
        
class table():
    
    def __init__(self, f : str) -> None:
        '''f is file name'''

        self.file_name = f
        # erases the file if it exists, creates it otherwise
        with open(f, 'w'):
            pass

        self.unwanted_messages = [262, 276, 294]
        self.selected_messages = list(filter(lambda x : x not in self.unwanted_messages, range(250, 300)))

        self.datatable = []
        self.estimated_states = []
            
    def writetotable(self, msg, callback) -> str:
        
        if msg._header.mgid in self.selected_messages:
            time = msg._header.timestamp
            message_abbrev = msg.Attributes.abbrev
            src = msg._header.src
            src_ent = msg._header.src_ent
            
            data = tolist(msg)
            data = [[time, message_abbrev, src, src_ent, *d] for d in data] # i don't think it expects a list with more than 1 item.
            self.datatable += data

        elif isinstance(msg, pg.messages.EstimatedState):
            time = msg._header.timestamp
            
            point = [msg.lat, msg.lon, msg.depth, time]
            
            self.estimated_states.append(point)
        else:
            pass

w = table('output.csv')

if __name__ == '__main__':
    
    src_file = 'Data.lsf'
    sub = n.subscriber(n.file_interface(input = src_file), use_mp=True)

    sub.subscribe_async(w.writetotable)

    sub.run()

    positions = pd.DataFrame(w.estimated_states, columns=['lat', 'lon', 'depth', 'timestamp'])
    values = pd.DataFrame(w.datatable, columns=['timestamp', 'message', 'src', 'src_ent','field', 'value'])

    interpolator = lambda x, key : np.interp(x, positions['timestamp'], positions[key])

    keys = ['lat', 'lon', 'depth']
    for k in keys:
        values[k] = interpolator(values['timestamp'], k)

    metadata = pd.read_csv('AUV_General_Metadata.csv', delimiter=';')
    metadata = metadata.groupby(by = 'Variable Name')

    netcdf_DS = xra.Dataset.from_dataframe(values)
    
    #netcdf_DS.timestamp.attrs['oi'] = 'oi'
    
    #xra.open_dataset(netcdf_DS.to_netcdf())