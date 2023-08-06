import random
import time
from ddtank import Status
from typing import List


class Team:
    captain: Status
    members: List[Status]

    def __init__(self, captain, *members):
        self.captain = Status(captain)
        self.members = [Status(member) for member in members] + [self.captain]

        self.active_member = 0

    def make_room(self):
        self.captain.click('rfind', pos=(603, 33), rgb=(176, 9, 3))  # 战斗
        self.captain.click('rfind', pos=(658, 139), rgb=(82, 52, 45))  # 码头
        self.captain.click('rfind', pos=(629, 520), rgb=(87, 45, 13))  # 创建房间
        self.captain.click('rfind', pos=(728, 481), rgb=(255, 219, 105))  # 房间设置
        self.captain.click('rfind', pos=(485, 124), rgb=(227, 226, 213))  # 选中密码
        self.captain.input(str(random.randint(100000, 999999)))

    def team_task(self, level: int):
        while not self.captain.find('find', pos=(), rgb=()):  # 是否在房间中
            for status in self.members:
                if status.find('find', pos=(495, 163), rgb=(255, 255, 224)):
                    task = status.team_task[level][self.active_member // len(self.members)]
                    if isinstance(task[0], str) and task[0] in ['left', 'l', '左', 'right', 'r', '右']:
                        status.move(*task)  # move_face: str, move_period: int, reverse_face: bool
                    else:
                        status.shot(*task)  # shot_angle: Union[int, tuple], shot_strength: int, shot_item: tuple
                    self.active_member += 1
            time.sleep(1)

