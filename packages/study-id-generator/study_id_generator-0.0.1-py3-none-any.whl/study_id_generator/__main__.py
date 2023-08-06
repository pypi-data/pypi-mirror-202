import os
import sys
import traceback
import signal
import logging
import pathlib
import configparser
import requests
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import paired_distances
import wx

CONFIG_PATH = pathlib.Path.home().joinpath(".config/study_id_generator/config.ini")

class MainFrame(wx.Frame):    
    def __init__(self):
        super().__init__(parent=None, title='Study ID Generator', size=(800,600))

        panel = wx.Panel(self)        
        box_sizer = wx.BoxSizer(wx.VERTICAL)  

        button = wx.Button(panel, label='Generate Study ID')
        button.Bind(wx.EVT_BUTTON, self.on_press)
        box_sizer.Add(button, 0, wx.ALL | wx.CENTER, 5)        
      
        style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL
        self.text_ctrl = wx.TextCtrl(panel, style=style)
        box_sizer.Add(self.text_ctrl, 1, wx.EXPAND)     

        panel.SetSizerAndFit(box_sizer)

        self.Show()

    def on_press(self, event):

        try:

            self.text_ctrl.AppendText(f"Loading configuration at {CONFIG_PATH}.\n")

            config_path = pathlib.Path(CONFIG_PATH)
            config = configparser.ConfigParser()
            config.read(config_path)

            MIN_ID = int(config['DEFAULT']['MIN_ID'])
            MAX_ID = int(config['DEFAULT']['MAX_ID'])
            ID_WIDTH = int(config['DEFAULT']['ID_WIDTH'])
            ID_FILLCHAR = config['DEFAULT']['ID_FILLCHAR']

            ids = []

            for section in config.sections():

                URL = config[section]['URL']
                API_KEY = config[section]['API_KEY']
                CERT_PATH = config[section]['CERT_PATH']
                FIELD_NAME = config[section]['FIELD_NAME']
                ID_REGEX = config[section]['ID_REGEX']

                data = {
                    'token': API_KEY,
                    'content': 'record',
                    'format': 'json',
                    'type': 'flat',
                    'fields[0]': FIELD_NAME
                }

                self.text_ctrl.AppendText(f"Requesting identifiers from {section}.\n")

                with requests.post(URL, data=data, verify=CERT_PATH, timeout=60) as res:
                    if not res.ok:
                        raise Exception(f"""Status Code: {res.status_code}  Content: {res.content}""")

                df = pd.DataFrame(res.json())

                df = df.loc[df[FIELD_NAME].str.contains(ID_REGEX) == True]

                ids.append(df[FIELD_NAME])

            ds = pd.concat(ids)

            ds = ds.drop_duplicates()

            df = ds.to_frame(name='id') # type: ignore

            df['id'] = df['id'].astype(str).str.pad(ID_WIDTH, side='left', fillchar=ID_FILLCHAR)

            id_variants = pd.Series(range(MIN_ID, MAX_ID))

            id_variants = id_variants.astype(str).str.pad(ID_WIDTH, side='left', fillchar=ID_FILLCHAR)

            id_variants = id_variants.loc[~id_variants.isin(df['id'])]

            df['id_variant'] = [id_variants.tolist()] * df.shape[0]

            df = df.explode('id_variant')

            self.text_ctrl.AppendText(f"Calculating pairwise distance between {df.shape[0]} pairs.\nThis will take some time...\n")

            df['id_vector'] = df['id'].apply(lambda x: [int(i) for i in list(x)])

            df['id_variant_vector'] = df['id_variant'].apply(lambda x: [int(i) for i in list(x)])
            
            df['dist'] = paired_distances(np.array(df['id_vector'].tolist()), np.array(df['id_variant_vector'].tolist()))

            df = df.groupby(['id_variant'])['dist'].agg(['mean'])

            df = df.loc[df['mean'] == df['mean'].max()]
            
            df = df.sample(n=1)

            study_id = df.index[0]

            self.text_ctrl.AppendText(f"The identifier with the greatest mean distance in {ID_WIDTH} dimensional space is: {study_id}.\n")

        except Exception as e:
            logger.error(f'{traceback.format_exc()}')
        finally:
            pass



if __name__ == '__main__':

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)

    for handler in logger.handlers.copy():
        logger.removeHandler(handler)
        logger.addHandler(ch)
        
    try:
        signal.signal(signal.SIGTERM, lambda signalnum, frame: sys.exit(0))

        app = wx.App()
        frame = MainFrame()
        app.MainLoop()

    except Exception as e:
        raise e
    
    except BaseException as e:
        logger.warning('Exiting.')
        logger.error(f'{traceback.format_exc()}')
        raise e
    
    finally:
        pass
