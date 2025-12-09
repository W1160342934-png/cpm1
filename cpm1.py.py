#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import requests
from time import sleep
import os, signal, sys
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.text import Text
from rich.style import Style
from rich.table import Table

# 从 cylo.py 导入核心类和统一 AccessKey 获取链接
from cylo import Bubcyz, ACCESSKEY_GET_URL

# 导入依赖校验
try:
    from cylo import Bubcyz
except ImportError:
    print("[错误] 缺少 cylo.py 文件，请确保与脚本同目录！")
    sys.exit(1)

# 常量定义
PINK = "#FFC0CB"
PURPLE = "#800080"
SEPARATOR_CHAR = '★'
ASCII_ART = r"""
　  　\.　-　 -　.　　
　　　 '　　 大 _ , -`.
　　 '　　　　_,'　　 _,'
　　'　　　,-'　　　_/ 爱
　 ' 大 ,-' \　　 _/　 仙
　'　 ,'　　 \　_'　　 尊
　'　'　　　 _\'　　　
　' ,　　_,-'　\　　　
　\,_,--'　　　 \　　　
"""
BRAND_NAME = "大爱仙尊专属工具版本 v1.1"
PROMPTS = [
    "请在使用本工具前，先在 CPM 游戏中登出账号！",
    "严禁分享您的访问密钥 检测到IP波动频繁封禁秘钥！",
    "独自问鼎 YDD 私信获得工具箱安装教程及使用权！"
]

# 信号处理（退出逻辑）
def signal_handler(sig, frame):
    print("\n[bold yellow]再见！感谢使用！[/bold yellow]")
    sys.exit(0)

# 颜色插值（渐变核心）
def interpolate_color(start, end, fraction):
    try:
        s = tuple(int(start.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        e = tuple(int(end.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        return "#{:02x}{:02x}{:02x}".format(*[int(s[j] + fraction*(e[j]-s[j])) for j in range(3)])
    except:
        return "#FFFFFF"

# 渐变文本生成
def gradient_text(text, start=None, end=None):
    txt = Text()
    if not start:
        start = "#{:02x}{:02x}{:02x}".format(*[random.randint(50, 230) for _ in range(3)])
        end = "#{:02x}{:02x}{:02x}".format(*[random.randint(50, 230) for _ in range(3)])
    for i, c in enumerate(text):
        color = interpolate_color(start, end, i/max(len(text)-1, 1))
        txt.append(c, style=Style(color=color))
    return txt

# 彩虹昵称格式生成
def rainbow_nickname(name):
    return ''.join([f'[{interpolate_color(
        "#{:02x}{:02x}{:02x}".format(*[random.randint(30, 220) for _ in range(3)]),
        "#{:02x}{:02x}{:02x}".format(*[random.randint(30, 220) for _ in range(3)]),
        i/max(len(name)-1, 1)
    ).lstrip("#")}]{c}' for i, c in enumerate(name)])

# 渐变分隔符
def gradient_sep(console, title="", width=40):
    title = f" {title} " if title else ""
    total = max(width, len(title)+4)
    left = (total - len(title))//2
    line = SEPARATOR_CHAR*left + title + SEPARATOR_CHAR*(total - len(title) - left)
    txt = Text()
    for i, c in enumerate(line):
        color = interpolate_color(PINK, PURPLE, i/max(len(line)-1, 1))
        txt.append(c, style=Style(color=color))
    console.print(txt)

# 横幅显示
def banner(console):
    os.system('cls' if os.name == 'nt' else 'clear')
    # 显示 ASCII 艺术
    art_colors = ["#FF0000", "#FF69B4", "#FFB6C1"]
    art_txt = Text()
    for y, line in enumerate(ASCII_ART.strip().splitlines()):
        color = art_colors[int(y/(len(ASCII_ART.strip().splitlines())-1)*(len(art_colors)-1))]
        art_txt.append(line + "\n", style=Style(color=color))
    console.print(art_txt)
    # 显示品牌和提示
    console.print(Text(BRAND_NAME, style="bold black"), justify="left")
    gradient_sep(console, "提示信息")
    for p in PROMPTS:
        console.print(gradient_text(p))
    gradient_sep(console, "结束提示")

# 玩家数据加载
def load_player_data(cpm, console):
    gradient_sep(console, "玩家信息")
    resp = cpm.get_player_data()
    if not resp.get('ok'):
        console.print(f"[bold red]获取数据失败：{resp.get('error', '未知错误')}[/bold red]")
        return False
    data = resp['data']
    keys = ['localID', 'money', 'coin', "Name", "FriendsID", "carIDnStatus"]
    if not all(k in data for k in keys) or not isinstance(data['carIDnStatus'], dict):
        console.print("[bold red]数据不完整，新账号需先登录游戏一次！[/bold red]")
        return False
    # 显示玩家信息
    info = [
        (f"昵称 (Name)   : {data['Name']}"),
        (f"ID (LocalID)  : {data['localID']}"),
        (f"绿钞 (Money)  : {data['money']}"),
        (f"金币 (Coins)  : {data['coin']}"),
        (f"好友数量      : {len(data['FriendsID'])}"),
        (f"车辆数量      : {len(set(data['carIDnStatus'].get('carGeneratedIDs', [])))}")
    ]
    for line in info:
        console.print(gradient_text(line))
    return True

# 输入验证
def prompt_valid(content, tag, console, password=False):
    while True:
        val = Prompt.ask(gradient_text(content), password=password, console=console)
        if val and not val.isspace():
            return val
        console.print(f"[bold red]{tag} 不能为空，请重新输入！[/bold red]")

# 地理位置加载
def load_client_details(console):
    gradient_sep(console, "地理位置 (估算)")
    try:
        resp = requests.get("http://ip-api.com/json", timeout=5)
        data = resp.json()
        console.print(gradient_text(f">> 国家/地区: {data.get('country', '未知')} ({data.get('countryCode', '')})"))
        console.print(gradient_text(f">> 城市     : {data.get('city', '未知')} {data.get('zip', '')}"))
    except:
        console.print("[bold yellow]无法获取地理位置信息[/bold yellow]")
    gradient_sep(console, "主菜单")

# 菜单配置
MENU_OPTIONS = [
    ("01", "修改绿钞数量 (上限 5千万)", "消耗: 1K 点数"),
    ("02", "修改金币数量 (上限 50万)", "消耗: 10K 点数"),
    ("03", "解锁皇冠成就 (156 成就)", "消耗: 30K 点数"),
    ("04", "更改玩家 ID (无空格)", "消耗: 30K 点数"),
    ("05", "更改普通昵称", "消耗: 5K 点数"),
    ("06", "更改彩虹渐变昵称", "消耗: 5K 点数"),
    ("07", "解锁自定义车牌", "消耗: 2K 点数"),
    ("08", "删除当前账号 (不可撤销)", "免费"),
    ("09", "注册新账号", "免费"),
    ("10", "清空好友列表", "消耗: 1K 点数"),
    ("11", "解锁所有付费车辆", "消耗: 5K 点数"),
    ("12", "解锁全部车辆 (含非付费)", "消耗: 10K 点数"),
    ("13", "解锁所有车辆警笛", "消耗: 3K 点数"),
    ("14", "解锁 W16 引擎", "消耗: 3K 点数"),
    ("15", "解锁所有喇叭", "消耗: 3K 点数"),
    ("16", "解锁引擎无损伤", "消耗: 3K 点数"),
    ("17", "解锁无限燃料", "消耗: 3K 点数"),
    ("18", "解锁所有付费房屋", "消耗: 4K 点数"),
    ("19", "解锁轮胎烟雾", "消耗: 4K 点数"),
    ("20", "解锁所有普通车轮", "消耗: 4K 点数"),
    ("21", "解锁所有人物动作", "消耗: 2K 点数"),
    ("22", "解锁所有男性服装", "消耗: 3K 点数"),
    ("23", "解锁所有女性服装", "消耗: 3K 点数"),
    ("24", "修改比赛胜利场数", "消耗: 10K 点数"),
    ("25", "修改比赛失败场数", "消耗: 10K 点数"),
    ("26", "克隆账号数据到另一账号", "消耗: 50K 点数"),
    ("27", "修改车辆马力/扭矩", "消耗: 5K 点数"),
    ("28", "自定义轮胎转向角度", "消耗: 5K 点数"),
    ("29", "自定义轮胎磨损度", "消耗: 3K 点数"),
    ("30", "自定义车辆行驶里程", "消耗: 3K 点数"),
    ("31", "自定义车辆刹车性能", "消耗: 2K 点数"),
    ("32", "移除车辆后保险杠", "消耗: 5K 点数"),
    ("33", "移除车辆前保险杠", "消耗: 5K 点数"),
    ("34", "强制修改当前账号密码", "消耗: 100K 点数"),
    ("35", "强制修改当前账号邮箱", "消耗: 100K 点数"),
    ("36", "自定义车辆尾翼", "消耗: 10K 点数"),
    ("37", "自定义车身套件", "消耗: 10K 点数"),
    ("38", "解锁高级/付费车轮", "消耗: 5K 点数"),
    ("39", "解锁皇冠图标车辆", "消耗: 10K 点数"),
    ("0", "退出工具箱", "")
]

if __name__ == "__main__":
    console = Console()
    signal.signal(signal.SIGINT, signal_handler)

    while True:  # 登录循环
        banner(console)

        # AccessKey 验证步骤（使用统一链接）
        gradient_sep(console, "AccessKey 验证")
        console.print(gradient_text(f"请访问以下网站获取 AccessKey：{ACCESSKEY_GET_URL}"))
        console.print(gradient_text("获取后粘贴到下方，无需手动注册！"))
        accesskey = prompt_valid("请输入 AccessKey", "AccessKey", console, password=False)

        # AccessKey 格式校验（长度≥10位）
        if len(accesskey) < 10:
            console.print("[bold red]AccessKey 格式无效（长度过短），请重新获取！[/bold red]")
            sleep(2)
            continue

        # 账号登录
        gradient_sep(console, "账号登录")
        acc_email = prompt_valid("请输入账号邮箱", "邮箱", console)
        acc_password = prompt_valid("请输入账号密码", "密码", console, password=True)

        console.print("[bold yellow][%] 正在尝试登录...", end="")

        try:
            # 初始化 Bubcyz（参数名 access_key 与 cylo.py 匹配）
            cpm = Bubcyz(access_key=accesskey)
            login_response = cpm.login(acc_email, acc_password)
        except requests.exceptions.RequestException as e:
            console.print(f"[bold red]登录失败 (网络错误 ✘)[/bold red]")
            console.print(f"[dim]错误详情: {e}[/dim]")
            sleep(3)
            continue
        except Exception as e:
            console.print(f"[bold red]登录时发生未知错误 (✘)[/bold red]")
            console.print(f"[dim]错误详情: {e}[/dim]")
            sleep(3)
            continue

        # 登录结果处理
        if login_response != 0:
            err_msg = {100: "账号未找到", 101: "密码错误"}.get(login_response, f"未知错误代码 {login_response}")
            console.print(f"[bold red]登录失败：{err_msg} (✘)[/bold red]")
            sleep(3)
            continue
        else:
            console.print("[bold green]登录成功 (✔)[/bold green]")
            sleep(1)

        # 主菜单循环
        while True:
            banner(console)
            if not load_player_data(cpm, console):
                console.print("[bold yellow]无法继续操作，请尝试重新登录！[/bold yellow]")
                sleep(3)
                break

            load_client_details(console)

            # 显示菜单表格
            menu_table = Table(show_header=False, box=None, padding=(0, 1))
            menu_table.add_column(justify="left", ratio=1, overflow="fold")
            menu_table.add_column(justify="right", style="bold red", min_width=12)
            for num, desc, cost in MENU_OPTIONS:
                left = Text()
                left.append(f"({num}) ", style="bold white")
                left.append(gradient_text(desc))
                right = Text(cost, style="bold red") if cost else Text("")
                menu_table.add_row(left, right)
            console.print(menu_table)

            gradient_sep(console, "CPM 工具箱")
            service = IntPrompt.ask(
                "[bold][?] 请选择服务项目 [red][1-39 或 0 退出][/red][/bold]",
                choices=[str(i) for i in range(40)],
                show_choices=False,
                console=console
            )

            gradient_sep(console, "操作执行")
            operation_successful = False
            exit_tool = False

            # 退出
            if service == 0:
                console.print("[bold white]感谢使用，再见！[/bold white]")
                exit_tool = True
                operation_successful = True

            # 修改绿钞
            elif service == 1:
                amount = IntPrompt.ask("[bold yellow][?] 输入绿钞数量 (1-500000000)[/bold yellow]", console=console)
                console.print("[%] 保存数据...", end="")
                if 0 < amount <= 500000000 and cpm.set_player_money(amount):
                    print("[bold green]成功 (✔)[/bold green]")
                    operation_successful = True
                else:
                    console.print("[bold red]失败 (✘)[/bold red]")

            # 修改金币
            elif service == 2:
                amount = IntPrompt.ask("[bold yellow][?] 输入金币数量 (1-500000)[/bold yellow]", console=console)
                console.print("[%] 保存数据...", end="")
                if 0 < amount <= 500000 and cpm.set_player_coins(amount):
                    print("[bold green]成功 (✔)[/bold green]")
                    operation_successful = True
                else:
                    console.print("[bold red]失败 (✘)[/bold red]")

            # 解锁类操作（整合逻辑）
            unlock_map = {
                3: ("解锁皇冠成就", cpm.set_player_rank, "[!] 请勿重复执行"),
                7: ("解锁自定义车牌", cpm.set_player_plates, None),
                10: ("清空好友列表", cpm.delete_player_friends, None),
                11: ("解锁所有付费车辆", cpm.unlock_paid_cars, "[!] 请勿中断"),
                12: ("解锁全部车辆", cpm.unlock_all_cars, None),
                13: ("解锁所有警笛", cpm.unlock_all_cars_siren, None),
                14: ("解锁 W16 引擎", cpm.unlock_w16, None),
                15: ("解锁所有喇叭", cpm.unlock_horns, None),
                16: ("解锁引擎无损伤", cpm.disable_engine_damage, None),
                17: ("解锁无限燃料", cpm.unlimited_fuel, None),
                18: ("解锁所有付费房屋", cpm.unlock_houses, None),
                19: ("解锁轮胎烟雾", cpm.unlock_smoke, None),
                20: ("解锁所有普通车轮", cpm.unlock_wheels, None),
                21: ("解锁所有人物动作", cpm.unlock_animations, None),
                22: ("解锁所有男性服装", cpm.unlock_equipments_male, None),
                23: ("解锁所有女性服装", cpm.unlock_equipments_female, None),
                38: ("解锁高级车轮", cpm.shittin, None),
                39: ("解锁皇冠图标车辆", cpm.unlock_crown, "[!] 请勿中断")
            }
            if service in unlock_map:
                name, func, note = unlock_map[service]
                if note:
                    console.print(f"[bold yellow]{note}[/bold yellow]")
                console.print(f"[%] 正在 {name}...", end="")
                if func():
                    print("[bold green]成功 (✔)[/bold green]")
                    operation_successful = True
                else:
                    console.print("[bold red]失败 (✘)[/bold red]")

            # 账号相关操作
            elif service == 8:  # 删除账号
                if Prompt.ask("[bold red][?] 确定删除账号？(y/n)[/bold red]", choices=["y", "n"], default="n") == "y":
                    console.print("[%] 删除账号...", end="")
                    cpm.delete()
                    print("[bold green]指令已发送 (✔)[/bold green]")
                    exit_tool = True
                    operation_successful = True
                else:
                    console.print("[bold yellow]操作已取消[/bold yellow]")

            elif service == 9:  # 注册新账号
                new_email = prompt_valid("[?] 新账号邮箱", "邮箱", console)
                new_pwd = prompt_valid("[?] 新账号密码", "密码", console, password=True)
                console.print("[%] 创建账号...", end="")
                status = cpm.register(new_email, new_pwd)
                if status == 0:
                    print("[bold green]成功 (✔)[/bold green]")
                    console.print("[bold yellow]新账号需先登录游戏一次！[/bold yellow]")
                    operation_successful = True
                elif status == 105:
                    console.print("[bold red]邮箱已注册 (✘)[/bold red]")
                else:
                    console.print(f"[bold red]错误代码 {status} (✘)[/bold red]")

            # 昵称/ID 修改
            elif service == 4:  # 更改 ID
                new_id = prompt_valid("[?] 新 ID (无空格)", "ID", console)
                if ' ' in new_id:
                    console.print("[bold red]ID 不能包含空格 (✘)[/bold red]")
                else:
                    console.print("[%] 保存数据...", end="")
                    if cpm.set_player_localid(new_id.upper()):
                        print("[bold green]成功 (✔)[/bold green]")
                        operation_successful = True
                    else:
                        console.print("[bold red]失败 (✘)[/bold red]")

            elif service == 5:  # 普通昵称
                new_name = prompt_valid("[?] 新昵称", "昵称", console)
                console.print("[%] 保存数据...", end="")
                if cpm.set_player_name(new_name):
                    print("[bold green]成功 (✔)[/bold green]")
                    operation_successful = True
                else:
                    console.print("[bold red]失败 (✘)[/bold red]")

            elif service == 6:  # 彩虹昵称
                new_name = prompt_valid("[?] 基础昵称", "昵称", console)
                console.print("[%] 生成渐变并保存...", end="")
                if cpm.set_player_name(rainbow_nickname(new_name)):
                    print("[bold green]成功 (✔)[/bold green]")
                    operation_successful = True
                else:
                    console.print("[bold red]失败 (✘)[/bold red]")

            # 比赛场数修改
            elif service in [24, 25]:
                field = "胜利" if service == 24 else "失败"
                func = cpm.set_player_wins if service == 24 else cpm.set_player_loses
                amount = IntPrompt.ask(f"[bold yellow][?] 输入{field}场数[/bold yellow]", console=console)
                console.print(f"[%] 修改{field}场数...", end="")
                if amount >= 0 and func(amount):
                    print("[bold green]成功 (✔)[/bold green]")
                    operation_successful = True
                else:
                    console.print("[bold red]失败 (✘)[/bold red]")

            # 账号克隆
            elif service == 26:
                to_email = prompt_valid("[?] 目标账号邮箱", "邮箱", console)
                to_pwd = prompt_valid("[?] 目标账号密码", "密码", console, password=True)
                console.print("[%] 克隆数据...", end="")
                if cpm.account_clone(to_email, to_pwd):
                    print("[bold green]成功 (✔)[/bold green]")
                    console.print("[bold yellow]目标账号数据可能已覆盖！[/bold yellow]")
                    operation_successful = True
                else:
                    console.print("[bold red]失败 (✘)[/bold red]")

            # 车辆性能修改
            elif service == 27:
                car_id = IntPrompt.ask("[?] 车辆 ID", console=console)
                hp = IntPrompt.ask("[?] 新马力", console=console)
                inner_hp = IntPrompt.ask("[?] 新内部马力", console=console)
                nm = IntPrompt.ask("[?] 新牛米", console=console)
                torque = IntPrompt.ask("[?] 新扭矩", console=console)
                console.print("[%] 修改性能...", end="")
                if all(val >= 0 for val in [car_id, hp, inner_hp, nm, torque]) and cpm.hack_car_speed(car_id, hp, inner_hp, nm, torque):
                    print("[bold green]成功 (✔)[/bold green]")
                    operation_successful = True
                else:
                    console.print("[bold red]失败 (✘)[/bold red]")

            # 车辆自定义操作
            car_custom_map = {
                28: ("转向角度", cpm.max_max1),
                29: ("磨损度", cpm.max_max2),
                30: ("行驶里程", cpm.millage_car),
                31: ("刹车性能", cpm.brake_car),
                36: ("尾翼 ID", cpm.telmunnongodz),
                37: ("车身套件 ID", cpm.telmunnongonz)
            }
            if service in car_custom_map:
                name, func = car_custom_map[service]
                car_id = IntPrompt.ask(f"[?] 车辆 ID (修改{name})", console=console)
                val = IntPrompt.ask(f"[?] 新{name}值", console=console)
                console.print(f"[%] 设置车辆{name}...", end="")
                if car_id >= 0 and val >= 0 and func(car_id, val):
                    print("[bold green]成功 (✔)[/bold green]")
                    operation_successful = True
                else:
                    console.print("[bold red]失败 (✘)[/bold red]")

            # 保险杠移除
            elif service in [32, 33]:
                typ = "后" if service == 32 else "前"
                func = cpm.rear_bumper if service == 32 else cpm.front_bumper
                car_id = IntPrompt.ask(f"[?] 车辆 ID (移除{typ}保险杠)", console=console)
                console.print(f"[%] 移除{typ}保险杠...", end="")
                if car_id >= 0 and func(car_id):
                    print("[bold green]成功 (✔)[/bold green]")
                    operation_successful = True
                else:
                    console.print("[bold red]失败 (✘)[/bold red]")

            # 密码/邮箱修改
            elif service == 34:
                new_pwd = prompt_valid("[?] 新密码", "密码", console, password=True)
                console.print("[%] 修改密码...", end="")
                if cpm.change_password(new_pwd):
                    print("[bold green]成功 (✔)[/bold green]")
                    console.print("[bold yellow]请用新密码重新登录！[/bold yellow]")
                    exit_tool = True
                    operation_successful = True
                else:
                    console.print("[bold red]失败 (✘)[/bold red]")

            elif service == 35:
                new_email = prompt_valid("[?] 新邮箱", "邮箱", console)
                if '@' not in new_email or '.' not in new_email.split('@')[-1]:
                    console.print("[bold red]邮箱格式无效 (✘)[/bold red]")
                else:
                    console.print("[%] 修改邮箱...", end="")
                    if cpm.change_email(new_email):
                        print("[bold green]成功 (✔)[/bold green]")
                        console.print("[bold yellow]请用新邮箱重新登录！[/bold yellow]")
                        break
                    else:
                        console.print("[bold red]失败 (✘)[/bold red]")

            # 操作后处理
            gradient_sep(console)
            if exit_tool:
                break
            if operation_successful:
                if Prompt.ask("[?] 返回主菜单？(y/n)", choices=["y", "n"], default="y") == "n":
                    console.print("[bold white]感谢使用，再见！[/bold white]")
                    sys.exit(0)
            else:
                console.print("[bold yellow]按回车键返回主菜单...[/bold yellow]")
                input()