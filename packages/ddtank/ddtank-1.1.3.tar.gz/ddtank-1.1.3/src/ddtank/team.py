import random

from ddtank import Status
from typing import Union


class Team:
    def __init__(self, status_captain: Status,
                 status_member_1: Union[None, Status] = None,
                 status_member_2: Union[None, Status] = None,
                 status_member_3: Union[None, Status] = None):
        self.captain = status_captain
        self.member_1, self.member_2, self.member_3 = status_member_1, status_member_2, status_member_3
        self.member_list = [self.member_1, self.member_2, self.member_3]

        self.captain.repeat_find_period = 100

    def make_room(self):
        self.captain.click('rfind', pos=(603, 33), rgb=(176, 9, 3))  # 战斗
        self.captain.click('rfind', pos=(658, 139), rgb=(82, 52, 45))  # 码头
        self.captain.click('rfind', pos=(629, 520), rgb=(87, 45, 13))  # 创建房间
        self.captain.click('rfind', pos=(728, 481), rgb=(255, 219, 105))  # 房间设置
        self.captain.click('rfind', pos=(485, 124), rgb=(227, 226, 213))  # 选中密码
        self.captain.input(str(random.randint(100000, 999999)))

    def select(self):
        self.captain.click('rfind', pos=(286, 241), rgb=(92, 71, 23))
        self.captain.click('rfind', pos=(372, 501), rgb=(162, 89, 7))
        self.captain.click('rfind', pos=(501, 565), rgb=(255, 204, 0))  # 确认

    def invite(self, member_num: int = 0):
        self.captain.click('rfind', pos=(800, 494), rgb=(8, 187, 240))
        self.captain.click('rfind', pos=(537, 170), rgb=(0, 174, 145))
        self.captain.click('rfind_image', img='invite')
        for member in self.member_list:
            if member is not None:
                member.activate()
            else:
                break
        for i in range(member_num):
            self.captain.click('rfind_image', img='invite_button')
            self.captain.sleep(1500)
            for member in self.member_list:
                if member is not None:
                    is_invited = self.member_1.click('find', pos=(417, 431), rgb=(113, 80, 8))
                    if is_invited:
                        self.member_1.click('rfind', pos=(938, 518), rgb=(233, 222, 176))
                else:
                    break

    def start_instance(self):
        self.captain.click('rfind', pos=(944, 515), rgb=(255, 249, 208))  # 开始
        self.captain.sleep(100)
        self.captain.press('enter')

    def fight_1(self):
        pass

    def fight_2(self):
        pass

    def fight_3(self):
        pass

    def fight_4(self):
        pass

    def task(self):
        self.make_room()
        self.select()
        # self.start_instance()
        # self.fight_1()
        # self.start_instance()
        # self.fight_2()
        # self.start_instance()
        # self.fight_3()
        self.invite(1)
        # self.start_instance()
        # self.fight_4()



