#!/usr/bin/python
# -*- coding: utf-8 -*- # 优化编码支持，避免中文乱码

import random
import urllib.parse
import requests
from time import sleep
import os, signal, sys
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.text import Text
from rich.style import Style
from rich.table import Table

# 导入无密钥版 Bubcyz 类
try:
    from cylo import Bubcyz
except ImportError:
    print("[错误] 找不到无密钥版 cylo.py 文件，请确保两者在同一目录！")
    sys.exit(1)

# --- 配色与分隔符优化 ---
PINK = "#FF69B4"  # 亮粉色，视觉更醒目
PURPLE = "#9932CC" # 深紫色，提升渐变质感
SEPARATOR_CHAR = '◆' # 替换分隔符，更具辨识度
# --- 标识替换：季伯常 → YDD大魔王 ---
ascii_art_ydd = r"""
　  　\.　-　 -　.　　
　　　 '　　 魔　 _ , -`.
　　 '　　　　_,'　　 _,'
　　'　　　,-'　　　_/ 快
　 ' 爱 ,-' \　　 _/　 手
　'　 ,'　　 \　_'　　 搜
　'　'　　　 _\'　　　 Y
　' ,　　_,-'　\　　　 D
　\,_,--'　　　 \　　　 D
"""
# --- 结束标识替换 ---

def signal_handler(sig, frame):
    """优化退出信号，增加优雅提示"""
    print("\n[bold yellow]感谢使用 YDD大魔王 工具箱！再见！[/bold yellow]")
    sys.exit(0)

def interpolate_color(start_color, end_color, fraction):
    """优化颜色插值算法，减少颜色失真"""
    try:
        start_rgb = tuple(int(start_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        end_rgb = tuple(int(end_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        interpolated_rgb = tuple(int(start + fraction * (end - start)) for start, end in zip(start_rgb, end_rgb))
        interpolated_rgb = tuple(max(0, min(255, val)) for val in interpolated_rgb)
        return "#{:02x}{:02x}{:02x}".format(*interpolated_rgb)
    except ValueError:
        return "#FFFFFF"

def random_gradient_text_line_rich(text):
    """优化渐变文字生成，提升颜色过渡自然度"""
    modified_text = Text()
    num_chars = len(text)
    if num_chars == 0:
        return modified_text

    # 固定颜色区间，避免出现过暗/过亮文字
    start_rgb = [random.randint(80, 220) for _ in range(3)]
    end_rgb = [random.randint(80, 220) for _ in range(3)]

    start_color = "#{:02x}{:02x}{:02x}".format(*start_rgb)
    end_color = "#{:02x}{:02x}{:02x}".format(*end_rgb)

    for i, char in enumerate(text):
        fraction = i / max(num_chars - 1, 1)
        interpolated_color = interpolate_color(start_color, end_color, fraction)
        modified_text.append(char, style=Style(color=interpolated_color))
    return modified_text

def rainbow_gradient_string_cpm_format(customer_name):
    """优化彩虹昵称生成，适配游戏内显示规则"""
    modified_string = ""
    num_chars = len(customer_name)
    start_rgb = [random.randint(50, 200) for _ in range(3)]
    end_rgb = [random.randint(50, 200) for _ in range(3)]
    start_color = "#{:02x}{:02x}{:02x}".format(*start_rgb)
    end_color = "#{:02x}{:02x}{:02x}".format(*end_rgb)

    for i, char in enumerate(customer_name):
        fraction = i / max(num_chars - 1, 1)
        interpolated_hex = interpolate_color(start_color, end_color, fraction).lstrip('#')
        modified_string += f'[{interpolated_hex}]{char}'
    return modified_string

def gradient_text_multi_line(text, colors):
    """优化多行文字渐变，提升显示一致性"""
    lines = text.strip('\n').splitlines()
    if not lines:
        return Text()
    height = len(lines)

    colorful_text = Text()
    for y, line in enumerate(lines):
        fraction_y = y / (height - 1) if height > 1 else 0
        color_index = int(fraction_y * (len(colors) - 1))
        color_index = min(max(color_index, 0), len(colors) - 1)
        style = Style(color=colors[color_index])
        colorful_text.append(line, style=style)
        if y < len(lines) - 1:
             colorful_text.append("\n")
    return colorful_text

def gradient_separator(title, console, separator_char=SEPARATOR_CHAR, total_width=45, start_color=PINK, end_color=PURPLE):
    """优化分隔符样式，加宽宽度提升美观度"""
    title_text_str = f" {title} " if title else ""
    title_width = len(title_text_str)
    actual_total_width = max(total_width, title_width + 4)
    separator_space = actual_total_width - title_width
    left_len = separator_space // 2
    right_len = separator_space - left_len

    full_line_chars = (separator_char * left_len) + title_text_str + (separator_char * right_len)
    separator_line_text = Text()
    num_chars_in_line = len(full_line_chars)

    for i, char in enumerate(full_line_chars):
        fraction_x = i / max(num_chars_in_line - 1, 1)
        interpolated_color = interpolate_color(start_color, end_color, fraction_x)
        style = Style(color=interpolated_color)
        separator_line_text.append(char, style=style)
    console.print(separator_line_text)

def banner(console):
    """优化横幅显示，替换所有标识为 YDD大魔王"""
    os.system('cls' if os.name == 'nt' else 'clear')
    # 彩虹渐变艺术字
    art_colors = ["#FF0000", "#FF69B4", "#9932CC"]
    colored_art = gradient_text_multi_line(ascii_art_ydd.strip(), art_colors)
    console.print(colored_art)
    console.print("\n")
    # 版本标题
    brand_name = "YDD大魔王专属工具版本 v2.0 [无密钥免费版]"
    text = Text(brand_name, style="bold black")
    console.print(text, justify="left")
    # 提示信息
    gradient_separator("提示信息", console)
    console.print(random_gradient_text_line_rich("请在使用本工具前，先在 CPM 游戏中登出账号！"))
    console.print(random_gradient_text_line_rich("本版本为免费无密钥版，全功能开放无限制！"))
    console.print(random_gradient_text_line_rich("快手搜 YDD大魔王 私信获得工具箱安装教程！"))
    gradient_separator("结束提示", console)

def load_player_data(cpm, console):
    """优化玩家数据加载，增加异常容错"""
    gradient_separator("玩家信息", console)
    response = cpm.get_player_data()
    if response.get('ok'):
        data = response.get('data', {})
        required_keys = ['localID', 'money', 'coin', "Name", "FriendsID", "carIDnStatus"]
        missing_keys = [key for key in required_keys if key not in data]
        if not missing_keys and isinstance(data.get('carIDnStatus'), dict):
            console.print(random_gradient_text_line_rich(f">> 昵称 (Name)   : {data.get('Name', '未定义')}"))
            console.print(random_gradient_text_line_rich(f">> ID (LocalID)  : {data.get('localID', '未定义')}"))
            console.print(random_gradient_text_line_rich(f">> 绿钞 (Money)  : {data.get('money', '未定义')}"))
            console.print(random_gradient_text_line_rich(f">> 金币 (Coins)  : {data.get('coin', '未定义')}"))
            friends_count = len(data.get("FriendsID", []))
            console.print(random_gradient_text_line_rich(f">> 好友数量      : {friends_count}"))
            car_list = data.get("carIDnStatus", {}).get("carGeneratedIDs", [])
            unique_car_list = set(car_list)
            car_count = len(unique_car_list)
            console.print(random_gradient_text_line_rich(f">> 车辆数量      : {car_count}"))
            return True
        else:
            error_msg = "[bold red] ! 错误：无法加载完整的玩家数据。"
            if missing_keys:
                error_msg += f" 缺少键: {', '.join(missing_keys)}。"
            error_msg += " 新账号必须至少登录一次游戏才能生成数据 (✘)[/bold red]"
            console.print(error_msg)
            return False
    else:
        error_detail = response.get('error', '未知错误')
        console.print(f"[bold red] ! 错误：获取玩家数据失败。原因: {error_detail} (✘)[/bold red]")
        console.print("[bold yellow]   请检查您的网络连接和登录凭据是否正确。[/bold yellow]")
        return False

def load_key_data(cpm, console):
    """优化版本信息展示，突出免费属性"""
    gradient_separator("版本信息", console)
    console.print(random_gradient_text_line_rich(">> 版本类型 : YDD大魔王 无密钥免费版"))
    console.print(random_gradient_text_line_rich(">> 功能限制 : 全功能开放，无任何点数消耗"))
    console.print(random_gradient_text_line_rich(">> 适配环境 : iSH 终端 / Windows 命令行"))

def prompt_valid_value(content, tag, console, password=False):
    """优化输入验证，增加空格过滤"""
    gradient_content = random_gradient_text_line_rich(content)
    while True:
        value = Prompt.ask(gradient_content, password=password, console=console).strip()
        if not value:
            console.print(f"[bold red]输入错误：{tag} 不能为空，请重新输入 (✘)[/bold red]")
        else:
            return value

def load_client_details(console):
    """优化地理位置获取，增加超时容错"""
    try:
        response = requests.get("http://ip-api.com/json", timeout=3)
        response.raise_for_status()
        data = response.json()
        gradient_separator("地理位置 (估算)", console)
        console.print(random_gradient_text_line_rich(f">> 国家/地区: {data.get('country', '未知')} ({data.get('countryCode', '')})"))
        console.print(random_gradient_text_line_rich(f">> 城市     : {data.get('city', '未知')} {data.get('zip', '')}"))
    except requests.exceptions.RequestException:
        console.print("[bold yellow] ! 警告：无法获取地理位置信息，不影响工具使用。[/bold yellow]")
    finally:
        gradient_separator("主菜单", console)

if __name__ == "__main__":
    """主程序入口，优化逻辑流程，提升稳定性"""
    console = Console()
    signal.signal(signal.SIGINT, signal_handler)

    while True: # 登录循环
        banner(console)
        # 账号密码输入（移除密钥输入）
        gradient_separator("账号登录", console)
        acc_email = prompt_valid_value("请输入账号邮箱", "邮箱", console)
        acc_password = prompt_valid_value("请输入账号密码", "密码", console)

        console.print("[bold yellow][%] 正在尝试登录...", end="")
        try:
            cpm = Bubcyz()
            login_response = cpm.login(acc_email, acc_password)
        except requests.exceptions.RequestException as e:
            console.print(f"[bold red]登录失败 (网络错误 ✘)[/bold red]")
            console.print(f"[dim]   错误详情: {e}[/dim]")
            sleep(3)
            continue
        except Exception as e:
             console.print(f"[bold red]登录时发生未知错误 (✘)[/bold red]")
             console.print(f"[dim]   错误详情: {e}[/dim]")
             sleep(3)
             continue

        # 登录结果判断（移除密钥错误码）
        if login_response != 0:
            error_map = {
                100: "账号未找到",
                101: "密码错误"
            }
            err_msg = error_map.get(login_response, f"未知错误代码 {login_response}")
            console.print(f"[bold red]登录失败：{err_msg} (✘)[/bold red]")
            sleep(3)
            continue
        else:
            console.print("[bold green]登录成功 (✔)[/bold green]")
            sleep(1)

        # --- 主菜单循环 ---
        while True:
            banner(console)
            if not load_player_data(cpm, console):
                console.print("[bold yellow]无法继续操作，请尝试重新登录。[/bold yellow]")
                sleep(3)
                break

            load_key_data(cpm, console)
            load_client_details(console)

            # 优化菜单选项，排版更清晰
            menu_options_data = [
                ("01", "修改绿钞数量 (上限 5千万)", "免费"),
                ("02", "修改金币数量 (上限 50万)", "免费"),
                ("03", "解锁皇冠成就 (156 成就)", "免费"),
                ("04", "更改玩家 ID (无空格限制)", "免费"),
                ("05", "更改普通昵称", "免费"),
                ("06", "更改彩虹渐变昵称", "免费"),
                ("07", "解锁自定义车牌", "免费"),
                ("08", "删除当前账号 (不可撤销)", "免费"),
                ("09", "注册新账号", "免费"),
                ("10", "清空好友列表", "免费"),
                ("11", "解锁所有付费车辆", "免费"),
                ("12", "解锁全部车辆 (含非付费)", "免费"),
                ("13", "解锁所有车辆警笛", "免费"),
                ("14", "解锁 W16 引擎", "免费"),
                ("15", "解锁所有喇叭", "免费"),
                ("16", "解锁引擎无损伤", "免费"),
                ("17", "解锁无限燃料", "免费"),
                ("18", "解锁所有付费房屋", "免费"),
                ("19", "解锁轮胎烟雾", "免费"),
                ("20", "解锁所有普通车轮", "免费"),
                ("21", "解锁所有人物动作", "免费"),
                ("22", "解锁所有男性服装", "免费"),
                ("23", "解锁所有女性服装", "免费"),
                ("24", "修改比赛胜利场数", "免费"),
                ("25", "修改比赛失败场数", "免费"),
                ("26", "克隆账号数据到另一账号", "免费"),
                ("27", "修改车辆马力/扭矩", "免费"),
                ("28", "自定义轮胎转向角度", "免费"),
                ("29", "自定义轮胎磨损度", "免费"),
                ("30", "自定义车辆行驶里程", "免费"),
                ("31", "自定义车辆刹车性能", "免费"),
                ("32", "移除车辆后保险杠", "免费"),
                ("33", "移除车辆前保险杠", "免费"),
                ("34", "强制修改账号密码", "免费"),
                ("35", "强制修改账号邮箱", "免费"),
                ("36", "自定义车辆尾翼", "免费"),
                ("37", "自定义车身套件", "免费"),
                ("38", "解锁高级/付费车轮", "免费"),
                ("39", "解锁皇冠图标车辆", "免费"),
                ("0", "退出工具箱", ""),
            ]

            # 菜单表格优化
            menu_table = Table(show_header=False, box=None, padding=(0, 2))
            menu_table.add_column(justify="left", style="default", ratio=2)
            menu_table.add_column(justify="right", style="bold green", min_width=8)
            for num, desc, cost in menu_options_data:
                left_cell = Text()
                left_cell.append(f"({num}) ", style="bold white")
                left_cell.append(random_gradient_text_line_rich(desc))
                right_cell = Text(cost, style="bold green") if cost else Text()
                menu_table.add_row(left_cell, right_cell)
            console.print(menu_table)
            gradient_separator("CPM 工具箱", console)

            # 用户选择
            service = IntPrompt.ask(
                "[bold][?] 请选择服务项目 [red][1-39 或 0 退出][/red][/bold]",
                choices=[str(i) for i in range(0, 40)],
                show_choices=False,
                console=console
            )
            gradient_separator("操作执行", console)
            operation_successful = False
            exit_tool = False

            # --- 功能逻辑（优化冗余代码，保留核心功能）---
            if service == 0:
                console.print("[bold white] 感谢使用 YDD大魔王 工具箱！再见！[/bold white]")
                exit_tool = True
                operation_successful = True

            elif service == 1:
                console.print("[bold yellow][?] 请输入绿钞数量 (最大 500000000)[/bold yellow]")
                amount = IntPrompt.ask("[?] 数量", console=console)
                console.print("[%] 正在保存数据...", end="")
                if 0 < amount <= 500000000:
                    if cpm.set_player_money(amount):
                        print("[bold green]成功 (✔)[/bold green]")
                        operation_successful = True
                    else:
                        console.print("[bold red]失败 (✘)[/bold red]")
                else:
                    console.print("[bold red]输入无效 (✘)[/bold red]")

            elif service == 2:
                console.print("[bold yellow][?] 请输入金币数量 (最大 500000)[/bold yellow]")
                amount = IntPrompt.ask("[?] 数量", console=console)
                console.print("[%] 正在保存数据...", end="")
                if 0 < amount <= 500000:
                    if cpm.set_player_coins(amount):
                        print("[bold green]成功 (✔)[/bold green]")
                        operation_successful = True
                    else:
                        console.print("[bold red]失败 (✘)[/bold red]")
                else:
                    console.print("[bold red]输入无效 (✘)[/bold red]")

            elif service == 3:
                console.print("[bold red][!] 提示: 游戏内未显示请重新登录[/bold red]")
                sleep(1)
                console.print("[%] 正在解锁皇冠成就...", end="")
                if cpm.set_player_rank():
                    print("[bold green]成功 (✔)[/bold green]")
                    operation_successful = True
                else:
                    console.print("[bold red]失败 (✘)[/bold red]")

            elif service == 4:
                new_id = prompt_valid_value("[?] 请输入新 ID (无空格)", "ID", console)
                console.print("[%] 正在保存数据...", end="")
                if ' ' not in new_id:
                    if cpm.set_player_localid(new_id.upper()):
                        print("[bold green]成功 (✔)[/bold green]")
                        operation_successful = True
                    else:
                        console.print("[bold red]失败 (✘)[/bold red]")
                else:
                    console.print("[bold red]ID 不能包含空格 (✘)[/bold red]")

            elif service == 5:
                new_name = prompt_valid_value("[?] 请输入新昵称", "昵称", console)
                console.print("[%] 正在保存数据...", end="")
                if cpm.set_player_name(new_name):
                    print("[bold green]成功 (✔)[/bold green]")
                    operation_successful = True
                else:
                    console.print("[bold red]失败 (✘)[/bold red]")

            elif service == 6:
                new_name = prompt_valid_value("[?] 请输入基础昵称", "基础昵称", console)
                console.print("[%] 生成渐变昵称...", end="")
                rainbow_name = rainbow_gradient_string_cpm_format(new_name)
                if cpm.set_player_name(rainbow_name):
                    print("[bold green]成功 (✔)[/bold green]")
                    operation_successful = True
                else:
                    console.print("[bold red]失败 (✘)[/bold red]")

            elif service == 7:
                console.print("[%] 解锁自定义车牌...", end="")
                if cpm.set_player_plates():
                    print("[bold green]成功 (✔)[/bold green]")
                    operation_successful = True
                else:
                    console.print("[bold red]失败 (✘)[/bold red]")

            elif service == 8:
                answ = Prompt.ask("[bold red][?] 确定删除账号？(y/n)[/bold red]", choices=["y", "n"], default="n")
                if answ == "y":
                    cpm.delete()
                    print("[bold green]账号删除指令已发送 (✔)[/bold green]")
                    exit_tool = True
                    operation_successful = True
                else:
                    console.print("[bold yellow]操作已取消[/bold yellow]")

            elif service == 9:
                new_email = prompt_valid_value("[?] 新账号邮箱", "邮箱", console)
                new_pwd = prompt_valid_value("[?] 新账号密码", "密码", console, password=True)
                console.print("[%] 注册新账号...", end="")
                status = cpm.register(new_email, new_pwd)
                if status == 0:
                    print("[bold green]成功 (✔)[/bold green]")
                    operation_successful = True
                elif status == 105:
                    console.print("[bold red]邮箱已被注册 (✘)[/bold red]")
                else:
                    console.print("[bold red]注册失败 (✘)[/bold red]")

            elif service == 10:
                console.print("[%] 清空好友列表...", end="")
                if cpm.delete_player_friends():
                    print("[bold green]成功 (✔)[/bold green]")
                    operation_successful = True
                else:
                    console.print("[bold red]失败 (✘)[/bold red]")

            # --- 解锁类功能批量处理 ---
            unlock_actions = {
                11: (cpm.unlock_paid_cars, "所有付费车辆"),
                12: (cpm.unlock_all_cars, "全部车辆"),
                13: (cpm.unlock_all_cars_siren, "所有车辆警笛"),
                14: (cpm.unlock_w16, "W16 引擎"),
                15: (cpm.unlock_horns, "所有喇叭"),
                16: (cpm.disable_engine_damage, "引擎无损伤"),
                17: (cpm.unlimited_fuel, "无限燃料"),
                18: (cpm.unlock_houses, "所有付费房屋"),
                19: (cpm.unlock_smoke, "轮胎烟雾"),
                20: (cpm.unlock_wheels, "所有普通车轮"),
                21: (cpm.unlock_animations, "所有人物动作"),
                22: (cpm.unlock_equipments_male, "所有男性服装"),
                23: (cpm.unlock_equipments_female, "所有女性服装"),
                38: (cpm.shittin, "高级/付费车轮"),
                39: (cpm.unlock_crown, "皇冠图标车辆")
            }
            if service in unlock_actions:
                func, desc = unlock_actions[service]
                console.print(f"[%] 解锁 {desc}...", end="")
                if func():
                    print("[bold green]成功 (✔)[/bold green]")
                    operation_successful = True
                else:
                    console.print("[bold red]失败 (✘)[/bold red]")

            # --- 胜负场数修改 ---
            elif service in [24, 25]:
                field = "胜利" if service == 24 else "失败"
                func = cpm.set_player_wins if service == 24 else cpm.set_player_loses
                amount = IntPrompt.ask(f"[?] 请输入{field}场数", console=console)
                console.print(f"[%] 修改{field}场数...", end="")
                if amount >= 0 and func(amount):
                    print("[bold green]成功 (✔)[/bold green]")
                    operation_successful = True
                else:
                    console.print("[bold red]失败 (✘)[/bold red]")

            # --- 账号克隆 ---
            elif service == 26:
                to_email = prompt_valid_value("[?] 目标账号邮箱", "邮箱", console)
                to_pwd = prompt_valid_value("[?] 目标账号密码", "密码", console, password=True)
                console.print("[%] 克隆账号数据...", end="")
                if cpm.account_clone(to_email, to_pwd):
                    print("[bold green]成功 (✔)[/bold green]")
                    operation_successful = True
                else:
                    console.print("[bold red]失败 (✘)[/bold red]")

            # --- 车辆性能修改 ---
            elif service == 27:
                car_id = IntPrompt.ask("[?] 车辆 ID", console=console)
                hp = IntPrompt.ask("[?] 新马力", console=console)
                inner_hp = IntPrompt.ask("[?] 内部马力", console=console)
                nm = IntPrompt.ask("[?] 牛米", console=console)
                torque = IntPrompt.ask("[?] 扭矩", console=console)
                console.print("[%] 修改车辆性能...", end="")
                if all(val >= 0 for val in [car_id, hp, inner_hp, nm, torque]):
                    if cpm.hack_car_speed(car_id, hp, inner_hp, nm, torque):
                        print("[bold green]成功 (✔)[/bold green]")
                        operation_successful = True
                    else:
                        console.print("[bold red]失败 (✘)[/bold red]")
                else:
                    console.print("[bold red]数值不能为负 (✘)[/bold red]")

            # --- 车辆自定义属性 ---
            car_custom = {
                28: (cpm.max_max1, "轮胎转向角度"),
                29: (cpm.max_max2, "轮胎磨损度"),
                30: (cpm.millage_car, "行驶里程"),
                31: (cpm.brake_car, "刹车性能"),
                36: (cpm.telmunnongodz, "车辆尾翼"),
                37: (cpm.telmunnongonz, "车身套件")
            }
            if service in car_custom:
                func, desc = car_custom[service]
                car_id = IntPrompt.ask(f"[?] 车辆 ID ({desc})", console=console)
                val = IntPrompt.ask(f"[?] {desc}数值", console=console)
                console.print(f"[%] 设置{desc}...", end="")
                if car_id >= 0 and val >= 0 and func(car_id, val):
                    print("[bold green]成功 (✔)[/bold green]")
                    operation_successful = True
                else:
                    console.print("[bold red]失败 (✘)[/bold red]")

            # --- 保险杠移除 ---
            elif service in [32, 33]:
                b_type = "后" if service == 32 else "前"
                func = cpm.rear_bumper if service == 32 else cpm.front_bumper
                car_id = IntPrompt.ask(f"[?] 车辆 ID (移除{b_type}保险杠)", console=console)
                console.print(f"[%] 移除{b_type}保险杠...", end="")
                if car_id >= 0 and func(car_id):
                    print("[bold green]成功 (✔)[/bold green]")
                    operation_successful = True
                else:
                    console.print("[bold red]失败 (✘)[/bold red]")

            # --- 密码修改 ---
            elif service == 34:
                new_pwd = prompt_valid_value("[?] 新密码", "密码", console, password=True)
                console.print("[%] 修改密码...", end="")
                if cpm.change_password(new_pwd):
                    print("[bold green]成功 (✔)[/bold green]")
                    exit_tool = True
                    operation_successful = True
                else:
                    console.print("[bold red]失败 (✘)[/bold red]")

            # --- 邮箱修改 ---
            elif service == 35:
                new_email = prompt_valid_value("[?] 新邮箱", "邮箱", console)
                if '@' in new_email and '.' in new_email.split('@')[-1]:
                    console.print("[%] 修改邮箱...", end="")
                    if cpm.change_email(new_email):
                        print("[bold green]成功 (✔)[/bold green]")
                        break
                    else:
                        console.print("[bold red]失败 (✘)[/bold red]")
                else:
                    console.print("[bold red]邮箱格式无效 (✘)[/bold red]")

            # --- 操作完成处理 ---
            if operation_successful and not exit_tool:
                gradient_separator("", console)
                answ = Prompt.ask("[?] 操作完成，返回主菜单？(y/n)", choices=["y", "n"], default="y")
                if answ == "n":
                    exit_tool = True
            elif not operation_successful and service not in [0, 8, 9]:
                gradient_separator("", console)
                console.print("[bold yellow] 按回车键返回主菜单...[/bold yellow]")
                input()
            if exit_tool:
                break
        if exit_tool:
            break