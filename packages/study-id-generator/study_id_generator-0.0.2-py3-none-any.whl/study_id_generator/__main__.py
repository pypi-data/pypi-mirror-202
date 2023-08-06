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
        super().__init__(parent=None, title='Study ID Generator', size=(400,300))

        self.panel = wx.Panel(self)        
        vbox = wx.BoxSizer(wx.VERTICAL)  
        hbox = wx.BoxSizer(wx.HORIZONTAL)  

        l1 = wx.StaticText(self.panel, 1, "Study ID") 
        self.study_id_window = wx.TextCtrl(self.panel, style=wx.TE_READONLY | wx.TE_RICH)
        self.study_id_window.SetDefaultStyle(wx.TextAttr(wx.RED))

        hbox.Add(l1, proportion=0, flag=wx.ALIGN_LEFT | wx.ALL, border=5) 
        hbox.Add(self.study_id_window, proportion=0, flag= wx.ALIGN_LEFT | wx.ALL, border=0) 

        button = wx.Button(self.panel, label='Generate Study ID')
        button.Bind(wx.EVT_BUTTON, self.on_press, id=wx.ID_ANY)
      
        self.log_window = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)

        vbox.Add(hbox, flag=wx.ALL, border=5)
        vbox.Add(self.log_window, proportion=1, flag=wx.EXPAND)     
        vbox.Add(button, proportion=0, flag=wx.ALL | wx.ALIGN_RIGHT, border=5)        

        self.panel.SetSizerAndFit(vbox)

        self.Show()

        self.log_window.AppendText(f"Loading configuration at {CONFIG_PATH}.\n")

        config_path = pathlib.Path(CONFIG_PATH)
        config = configparser.ConfigParser()
        config.read(config_path)

        self._MIN_ID = int(config['DEFAULT']['MIN_ID'])
        self._MAX_ID = int(config['DEFAULT']['MAX_ID'])
        self._ID_WIDTH = int(config['DEFAULT']['ID_WIDTH'])
        self._ID_FILLCHAR = config['DEFAULT']['ID_FILLCHAR']

        self._section = {section:config[section] for section in config.sections()}

    def on_press(self, event):

        try:
            self.panel.SetCursor(wx.Cursor(wx.CURSOR_ARROWWAIT))

            self.study_id_window.Clear()
            self.study_id_window.Update()
            self.log_window.Clear()
            self.log_window.Update()

            ids = []

            for section_name, section in self._section.items():
                data = {
                    'token': section['API_KEY'],
                    'content': 'record',
                    'format': 'json',
                    'type': 'flat',
                    'fields[0]': section['FIELD_NAME']
                }

                self.log_window.AppendText(f"Requesting identifiers from {section_name}.\n")

                with requests.post(section['URL'], data=data, verify=section['CERT_PATH'], timeout=60) as res:
                    if not res.ok:
                        raise Exception(f"""Status Code: {res.status_code}  Content: {res.content}""")

                df = pd.DataFrame(res.json())

                df = df.loc[df[section['FIELD_NAME']].str.contains(section['ID_REGEX']) == True]

                ids.append(df[section['FIELD_NAME']])

            ds = pd.concat(ids)
                        
            ds = ds.drop_duplicates()

            df = ds.to_frame(name='id') # type: ignore

            df['id'] = df['id'].astype(str).str.pad(self._ID_WIDTH, side='left', fillchar=self._ID_FILLCHAR)

            id_variants = pd.Series(range(self._MIN_ID, self._MAX_ID))

            id_variants = id_variants.astype(str).str.pad(self._ID_WIDTH, side='left', fillchar=self._ID_FILLCHAR)

            id_variants = id_variants.loc[~id_variants.isin(df['id'])]

            df['id_variant'] = [id_variants.tolist()] * df.shape[0]

            df = df.explode('id_variant')

            self.log_window.AppendText(f"Calculating pairwise distance between {df.shape[0]} pairs of identifiers...\n")

            df['id_vector'] = df['id'].apply(lambda x: [int(i) for i in list(x)])

            df['id_variant_vector'] = df['id_variant'].apply(lambda x: [int(i) for i in list(x)])
            
            df['dist'] = paired_distances(np.array(df['id_vector'].tolist()), np.array(df['id_variant_vector'].tolist()))

            df = df.groupby(['id_variant'])['dist'].agg(['mean'])

            df = df.loc[df['mean'] == df['mean'].max()]
            
            df = df.sample(n=1)

            study_id = df.index[0]

            self.study_id_window.AppendText(study_id)

            self.panel.SetCursor(wx.Cursor(wx.CURSOR_ARROW))

        except Exception as e:
            logger.error(f'{traceback.format_exc()}')

        finally:
            pass



if __name__ == '__main__':

    try:
        signal.signal(signal.SIGTERM, lambda signalnum, frame: sys.exit(0))
        signal.signal(signal.SIGINT, lambda signalnum, frame: sys.exit(0))

        logger = logging.getLogger()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch = logging.StreamHandler(stream=sys.stdout)
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        for handler in logger.handlers.copy():
            logger.removeHandler(handler)
            logger.addHandler(ch)

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
