import inspect
import os
import threading as th
import time
from typing import ClassVar

from autowsgr.constants.custom_exceptions import CriticalErr, ImageNotFoundErr, NetworkErr
from autowsgr.constants.data_roots import DATA_ROOT, OCR_ROOT
from autowsgr.constants.image_templates import IMG
from autowsgr.constants.other_constants import ALL_PAGES
from autowsgr.constants.ui import WSGR_UI, Node
from autowsgr.port.common import Port
from autowsgr.timer.backends import EasyocrBackend, PaddleOCRBackend
from autowsgr.timer.controllers import AndroidController, WindowsController
from autowsgr.utils.io import yaml_to_dict
from autowsgr.utils.logger import Logger
from autowsgr.utils.operator import unzip_element


# TODO: fix class variable
class Timer(AndroidController, WindowsController):
    """程序运行记录器, 用于记录和传递部分数据, 同时用于区分多开, WSGR 专用"""

    # 战舰少女R专用控制器
    everyday_check = True
    ui = WSGR_UI
    plan_root_list: ClassVar[dict] = {}
    ship_stats: ClassVar[list] = [0, 0, 0, 0, 0, 0, 0]  # 我方舰船状态
    enemy_type_count: ClassVar[dict] = {}  # 字典,每种敌人舰船分别有多少
    now_page = None  # 当前所在 UI 名
    resources = None  # 当前四项资源量
    got_ship_num = 0  # 当天已掉落的船
    got_loot_num = 0  # 当天已掉落的胖次
    quick_repaired_cost = 0  # 消耗快修数量
    """
    以上时能用到的
    以下是暂时用不到的
    """
    last_mission_completed = 0

    last_expedition_check_time = time.time()

    def __init__(self, config, logger: Logger) -> None:
        self.port = Port(logger)
        self.config = config
        self.logger = logger

        # 初始化android控制器
        WindowsController.__init__(self, config.emulator, logger)

        dev = self.connect_android()
        AndroidController.__init__(self, config, logger, dev)

        if self.config.OCR_BACKEND == 'easyocr':
            self.ocr_backend = EasyocrBackend(config, logger)
        elif self.config.OCR_BACKEND == 'paddleocr':
            self.ocr_backend = PaddleOCRBackend(config, logger)
        else:
            raise ValueError(f'Unknown OCR_BACKEND: {self.config.OCR_BACKEND}')

        # 获取调用栈信息
        stack = inspect.stack()
        # 最初启动脚本的路径在调用栈的最后一个元素中
        script_running_directory = os.path.abspath(stack[-1].filename)
        # 从脚本运行目录查找plans和ship_name，如果存在则使用，不存在则使用默认的
        # 加载plans文件夹
        self.logger.info('尝试从脚本运行目录加载plans')
        if os.path.exists(
            os.path.abspath(os.path.join(script_running_directory, '..', 'plans')),
        ):
            config.PLAN_ROOT = os.path.abspath(
                os.path.join(script_running_directory, '..', 'plans'),
            )
            self.logger.info(f'Succeed to load PLAN_ROOT: {self.config.PLAN_ROOT}')
        else:
            self.logger.warning(
                f"从脚本运行目录加载plans失败，将会从默认目录 {os.path.join(DATA_ROOT, 'plans')} 加载plans",
            )
            config.PLAN_ROOT = os.path.join(DATA_ROOT, 'plans')

        self.create_nested_dict(config.PLAN_ROOT)
        self.plan_root_list = self.update_nested_dict(
            self.create_nested_dict(os.path.join(DATA_ROOT, 'plans')),
            self.create_nested_dict(config.PLAN_ROOT),
        )

        # 加载舰船名文件
        defult_ship_names = yaml_to_dict(os.path.join(OCR_ROOT, 'ship_name.yaml'))
        self.logger.info('尝试从脚本运行目录加载ship_names.yaml')
        if os.path.exists(
            os.path.abspath(
                os.path.join(script_running_directory, '..', 'ship_names.yaml'),
            ),
        ):
            config.SHIP_NAME_PATH = os.path.abspath(
                os.path.join(script_running_directory, '..', 'ship_names.yaml'),
            )
            self.ship_names = yaml_to_dict(config.SHIP_NAME_PATH)
            self.logger.info(f'Succeed to load ship_name file:{config.SHIP_NAME_PATH}')
            self.ship_names = self.update_nested_dict(
                defult_ship_names,
                self.ship_names,
            )
        else:
            self.ship_names = defult_ship_names
        self.ship_names = unzip_element(list(self.ship_names.values()))

        self.init()

    # ========================= OCR 功能穿透 =========================
    def create_nested_dict(self, directory):
        """
        创建一个嵌套字典，表示目录及其子目录中的文件
        Args:
            directory (str): 目录路径
        Returns:
            dict: 嵌套字典，表示目录结构
        """
        for root, _dirs, files in os.walk(directory):
            # 获取相对于根目录的路径
            rel_path = os.path.relpath(root, directory)
            # 获取当前层级的字典
            current_dict = self.plan_root_list
            if rel_path != '.':
                for part in rel_path.split(os.sep):
                    current_dict = current_dict.setdefault(part, {})
            # 将文件添加到当前层级的字典中
            for file in files:
                file_key = file[:-5] if file.endswith('.yaml') else file
                # 赋予其绝对路径
                current_dict[file_key] = os.path.abspath(os.path.join(root, file))
        return self.plan_root_list

    def update_nested_dict(self, d1, d2):
        """
        递归地更新嵌套字典 d1，使其包含 d2 中的所有键值对。
        如果键在两个字典中都存在且对应的值也是字典，则递归更新。
        Args:
            d1 (dict): 要更新的字典
            d2 (dict): 用于更新的字典
        Returns:
            dict: 更新后的字典 d1
        """
        for k, v in d2.items():
            if k in d1 and isinstance(d1[k], dict) and isinstance(v, dict):
                self.update_nested_dict(d1[k], v)
            else:
                d1[k] = v
        return d1

    def recognize(
        self,
        img,
        allowlist: list[str] | None = None,
        candidates: list[str] | None = None,
        multiple=False,
        allow_nan=False,
        rgb_select=None,
        tolerance=30,
        **kwargs,
    ):
        """识别任意字符串"""
        return self.ocr_backend.recognize(
            img,
            allowlist,
            candidates,
            multiple,
            allow_nan,
            rgb_select,
            tolerance,
            **kwargs,
        )

    def recognize_number(
        self,
        img,
        extra_chars='',
        multiple=False,
        allow_nan=False,
        **kwargs,
    ):
        """识别数字"""
        return self.ocr_backend.recognize_number(
            img,
            extra_chars,
            multiple,
            allow_nan,
            **kwargs,
        )

    def recognize_ship(self, image, candidates, **kwargs):
        """传入一张图片,返回舰船信息,包括名字和舰船型号"""
        return self.ocr_backend.recognize_ship(image, candidates, **kwargs)

    # ========================= 初级游戏控制 =========================
    def init(self):
        """初始化游戏状态, 以便进一步的控制"""
        self.app_name = self.which_app
        # ========== 启动游戏 ==========
        if self.config.account is not None and self.config.password is not None:
            self.restart(account=self.config.account, password=self.config.password)
        if not self.is_game_running():
            self.start_game()
        self.start_app(self.app_name)

        # ========== 检查游戏页面状态 ============

        try:
            self.set_page()
            self.logger.info(f'启动成功, 当前位置: {self.now_page.name}')
        except:
            if 'CHECK_PAGE' in self.config.__dict__ and self.config.CHECK_PAGE:
                self.logger.warning('无法确定当前页面, 尝试重启游戏')
                self.restart()
                self.set_page()
            else:
                self.logger.warning('在无法确定页面的情况下继续.')

    def log_in(self, account, password):
        pass

    def log_out(self, account, password):
        """在登录界面登出账号"""

    def start_game(self, account=None, password=None, delay=1.0):
        """启动游戏"""
        self.start_app(self.app_name)
        res = self.wait_images(
            [IMG.start_image[2]] + IMG.confirm_image[1:],
            0.85,
            gap=1,
            timeout=70 * delay,
        )

        if res is None:
            raise TimeoutError('start_app timeout')
        if res != 0:
            self.confirm_operation()
            if not self.wait_image(IMG.start_image[2], timeout=200):
                raise TimeoutError('resource downloading timeout')

        # ========= 登录 =========

        if account is not None and password is not None:
            self.click(75, 450)
            if not self.wait_image(IMG.start_image[3]):
                raise TimeoutError("can't enter account manage page")
            self.click(460, 380)
            if not self.wait_image(IMG.start_image[4]):
                raise TimeoutError("can't logout successfully")
            self.click(540, 180)
            for _ in range(20):
                p = th.Thread(target=lambda: self.shell('input keyevent 67'))
                p.start()
            p.join()
            self.text(str(account))
            self.click(540, 260)
            for _ in range(20):
                p = th.Thread(target=lambda: self.shell('input keyevent 67'))
                p.start()
            p.join()
            time.sleep(0.5)
            self.text(str(password))
            self.click(400, 330)
            res = self.wait_images([IMG.start_image[5], IMG.start_image[2]])
            if res is None:
                raise TimeoutError('login timeout')
            if res == 0:
                raise CriticalErr('password or account is wrong')

        # =========== 开始游戏 ===========

        delay = 15
        while self.image_exist(IMG.start_image[2]):
            self.click_image(IMG.start_image[2])
            if self.wait_image(IMG.game_ui[3], timeout=delay, after_get_delay=0.25):
                break
            delay *= 2
            if delay > 30:
                raise ImageNotFoundErr("can't start game")
        # ============ 关闭新闻, 领取每日奖励 =============

        try:
            if self.everyday_check:
                self.logger.info('正在尝试关闭新闻, 领取奖励')
                if self.wait_image(IMG.start_image[6], timeout=2):  # 新闻与公告,设为今日不再显示
                    if not self.check_pixel((70, 485), (201, 129, 54)):
                        self.click(70, 485)
                    self.click(30, 30)
                if self.wait_image(IMG.start_image[7], timeout=7):  # 每日签到
                    self.click(474, 357)
                    self.confirm_operation(must_confirm=1, timeout=2)
                self.everyday_check = False
            self.go_main_page()
            self.logger.info('游戏启动成功!')
        except:
            raise CriticalErr('fail to start game')

    def restart(self, times=0, *args, **kwargs):
        try:
            self.shell(f'am force-stop {self.app_name}')
            self.shell('input keyevent 3')
            self.start_game(**kwargs)
        except Exception:
            if not self.is_android_online():
                pass

            elif times == 1:
                raise CriticalErr('on restart,')

            elif not self.check_network():
                for i in range(11):
                    time.sleep(10)
                    if self.check_network():
                        break
                    if i == 10:
                        raise NetworkErr

            elif self.is_game_running():
                raise CriticalErr('CriticalErr on restart function')

            self.connect_android()
            self.restart(times + 1, *args, **kwargs)

    def is_other_device_login(self, timeout=2):
        """检查是否有其他设备登录顶号"""
        return self.wait_images(IMG.error_image['user_remote_login'], timeout=timeout) is not None

    def process_other_device_login(self, timeout=2):
        """处理其他设备登录顶号
        TODO: 重新登录以后写，暂时留空,直接抛出错误
        """
        if self.is_other_device_login(timeout):
            self.log_screen(need_screen_shot=True, name='other device login.PNG')
            self.logger.error('other device login')
            raise CriticalErr('other device login')

    def is_bad_network(self, timeout=10):
        """检查是否为网络状况问题"""
        return (
            self.wait_images(
                [IMG.symbol_image[10]] + IMG.error_image['bad_network'],
                timeout=timeout,
            )
            is not None
        )

    def reset_chapter_map(self):
        self.port.chapter = None
        self.port.map = None

    def process_bad_network(self, extra_info='', timeout=10):
        """判断并处理网络状况问题
        Returns:
            bool: 如果为 True 则表示为网络状况问题,并已经成功处理,否则表示并非网络问题或者处理超时.
        Raise:
            TimeoutError:处理超时
        """
        start_time = time.time()
        while self.is_bad_network(timeout):
            self.log_screen(need_screen_shot=True, name='bad_network.PNG')
            self.logger.warning(f'bad network: {extra_info}')

            # 等待网络恢复

            if not self.wait_network():
                raise NetworkErr("can't connect to www.moefantasy.com")

            # 处理网络问题
            while self.wait_images(
                [IMG.symbol_image[10]] + IMG.error_image['bad_network'],
                timeout=3,
            ):
                time.sleep(0.5)

                if self.image_exist(IMG.error_image['bad_network']):
                    self.click_image(IMG.error_image['network_retry'])

                if not self.wait_images(
                    [IMG.symbol_image[10]] + IMG.error_image['bad_network'],
                    timeout=5,
                ):
                    self.logger.debug('ok network problem solved')
                    self.reset_chapter_map()
                    return True

                if time.time() - start_time > 1800:
                    raise TimeoutError('process bad network timeout')
        return False

    # ========================= 维护当前所在游戏界面 =========================
    def _integrative_page_identify(self) -> int | None:
        positions = [(171, 47), (300, 47), (393, 47), (504, 47), (659, 47)]
        for i, position in enumerate(positions):
            if self.check_pixel(position, (225, 130, 16)):
                return i + 1
        return None

    def identify_page(self, name, need_screen_shot=True):
        if need_screen_shot:
            self.update_screen()

        if (name == 'main_page') and (self.identify_page('options_page', 0)):
            return False
        if (name == 'map_page') and (
            self._integrative_page_identify() != 1 or self.check_pixel((35, 297), (47, 253, 226))
        ):
            return False
        if (name == 'build_page') and (self._integrative_page_identify() != 1):
            return False
        if (name == 'develop_page') and (self._integrative_page_identify() != 3):
            return False
        return self.image_exist(IMG.identify_images[name], False)

    def wait_pages(self, names, timeout=10, gap=0.1, after_wait=0.1):
        start_time = time.time()
        if isinstance(names, str):
            names = [names]
        while True:
            self.update_screen()
            for i, name in enumerate(names):
                if self.identify_page(name, 0):
                    time.sleep(after_wait)
                    return i + 1

            if time.time() - start_time > timeout:
                break
            time.sleep(gap)

        if self.is_bad_network(timeout=3) and self.process_bad_network("can't wait pages"):
            return self.wait_pages(names, timeout, gap, after_wait)
        if self.is_other_device_login():
            self.process_other_device_login()

        raise TimeoutError(f'identify timeout of{names!s}')

    def get_now_page(self):
        """获取并返回当前页面名称"""
        self.update_screen()
        for page in ALL_PAGES:
            if self.identify_page(page, need_screen_shot=False):
                return page
        return 'unknown_page'

    def check_now_page(self):
        return self.identify_page(name=self.now_page.name)

    def operate(self, end: Node):
        ui_list = self.ui.find_path(self.now_page, end)
        for next in ui_list[1:]:
            edge = self.now_page.find_edge(next)
            opers = edge.operate()
            self.now_page = next
            for oper in opers:
                fun, args = oper
                if fun == 'click':
                    self.click(*args)
                else:
                    raise ValueError(f'unknown function name: {fun}')

            if edge.other_dst is not None:
                dst = self.wait_pages(names=[self.now_page.name, edge.other_dst.name])
                if dst == 1:
                    continue
                self.logger.debug(
                    f'Go page: {self.now_page.name}, but arrive: {edge.other_dst.name}',
                )
                self.now_page = self.ui.get_node_by_name(
                    [self.now_page.name, edge.other_dst.name][dst - 1],
                )
                self.logger.debug(f'Now page: {self.now_page.name}')
                if self.now_page.name == 'expedition_page':
                    try_to_get_expedition(self)
                self.operate(end)
                return
            self.wait_pages(names=[self.now_page.name])
            time.sleep(0.25)

    def set_page(self, page_name=None, page=None):
        if page_name is None and page is None:
            now_page = self.get_now_page()

            if now_page is None:
                raise ImageNotFoundErr('无法识别该页面')
            if now_page != 'unknown_page':
                self.now_page = self.ui.get_node_by_name(now_page)
            else:
                self.now_page = now_page
        elif page is not None:
            if not isinstance(page, Node):
                self.logger.error('arg:page must be an controller.ui.Node object')
                raise ValueError

            self.now_page = page if (self.ui.page_exist(page)) else 'unknown_page'
        else:
            page = self.ui.get_node_by_name(page_name)
            if page is None:
                page = 'unknown_page'

            self.now_page = page

    def walk_to(self, end, try_times=0):
        try:
            if isinstance(self.now_page, str) and 'unknown' in self.now_page:
                self.go_main_page()
            if isinstance(end, Node):
                self.operate(end)
                self.wait_pages(end.name)
                return
            if isinstance(end, str):
                end = self.ui.get_node_by_name(end)
                if end is None:
                    self.logger.error('unacceptable value of end: {end}')
                    raise ValueError('illegal value:end, in Timer.walk_to')
                self.walk_to(end)

        except TimeoutError as exception:
            if try_times > 3:
                raise TimeoutError("can't access the page")
            if self.is_other_device_login():
                self.process_other_device_login()
            if not self.is_bad_network(timeout=2):
                self.logger.debug(
                    'wrong path is operated,anyway we find a way to solve,processing',
                )
                self.logger.debug('wrong info is:', exception)
                self.go_main_page()
                self.walk_to(end, try_times + 1)
            else:
                while True:
                    if self.process_bad_network(
                        "can't walk to the position because a TimeoutError",
                    ):
                        try:
                            if not self.wait_pages(names=self.now_page.name, timeout=1):
                                self.set_page(self.get_now_page())
                        except Exception:
                            self.go_main_page()
                        else:
                            break
                    else:
                        raise ValueError('unknown error')
                self.walk_to(end)

    def go_main_page(
        self,
        quit_operation_time: int = 0,
        list1: list | None = None,
        list2: list | None = None,
    ) -> None:
        """回退到游戏主页
        Args:
            timer (Timer): _description_
            quit_operation_time (int, optional): _description_. Defaults to 0.
            list1 (list, optional): _description_. Defaults to [].
            list2 (list, optional): _description_. Defaults to [].

        Raises:
            ValueError: _description_
        """
        if list1 is None:
            list1 = []
        if list2 is None:
            list2 = []

        if quit_operation_time > 200:
            if self.is_other_device_login():
                self.process_other_device_login()

            if self.is_bad_network(timeout=3):
                if self.process_bad_network("can't go main page"):
                    self.go_main_page(0, list1)
                    return
            else:
                self.logger.error("Unknown error,can't go main page")
                raise ValueError("Error,Couldn't go main page")
        self.reset_chapter_map()
        self.now_page = self.ui.get_node_by_name('main_page')
        if len(list1) == 0:
            list1 = IMG.back_buttons[1:] + list2
        type = self.wait_images([*list1, IMG.game_ui[3]], 0.8, timeout=0)

        if type is None:
            self.go_main_page(quit_operation_time + 1, list1)
            return

        if type >= len(list1):
            type = self.wait_images(list1, timeout=0)
            if type is None:
                return

        pos = self.get_image_position(list1[type], False, 0.8)
        self.click(pos[0], pos[1])

        new_list = list1[1:] + [list1[0]]
        self.go_main_page(quit_operation_time + 1, new_list)

    def goto_game_page(self, target='main', extra_check=False):
        """到某一个游戏界面

        Args:
            target (str, str): 目标章节名(见 ./constants/other_constants). Defaults to 'main'.
        """
        self.walk_to(target)
        if extra_check:
            self.wait_pages(names=[self.now_page.name])

    def confirm_operation(
        self,
        must_confirm=False,
        delay=0.5,
        confidence=0.9,
        timeout=0,
    ):
        """等待并点击弹出在屏幕中央的各种确认按钮

        Args:
            must_confirm (int, optional): 是否必须按. Defaults to 0.
            delay (float, optional): 点击后延时(秒). Defaults to 0.5.
            timeout (int, optional): 等待延时(秒),负数或 0 不等待. Defaults to 0.

        Raises:
            ImageNotFoundErr: 如果 must_confirm = True 但是 timeout 之内没找到确认按钮排除该异常
        Returns:
            bool:True 为成功,False 为失败
        """
        pos = self.wait_images(
            IMG.confirm_image[1:],
            confidence=confidence,
            timeout=timeout,
        )
        if pos is None:
            if must_confirm:
                raise ImageNotFoundErr('no confirm image found')
            return False
        res = self.get_image_position(
            IMG.confirm_image[pos + 1],
            confidence=confidence,
            need_screen_shot=False,
        )
        self.click(res[0], res[1], delay=delay)
        return True

    @property
    def which_app(self):
        if self.config.game_app == '官服':
            start_game_app = 'com.huanmeng.zhanjian2'
        elif self.config.game_app == '应用宝':
            start_game_app = 'com.tencent.tmgp.zhanjian2'
        elif self.config.game_app == '小米':
            start_game_app = 'com.hoolai.zjsnr.mi'
        return start_game_app


def process_error(timer: Timer):
    print('processing errors')
    if not timer.is_android_online() or not timer.is_game_running():
        timer.restart_android()
        timer.connect_android()

        return 'Android Restarted'

    return 'ok,bad network' if timer.process_bad_network() else 'ok,unknown error'


def try_to_get_expedition(timer: Timer):
    timer.logger.info('Getting Expedition Rewards....')
    get, pos = False, timer.wait_image(IMG.game_ui[6], timeout=2)
    while pos:
        timer.click(pos[0], pos[1], delay=1)
        timer.wait_image(IMG.fight_image[3], after_get_delay=0.25)
        timer.click(900, 500, delay=1)
        timer.confirm_operation(must_confirm=1, delay=0.5, confidence=0.9)
        pos, get = timer.wait_image(IMG.game_ui[6], timeout=2), True
    return get
