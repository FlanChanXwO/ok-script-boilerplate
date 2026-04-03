from ok import BaseTask

class Abc(BaseTask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "c"
        self.description = "c2"

        self.capture_config = {
        'windows': {
        'exe': 'com.bilibili.nslg.exe',
        'hwnd_class': 'UnityWndClass',
        'interaction': 'Pynput',
        'capture_method': 'BitBlt_RenderFull',
        # 'resolution': (2560, 1440),
        }
        }
        
    def run(self):
        self.sleep(0.71) # wait for 0.71s
        self.send_key('esc', down_time=0.17) # press key 'esc'
        self.sleep(0.68) # wait for 0.68s
        self.click(901, 856, down_time=0.10) # left click at (901, 856)
        self.sleep(0.75) # wait for 0.75s
        self.click(1159, 1359, down_time=0.09) # left click at (1159, 1359)
        self.sleep(0.96) # wait for 0.96s
        self.click(227, 82, down_time=0.10) # left click at (227, 82)
        self.sleep(1.18) # wait for 1.18s
        self.click(2715, 829, down_time=0.08) # left click at (2715, 829)