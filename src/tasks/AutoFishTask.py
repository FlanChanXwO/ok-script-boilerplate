from ok import BaseTask
from qfluentwidgets import FluentIcon

class AutoFishTask(BaseTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "自动钓鱼"
        self.description = "需要大师鱼竿+悠闲,请在钓鱼空格界面运行钓鱼任务"
        self.group_name = "全自动"
        self.group_icon = FluentIcon.VIEW
        self.default_config.update({
            '循环次数(0为无尽)': 0
        })
        self.load_config()
        self.stat = {
            "finished_times" : 0,
            "fish_times" : int(self.config['循环次数(0为无尽)']),
            "is_infinite" : int(self.config['循环次数(0为无尽)']) <= 0
        }

    def reset_config(self):
        self.info_clear()
        self.load_config()
        self.stat["finished_times"] = 0
        self.stat["fish_times"] = int(self.config['循环次数(0为无尽)'])
        self.stat["is_infinite"] = int(self.config['循环次数(0为无尽)']) <= 0


    def handle_no_fish(self):
        self.log_info("水中暂时无鱼，停止循环")
        self.sleep(0.5)
        self.back()
        self.sleep(0.5)
        self.back()
        self.sleep(0.5)
        self.back()

    def run(self):
        # 重置配置
        self.reset_config()

        if self.stat["is_infinite"]:
            self.log_info("启用无尽模式")
        else:
            self.log_info("启用有限模式")

        # 开始钓鱼
        while self.stat["is_infinite"] or self.stat["fish_times"] > 0:
            self.info_add("轮次",1)
            self.sleep(1)
            # 奖励鱼
            get_bigger_fish_area = self.find_one("授渔以鱼")
            # 正常钓鱼
            drop_pole_area = self.find_one("丢杆")
            if drop_pole_area or get_bigger_fish_area:
                if drop_pole_area:
                    self.log_info("发现正常鱼")
                    self.send_key("space")
                else:
                    self.log_info("发现奖励鱼")
                    self.send_key("e")
                # 处理无鱼情况
                no_fish_box = self.find_one("水中无鱼")
                if no_fish_box:
                    no_fish_tip_text = self.ocr(name="水中暂时无鱼", box=no_fish_box)
                    if no_fish_tip_text:
                        self.handle_no_fish()
                        break
                # 等待收杆
                self.log_info("正在等待收杆")
                close_pole_area = self.wait_feature("收杆")
                # 正在钓鱼
                if close_pole_area:
                    # 等待收鱼
                    self.log_info("正在等待收鱼")
                    self.wait_feature("丢杆")
                    self.sleep(1)
                    # 收鱼
                    self.send_key("space")
                    self.log_info("正在等待结算")
                    can_close_ui_box = self.wait_feature("可以关闭钓鱼界面")
                    self.wait_ocr(name="点击空白区域关闭",box=can_close_ui_box)
                    # 继续下一次钓鱼
                    self.sleep(1)
                    self.send_key("space")
                    # 统计进度
                    self.stat["finished_times"] +=1
                    self.info_add("钓鱼次数", 1)
                    if get_bigger_fish_area:
                        self.info_add("授渔以鱼",1)
                    if not self.stat["is_infinite"]:
                        # 减少循环次数
                        self.stat["fish_times"]-=1
                        self.log_info(f"当前钓鱼进度为{self.stat["finished_times"]}/{self.stat["fish_times"]}")
                    else:
                        self.log_info(f"钓鱼完成，当前钓鱼次数为{self.stat["finished_times"]}")
                else: # 处理超时（无鱼情况）
                    self.handle_no_fish()
                    break


        self.log_info("已完成自动钓鱼流程",notify=True)
