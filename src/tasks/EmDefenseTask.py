import time
from ok import BaseTask

class EmDefenseTask(BaseTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "扼守"
        self.description = "扼守（65级）"
        self.default_config.update({
            '技能按键': 'e',
            '技能频率(秒)': 120,
            '技能次数':1,
            '循环次数(0为无尽)':0,
            '启用月卡识别': True,
        })

    def run(self):
        self.log_info('任务开始运行!', notify=True)
        self.begin_challenge()
        self.log_info('任务运行完成!', notify=True)

    def find_some_text_on_bottom_right(self):
        return self.ocr(box="bottom_right",match="确认选择", log=True) #指定box以提高ocr速度

    def find_start_challenge(self):
        return self.find_one(feature_name="开始挑战",box=None)

    def begin_challenge(self):
        self.sleep(1)
        confirm_select_btn = self.find_some_text_on_bottom_right()
        if confirm_select_btn:
            self.log_info("匹配确认选择")
            self.click(confirm_select_btn)
            self.select_buff_and_begin()
            self.match_map()


    def select_buff_and_begin(self):
        self.sleep(1)
        self.log_info("匹配开始挑战")
        self.click(self.find_start_challenge())

    def finish_mission(self):
        self.sleep(1)
        self.log_info("正在结束任务")
        self.back()
        finish_btn = self.find_one('结束任务界面')
        self.click(finish_btn)
        confirm_finish_btn = self.find_one('退出委托界面')
        self.click(confirm_finish_btn)
        self.log_info("已结束任务")

    def match_map(self):
        map_box = self.wait_feature('初始地图',time_out=10)
        if not map_box:
            self.log_info("没有匹配到初始地图，结束任务")
            self.finish_mission()
        else:
            self.log_info("匹配到初始地图")
            self.move_to_target()

    def move_to_target(self):
        self.log_info("开始移动到目标位置")
        move_start = time.time()
        try:
            # ===== 根据扼守-30or65.json录制的路径 =====
            # 0.52s: 开始向前移动
            self.send_key_down("lalt")

            self.sleep(2)
            self.send_key_down("w")

            # 1.11s: 开始冲刺 (0.59s后)
            self.sleep(0.59)
            self.send_key_down("lshift")

            # 1.33s: 向左移动 (0.22s后)
            self.sleep(0.22)
            self.send_key_down("a")

            # 2.41s: 停止前进 (1.08s后)
            self.sleep(1.08)
            self.send_key_up("w")

            # 3.85s: 再次向前 (1.44s后)
            self.sleep(1.44)
            self.send_key_down("w")

            # 3.94s: 停止向左 (0.09s后)
            self.sleep(0.09)
            self.send_key_up("a")

            # 4.84s: 再次向左 (0.90s后)
            self.sleep(0.90)
            self.send_key_down("a")

            # 5.22s-7.82s: Shift连续切换 (可能在调整位置)
            self.sleep(0.38)
            self.send_key_up("lshift")
            self.sleep(0.24)
            self.send_key("lshift", down_time=0.35)
            self.sleep(0.79)
            self.send_key("lshift", down_time=0.41)
            self.sleep(0.80)
            self.send_key_down("lshift")

            # 9.09s: 停止前进 (1.27s后)
            self.sleep(1.27)
            self.send_key_up("w")

            # 9.56s: 短暂前进 (0.47s后)
            self.sleep(0.47)
            self.send_key_down("w")

            # 9.91s: 停止前进 (0.35s后)
            self.sleep(0.35)
            self.send_key_up("w")

            # 10.70s: 跳跃 (0.79s后)
            self.sleep(0.79)
            self.send_key("space", down_time=0.09)

            # 12.83s: 短暂后退调整 (2.04s后)
            self.sleep(2.04)
            self.send_key("s", down_time=0.09)

            # 13.32s: 短暂前进调整 (0.40s后)
            self.sleep(0.40)
            self.send_key("w", down_time=0.10)

            # 13.86s: 再次短暂后退 (0.44s后)
            self.sleep(0.44)
            self.send_key("s", down_time=0.10)

            # 18.89s-18.99s: 释放所有移动键 (4.93s后)
            self.sleep(4.93)
            self.send_key_up("lshift")
            self.sleep(0.10)
            self.send_key_up("a")

            self.send_key_up("lalt")
            # 19.97s: 复位并传送到目标位置
            # self.reset_and_transport()
        except Exception as e:
            pass
        finally:
            pass