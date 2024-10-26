import asyncio
import os  # 添加这行
from nonebot import on_command, on_message, get_bot  # 添加 get_bot
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment, Bot
from nonebot.adapters.onebot.v11.permission import GROUP, GROUP_ADMIN, GROUP_OWNER
from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata
from nonebot import require, get_driver
from nonebot.rule import keyword
from nonebot.params import EventPlainText  # 添加这行导入
import aiohttp
import time
from datetime import datetime
from pathlib import Path
from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler

from .config import plugin_config
from .data_source import (
    live_db, 
    get_live_info_by_uid, 
    get_live_info,  # 添加这个导入
    generate_qrcode, 
    check_qrcode_status, 
    NeedLoginError, 
    RateLimitError,  # 添加这个导入
    Credential
)
from .models import SubscriptionInfo

__plugin_meta__ = PluginMetadata(
    name="直播订阅",
    description="B站直播订阅通知插件",
    usage="""
    指令:
      直播订阅帮助 - 显示详细帮助信息
      订阅直播 [房间号] - 订指定直播间
      取消订阅 [间号] - 取消订阅指定直播间
      订阅列表 - 查看当前群订阅的直播间
      订阅设置 - 管理通知设置
      订阅管理 - 管理订阅管理员
    """,
)

sub = on_command(
    "订阅直播",
    # 需要是群管理员或更高权限
    permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER,
    priority=5,
    block=True
)
unsub = on_command(
    "取消订阅",
    # 需要是群管理员或更高权限
    permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER,
    priority=5,
    block=True
)
sub_list = on_command("订阅列表", permission=GROUP, priority=5, block=True)

# 添加新的命令
admin_cmd = on_command("订阅管理", permission=GROUP, priority=5, block=True)

# 添加管理员列表命令
admin_list = on_command(
    "管理员列表",
    aliases={"订阅管员", "订阅管理列表"},
    permission=GROUP,
    priority=5,
    block=True
)

# 修改帮助命令定义，只保留一个命令名
help_cmd = on_command(
    "bilihelp",
    permission=GROUP,
    priority=1,
    block=True
)

@help_cmd.handle()
async def handle_help(bot: Bot, event: GroupMessageEvent):
    # 判断用户权限
    is_super_admin = event.user_id in plugin_config.live_super_admins
    is_admin = await check_admin(event)  # 修改这里，使用 check_admin 函数
    
    # 基础命令部分
    base_commands = (
        "🔰 基础命令：\n"
    )
    if is_admin:  # 修改这里，只要是管理员就显示
        base_commands += (
            "  订阅直播 [UID] - 订阅指定UP主的直播间（限管理员）\n"
            "  取消订阅 - 显示订阅列表并通过序号取消订阅（限管理员）\n"
        )
    base_commands += "  订阅列表 - 查看当前群订阅的直播间\n"
    
    # 管理命令部分
    admin_commands = "👥 管理命令：\n"
    if is_super_admin:  # 只有全局管理员能看到这些命令
        admin_commands += (
            "  订阅管理 添加管理 @用户 - 添加订阅管理员（限全局管理）\n"
            "  订阅管理 移除管理 @用户 - 移除订阅管理员（限全局管理）\n"
            "  账号状态 - 查看B站账号登录状态（限全局管理）\n"
            "  重新登录 - 更新B站账号Cookie（限全局管理）\n"
            "  截图 - 查看正在直播的主播并获取截图（限全局管理）\n"
        )
    admin_commands += "  管理员列 - 查看当前群的订阅管理员\n"
    
    # 通知内容分
    notification_info = (
        "📝 通知内容包括：\n"
        "• 主播开播提醒（标题、分区、粉丝数等）\n"
        "• 直播间标题更新提醒\n"
        "• 播提醒\n"
        "• 直播分区信息\n"
        "• 粉丝数据统计\n"
        "• 直播间标签\n"
    )
    
    # 注意事项部分
    notes = (
        "❗ 注意事项：\n"
        "1. 订阅命令使用UP主的UID（在UP主空间链接中获取）\n"
    )
    if is_admin:  # 修改这里，只要是管理员就显示
        notes += "2. 需要群管理员权限才能订阅和取消订阅\n"
    else:
        notes += "2. 请联系群管理员进行订阅和取消订阅操作\n"
    notes += (
        "3. 首次使用需要扫码登录以获取完整功能\n"
        "4. Cookie有效期有限，失效时需要重新登录\n"
    )
    
    # 权限信息部分
    if is_super_admin:
        permission_info = (
            "\n🔑 权限说明：\n"
            "您是全局管理员，可以使用所有功能"
        )
    elif is_admin:
        permission_info = (
            "\n🔑 权限说明：\n"
            "您是订阅管理员，可以管理订阅"
        )
    else:
        permission_info = (
            "\n🔑 权限说明：\n"
            "您是普通成员，可以查看订阅列表"
        )
    
    # 全局管理员列表（只对管理员显示）
    admin_list = ""
    if is_admin:  # 修改这里，使用 is_admin 而不是 is_group_admin
        admin_list = (
            "\n👑 全局管理员：\n" +
            "\n".join(f"• {admin}" for admin in plugin_config.live_super_admins)
        )
    
    # 组合完整帮助文本
    help_text = (
        "📺 B站直播订阅系统 使用帮助\n\n" +
        base_commands + "\n" +
        admin_commands + "\n" +
        notification_info + "\n" +
        notes +
        permission_info +
        admin_list
    )

    try:
        await bot.send_group_msg(
            group_id=event.group_id,
            message=Message(help_text)
        )
    except Exception as e:
        print(f"发送帮助信息失败：{e}")

# 权限检查函数
async def check_admin(event: GroupMessageEvent) -> bool:
    """检查是否是管理员
    只检查全局管理员和被添加的管理员，不检查群管理员
    """
    group_str = str(event.group_id)
    user_id = event.user_id
    return (
        user_id in plugin_config.live_super_admins or
        user_id in live_db._data.get(group_str, SubscriptionInfo(group_id=event.group_id)).admin_users
    )

@sub.handle()
async def handle_sub(bot: Bot, event: GroupMessageEvent):
    # 修改权限检查
    if not await check_admin(event):
        await sub.finish("⚠️ 权限不足\n只有管理员才能使用订阅命令")
        return
        
    msg = str(event.get_message()).strip()
    msg = msg.replace("订阅直播", "").strip()
    
    if not msg.isdigit():
        await sub.finish("请输入正确的UID")
        return
        
    uid = int(msg)
    try:
        liver_info = await get_live_info_by_uid(uid)
        if not liver_info:
            await sub.finish(f"未找到UID为 {uid} 的直播间信息，请确认该用户是否开通直播间")
            return
            
        if live_db.add_subscription(event.group_id, liver_info.room_id):
            live_db.update_liver_info(liver_info)
            status = "🔴直播中" if liver_info.live_status else "⭕未开播"
            msg = (
                f"成功订阅 {liver_info.name}（{uid}）的直播间\n"
                f"房间号：{liver_info.room_id}\n"
                f"当前状态：{status}\n"
                f"标题：{liver_info.title}\n"
                f"分区：{liver_info.area_name}"
            )
            await bot.send_group_msg(group_id=event.group_id, message=msg)
            return  # 添加 return 避免继续执行
        else:
            await sub.finish("该主播的直播间已经订阅过")
            return
            
    except NeedLoginError as e:
        try:
            # 生成登录二维码
            qrcode_bytes, qr_key = await generate_qrcode()
            await bot.send_group_msg(
                group_id=event.group_id,
                message=(
                    "请使用B站手机客户端扫描二维码登录\n"
                    "1. 打开B站手机客户端\n"
                    "2. 点击右下角「我的」\n"
                    "3. 点击右上角扫一扫\n"
                    "4. 扫描下方二维码\n"
                    "5. 在手机上确认登录"
                )
            )
            await bot.send_group_msg(
                group_id=event.group_id,
                message=MessageSegment.image(qrcode_bytes)
            )
            
            last_status = ""
            # 等待扫码
            for _ in range(90):  # 最多等待90*2=180秒
                await asyncio.sleep(2)
                status = await check_qrcode_status(qr_key)
                
                if isinstance(status, Credential):  # 如返回的是凭证，说明登录成功
                    live_db.save_credential(status)
                    await bot.send_group_msg(
                        group_id=event.group_id,
                        message="登录成功！请重新发送订阅命令"
                    )
                    return
                elif status != last_status and status != "请扫码":  # 只在状态变化时发送提示
                    await bot.send_group_msg(
                        group_id=event.group_id,
                        message=status
                    )
                    last_status = status
                    if status in ["二维码已失效"]:  # 只在二维码失效时退出
                        break
                    
            if "已失效" not in last_status:  # 只在真正超时时发送超时消息
                await bot.send_group_msg(
                    group_id=event.group_id,
                    message="登录超时，请重新尝试"
                )
            
        except Exception as e:
            print(f"生成二维码异常: {e}")
            await bot.send_group_msg(
                group_id=event.group_id,
                message="生成登录二维码失败，请稍后重试"
            )
        return  # 添加这个 return 避免继续执行

    except RateLimitError as e:
        await sub.finish(str(e))
        return
        
    except Exception as e:
        print(f"订阅处理异常: {e}")
        # 如果已经发送了成功消息，就不再发送错误消息
        if "success" not in str(e).lower():
            await sub.finish("订阅处理过程中发生错误，请稍后重试")
        return

# 添加一个字典来存储每个群的取消订阅状态
unsub_status = {}

@unsub.handle()
async def handle_unsub(bot: Bot, event: GroupMessageEvent):
    # 修改权限检查
    if not await check_admin(event):
        await sub.finish("⚠️ 权限不足\n只有管理员才能使用取消订阅命令")
        return
        
    group_id = event.group_id
    room_ids = live_db.get_subscription(group_id)
    
    if not room_ids:
        await unsub.finish("当前群未订阅任何直播间")
        return
    
    # 生成订阅列表消息
    msg = "当前订阅的直播间列表：\n"
    for idx, room_id in enumerate(room_ids, 1):
        liver_info = live_db.get_liver_info(room_id)
        if liver_info:
            status = "🔴直播中" if liver_info.live_status else "⭕未开播"
            msg += f"{idx}. {liver_info.name}（{room_id}）{status}\n"
        else:
            msg += f"{idx}. {room_id}\n"
    
    msg += f"\n请发送要取消订阅的直播间序号（1-{len(room_ids)}）"
    
    # 保存当前群的订阅列表状
    unsub_status[group_id] = {
        "step": "waiting_number",
        "room_ids": room_ids,
        "last_msg": msg,
        "timestamp": time.time()  # 添加时间戳
    }
    
    await unsub.send(msg)

@unsub.got("number")
async def handle_unsub_number(bot: Bot, event: GroupMessageEvent, number: str = EventPlainText()):
    group_id = event.group_id
    
    # 检查是否处于等待序号状态
    if group_id not in unsub_status or unsub_status[group_id]["step"] != "waiting_number":
        await unsub.finish("请先发送取消订阅命令")
        return
    
    try:
        idx = int(number)
        room_ids = unsub_status[group_id]["room_ids"]
        
        if not 1 <= idx <= len(room_ids):
            await unsub.reject(f"请发送正确的序号（1-{len(room_ids)}）")
            return
        
        room_id = room_ids[idx - 1]
        liver_info = live_db.get_liver_info(room_id)
        name = liver_info.name if liver_info else room_id
        
        # 更新状态为等待确认
        unsub_status[group_id].update({
            "step": "waiting_confirm",
            "selected_room_id": room_id,
            "selected_name": name
        })
        
        # 修改这行，使用三引号来避免引号冲突
        confirm_msg = f'''确定要取消订阅 {name}（{room_id}）的播间吗？
请发送"确认"或"取消"'''
        await unsub.send(confirm_msg)
        
    except ValueError:
        await unsub.reject("请发送正确的数字序号")

@unsub.got("confirm")
async def handle_unsub_confirm(bot: Bot, event: GroupMessageEvent, confirm: str = EventPlainText()):
    group_id = event.group_id
    
    # 检查是否处于等待确认状态
    if group_id not in unsub_status or unsub_status[group_id]["step"] != "waiting_confirm":
        await unsub.finish("请先发送取消订阅命令")
        return
    
    if confirm != "确认":
        if confirm == "取消":
            await unsub.finish("已取消操作")
        else:
            await unsub.reject('请发送"确认"或"取消"')
        return
    
    # 执行取消订阅
    room_id = unsub_status[group_id]["selected_room_id"]
    name = unsub_status[group_id]["selected_name"]
    
    if live_db.remove_subscription(group_id, room_id):
        # 清理状态
        del unsub_status[group_id]
        await unsub.finish(f"已取消订阅 {name}（{room_id}）的直播间")
    else:
        await unsub.finish("取消订阅失败，请稍后重试")

# 添加超时处理
@scheduler.scheduled_job('interval', minutes=5)
async def clean_unsub_status():
    """清理超时的取消订阅状态"""
    current_time = time.time()
    for group_id in list(unsub_status.keys()):
        if current_time - unsub_status[group_id].get("timestamp", 0) > 300:  # 5分钟超时
            del unsub_status[group_id]

# 添加一个字典来存储订阅列表状态
sub_list_status = {}

@sub_list.handle()
async def handle_sub_list(event: GroupMessageEvent):
    group_id = event.group_id
    room_ids = live_db.get_subscription(group_id)
    if not room_ids:
        await sub_list.finish("当前群未订阅任何直播间")
        return
        
    msg = "当前订阅的直播间：\n"
    for idx, room_id in enumerate(room_ids, 1):
        liver_info = live_db.get_liver_info(room_id)
        if liver_info:
            status = "🔴直播中" if liver_info.live_status else "⭕未开播"
            msg += f"{idx}. {liver_info.name}（{room_id}）{status}\n"
        else:
            msg += f"{idx}. {room_id}\n"
    
    msg += "\n发送序号查看主播详细信息（60秒内有效）"
    
    # 保存状态
    sub_list_status[group_id] = {
        "room_ids": room_ids,
        "timestamp": time.time()
    }
    
    await sub_list.send(msg.strip())

@sub_list.got("number")
async def handle_sub_list_number(event: GroupMessageEvent, number: str = EventPlainText()):
    group_id = event.group_id
    
    # 检查是否在60秒内
    if (
        group_id not in sub_list_status or 
        time.time() - sub_list_status[group_id]["timestamp"] > 60
    ):
        # 超时，直接结束，不发送消息
        del sub_list_status[group_id]
        await sub_list.finish()
        return
        
    try:
        idx = int(number)
        room_ids = sub_list_status[group_id]["room_ids"]
        
        if not 1 <= idx <= len(room_ids):
            # 序号错误，直接结束，不发送消息
            del sub_list_status[group_id]
            await sub_list.finish()
            return
            
        room_id = room_ids[idx - 1]
        liver_info = live_db.get_liver_info(room_id)
        
        if liver_info:
            status = "🔴直播中" if liver_info.live_status else "⭕未开播"
            
            # 构建消息
            msg = Message()
            
            # 如果有封面且正在直播，添加封面图片
            if liver_info.cover and liver_info.live_status:
                try:
                    msg += MessageSegment.image(liver_info.cover)
                    msg += MessageSegment.text("\n")  # 添加换行
                except Exception as e:
                    print(f"添加封面图片失败: {e}")
            
            # 添加文字信息
            msg += MessageSegment.text(
                f"主播：{liver_info.name}\n"
                f"UID：{liver_info.uid}\n"
                f"房间号：{liver_info.room_id}\n"
                f"状态：{status}\n"
                f"标题：{liver_info.title}\n"
                f"分区：{liver_info.area_name}\n"
                f"标签：{' '.join(liver_info.tags)}\n"
                f"直播间：https://live.bilibili.com/{room_id}"
            )
            
            await sub_list.finish(msg)
        else:
            await sub_list.finish(f"未找到房间 {room_id} 的信息")
            
    except ValueError:
        # 输入不是数字，直接结束，不发送消息
        del sub_list_status[group_id]
        await sub_list.finish()
        return
    finally:
        # 清理状态
        if group_id in sub_list_status:
            del sub_list_status[group_id]

# 添加定时清理状态的任务
@scheduler.scheduled_job('interval', minutes=1)
async def clean_sub_list_status():
    """清理超时的订阅列表状态"""
    current_time = time.time()
    for group_id in list(sub_list_status.keys()):
        if current_time - sub_list_status[group_id]["timestamp"] > 60:
            del sub_list_status[group_id]

@admin_cmd.handle()
async def handle_admin(bot: Bot, event: GroupMessageEvent):
    # 检查是否是超级管理员
    if event.user_id not in plugin_config.live_super_admins:
        super_admins_info = []
        for admin_id in plugin_config.live_super_admins:
            try:
                info = await bot.get_group_member_info(
                    group_id=event.group_id,
                    user_id=admin_id,
                    no_cache=True
                )
                nickname = info.get("card") or info.get("nickname", str(admin_id))
                super_admins_info.append(f"{nickname}（{admin_id}）")
            except:
                super_admins_info.append(str(admin_id))
        
        await admin_cmd.finish(
            "⚠️ 权限不足\n"
            "只有全局管理员才能管理订阅管理员\n"
            f"全局管理员：\n" + "\n".join(f"• {admin}" for admin in super_admins_info)
        )
        return
        
    msg = str(event.get_message()).strip()
    cmd_parts = msg.split()
    
    if len(cmd_parts) < 2:
        await admin_cmd.finish(
            "使用方法:\n"
            "订阅管理 添加管理 @用户\n"
            "订阅管理 移除管理 @用户"
        )
        return
        
    action = cmd_parts[1]  # 获取操作类型（添加管理/移除管理）
    
    # 获取被@的用户
    at_users = [seg.data['qq'] for seg in event.message if seg.type == 'at']
    if not at_users:
        await admin_cmd.finish("请@要操作的用户")
        return
        
    target_user = int(at_users[0])
    
    # 检查目标用户是否是全局管理员
    if target_user in plugin_config.live_super_admins:
        await admin_cmd.finish(f"用户 {target_user} 是全局管理员，无需添加或移除")
        return
        
    group_str = str(event.group_id)
    
    # 确保群组存于数据中
    if group_str not in live_db._data:
        live_db._data[group_str] = SubscriptionInfo(group_id=event.group_id)
    
    if action == "添加管理":
        if target_user in live_db._data[group_str].admin_users:
            await admin_cmd.finish(f"用户 {target_user} 已经是管理员了")
            return
            
        live_db._data[group_str].admin_users.append(target_user)
        live_db._save()
        await admin_cmd.finish(f"已添加用户 {target_user} 为管理员")
        
    elif action == "移除管理":
        if target_user not in live_db._data[group_str].admin_users:
            await admin_cmd.finish(f"用户 {target_user} 不是管理员")
            return
            
        live_db._data[group_str].admin_users.remove(target_user)
        live_db._save()
        await admin_cmd.finish(f"已移除用户 {target_user} 的管理员权限")
        
    else:
        await admin_cmd.finish(
            "未知的操作类型\n"
            "使用方法:\n"
            "订阅管理 添加管理 @用户\n"
            "订阅管理 移除管理 @用户"
        )

@admin_list.handle()
async def handle_admin_list(bot: Bot, event: GroupMessageEvent):
    group_id = event.group_id
    group_str = str(group_id)
    
    try:
        # 获取群信息
        group_info = await bot.get_group_info(group_id=group_id)
        group_name = group_info["group_name"]
        
        # 获取管理员列表
        admin_users = live_db._data.get(group_str, SubscriptionInfo(group_id=group_id)).admin_users
        
        if not admin_users:
            msg = (
                f"群【{group_name}】当前没有订阅管理员\n\n"
                "添加管理员方法：\n"
                "订阅管理 添加管理 @用户"
            )
            await bot.send_group_msg(group_id=group_id, message=msg)
            return
            
        # 获取每个管理员的群昵称
        msg = f"群【{group_name}】的订阅管理员列表：\n"
        for user_id in admin_users:
            try:
                member_info = await bot.get_group_member_info(
                    group_id=group_id,
                    user_id=user_id,
                    no_cache=True  # 不使用缓存
                )
                nickname = member_info.get("card") or member_info.get("nickname", str(user_id))
                msg += f"• {nickname}（{user_id}）\n"
            except Exception as e:
                msg += f"• {user_id}\n"
                print(f"获取成员 {user_id} 信息失败: {e}")
                
        # 添加说明
        msg += "\n管理员可以执行以下操作：\n"
        msg += "1. 添加/移除订阅\n"
        msg += "2. 添加/移除其他管理员\n"
        msg += "\n使用方法：\n"
        msg += "订阅管理 添加管理 @用户\n"
        msg += "订阅管理 移除管理 @用户"
        
        await bot.send_group_msg(group_id=group_id, message=msg)
        
    except Exception as e:
        print(f"获理员列表失败: {e}")
        error_msg = (
            "获取管理员列表失败，请稍后重试\n"
            f"错误信息：{str(e)}"
        )
        await bot.send_group_msg(group_id=group_id, message=error_msg)
        return  # 添加 return 避免继续执行

# 添加状态缓存字典
live_status_cache = {}

async def check_live_status():
    """检查直播状态"""
    print("\n=== 开始检查直播状态 ===")
    room_ids = live_db.get_all_rooms()
    print(f"需要检查房间数: {len(room_ids)}")
    
    try:
        bot = get_bot()  # 获取机器人实例
    except ValueError as e:
        print(f"获取机器人实例失败: {e}")
        return
    
    for room_id in room_ids:
        print(f"\n正在检查房间 {room_id}...")
        old_info = live_db.get_liver_info(room_id)
        new_info = await get_live_info(room_id)
        
        if not new_info:
            print(f"获取房间 {room_id} 信息失败，跳过")
            continue
            
        # 检查缓存中的状态
        cached_status = live_status_cache.get(room_id, {
            "live_status": new_info.live_status,  # 初始化时使用当前状态
            "title": new_info.title,  # 初始化时使用当前标题
            "last_check": 0
        })
        
        # 更新数据库中的信息
        live_db.update_liver_info(new_info)
        
        # 打印状态变化
        if cached_status["live_status"] != new_info.live_status:
            print(
                f"直播状态变化: {new_info.name}\n"
                f"原状态: {'直播中' if cached_status['live_status'] else '未开播'}\n"
                f"新状态: {'直播中' if new_info.live_status else '未开播'}"
            )
            
            # 只有在非首次检查时才发送通知
            if cached_status["last_check"] > 0:
                for group_id in live_db._data.keys():
                    if room_id not in live_db.get_subscription(int(group_id)):
                        continue
                        
                    if new_info.live_status:  # 开播提醒
                        print(f"向群 {group_id} 发送开播提醒")
                        # 构建消息
                        msg = Message()
                        
                        # 添加封面图片
                        if new_info.cover:
                            try:
                                msg += MessageSegment.image(new_info.cover)
                                msg += MessageSegment.text("\n")  # 添加换行
                            except Exception as e:
                                print(f"添加封面图片失败: {e}")
                        
                        # 添加文字信息
                        msg += MessageSegment.text(
                            f"🔴直播提醒\n"
                            f"主播：{new_info.name}\n"
                            f"标题：{new_info.title}\n"
                            f"分区：{new_info.area_name}\n"
                            f"标签：{' '.join(new_info.tags)}\n"
                            f"直播间：https://live.bilibili.com/{room_id}"
                        )
                        
                        try:
                            await bot.send_group_msg(
                                group_id=int(group_id),
                                message=msg
                            )
                        except Exception as e:
                            print(f"发送开播提醒失败: {e}")
                    else:  # 下播提醒
                        print(f"向群 {group_id} 发送下播提醒")
                        msg = f"⭕下播提醒\n{new_info.name} 的直播结束了"
                        try:
                            await bot.send_group_msg(
                                group_id=int(group_id),
                                message=msg
                            )
                        except Exception as e:
                            print(f"发送下播提醒失败: {e}")
            else:
                print("首次检查，过通知")
                
        elif cached_status["title"] != new_info.title and cached_status["last_check"] > 0:
            print(
                f"标题变化: {new_info.name}\n"
                f"原标题: {cached_status['title']}\n"
                f"新标题: {new_info.title}"
            )
            # 构建消息
            msg = Message()
            
            # 添加文字信息
            msg += MessageSegment.text(
                f"📢标题更新\n"
                f"主播：{new_info.name}\n"
                f"新标题：{new_info.title}\n"
                f"原标题：{cached_status['title'] if cached_status['title'] else '无'}"
            )
            
            try:
                await bot.send_group_msg(
                    group_id=int(group_id),
                    message=msg
                )
            except Exception as e:
                print(f"发送标题更新提醒失败: {e}")
        else:
            print(f"状态未变: {new_info.name} - {'直播中' if new_info.live_status else '未开播'}")
        
        # 更新缓存
        live_status_cache[room_id] = {
            "live_status": new_info.live_status,
            "title": new_info.title,
            "last_check": time.time()
        }
                    
        await asyncio.sleep(1)  # 防止请求太快
    
    print("\n=== 检查完成 ===\n")

# 注册定时任务
scheduler.add_job(
    check_live_status,
    "interval",
    seconds=plugin_config.live_check_interval,
    id="live_status_check",
    replace_existing=True
)

# 添加测试命令
test = on_command("订阅测试", permission=GROUP, priority=1, block=True)

@test.handle()
async def handle_test(bot: Bot, event: GroupMessageEvent):
    try:
        await bot.send_group_msg(
            group_id=event.group_id,
            message="测试消息：机器人正常运行中"
        )
    except Exception as e:
        print(f"发送测试消息失败：{e}")

# 修改账号状态命定义
account_status = on_command(
    "账号状态",
    aliases={"登录状", "cookie状态"},
    permission=GROUP,  # 修改为只需要群聊权限
    priority=5,
    block=True
)

@account_status.handle()
async def handle_account_status(bot: Bot, event: GroupMessageEvent):
    # 检查是否是超级管理员
    if event.user_id not in plugin_config.live_super_admins:
        super_admins_info = []
        for admin_id in plugin_config.live_super_admins:
            try:
                info = await bot.get_group_member_info(
                    group_id=event.group_id,
                    user_id=admin_id,
                    no_cache=True
                )
                nickname = info.get("card") or info.get("nickname", str(admin_id))
                super_admins_info.append(f"{nickname}（{admin_id}）")
            except:
                super_admins_info.append(str(admin_id))
        
        await account_status.finish(
            "⚠️ 权限不足\n"
            "只有全局管理员才能查看账号状态\n"
            f"全局管理员：\n" + "\n".join(f"• {admin}" for admin in super_admins_info)
        )
        return

    credential = live_db.get_credential()
    if not credential:
        await account_status.finish(
            "当前未登录，请先使用以下命令进行登录：\n"
            "1. 发送 订阅直播 [UID] 命令\n"
            "2. 使用B站手机客户端扫描二维码\n"
            "3. 在手机上确认登"
        )
        return
    
    try:
        # 尝试获取一个用户信息来测试cookie是否有效
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Origin": "https://space.bilibili.com",
            "Referer": "https://space.bilibili.com",
            "Cookie": f"SESSDATA={credential.sessdata}; bili_jct={credential.bili_jct}; buvid3={credential.buvid3}"
        }
        
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get("https://api.bilibili.com/x/web-interface/nav") as resp:
                result = await resp.json()
                if result["code"] == 0:
                    user_info = result["data"]
                    msg = (
                        "🔑 账号登录状态\n"
                        f"状态：✅ 已登录\n"
                        f"户名：{user_info['uname']}\n"
                        f"等级：{user_info['level_info']['current_level']}\n"
                        f"硬币：{user_info['money']}\n"
                        "Cookie：✅ 有效\n"
                        f"会员状态：{'⭐ VIP' if user_info['vipStatus'] else '普通用户'}"
                    )
                else:
                    msg = (
                        "🔑 账号登录状态\n"
                        "状态：❌ Cookie已失效\n"
                        "请重新登录：\n"
                        "1. 送 订阅直播 [UID] ���令\n"
                        "2. 使用B站手机客户端扫描二码\n"
                        "3. 在手机上确认登录"
                    )
    except Exception as e:
        print(f"检查账号状态失败: {e}")
        msg = (
            " 账号登录状态\n"
            "状态：❌ 检查失败\n"
            f"错误信息：{str(e)}\n"
            "请稍后重试或重新登录"
        )
    
    await account_status.finish(msg)

# 添加重新登录命令
relogin = on_command(
    "重新登录",
    aliases={"更新cookie", "更新登录", "重新登陆", "更新登陆"},
    permission=GROUP,
    priority=5,
    block=True
)

@relogin.handle()
async def handle_relogin(bot: Bot, event: GroupMessageEvent):
    # 检查是否是超级管理员
    if event.user_id not in plugin_config.live_super_admins:
        super_admins_info = []
        for admin_id in plugin_config.live_super_admins:
            try:
                info = await bot.get_group_member_info(
                    group_id=event.group_id,
                    user_id=admin_id,
                    no_cache=True
                )
                nickname = info.get("card") or info.get("nickname", str(admin_id))
                super_admins_info.append(f"{nickname}（{admin_id}）")
            except:
                super_admins_info.append(str(admin_id))
        
        await relogin.finish(
            "⚠️ 权限不足\n"
            "只有全局管理员才能重新登录\n"
            f"全局管理员：\n" + "\n".join(f"• {admin}" for admin in super_admins_info)
        )
        return

    try:
        # 生成登录二维码
        qrcode_bytes, qr_key = await generate_qrcode()
        await bot.send_group_msg(
            group_id=event.group_id,
            message=(
                "请使用B站手机客户端扫描二维码登录\n"
                "1. 打开B站手机客户端\n"
                "2. 点击右下角「我的」\n"
                "3. 点击右上角扫一扫\n"
                "4. 扫描下方二维码\n"
                "5. 在手机上确认登录"
            )
        )
        await bot.send_group_msg(
            group_id=event.group_id,
            message=MessageSegment.image(qrcode_bytes)
        )
        
        last_status = ""
        # 等待扫码
        for _ in range(90):  # 最多等待90*2=180秒
            await asyncio.sleep(2)
            status = await check_qrcode_status(qr_key)
            
            if isinstance(status, Credential):  # 如果返回的是凭证，说明登录成功
                live_db.save_credential(status)
                await bot.send_group_msg(
                    group_id=event.group_id,
                    message="登录成功！Cookie已更新"
                )
                return
            elif status != last_status and status != "请扫码":  # 只在状态变化时发送提示
                await bot.send_group_msg(
                    group_id=event.group_id,
                    message=status
                )
                last_status = status
                if status in ["二维码已失效"]:  # 只在二维码失效时退出
                    break
                
        if "已失效" not in last_status:  # 只在真正超时时发送超时消息
            await bot.send_group_msg(
                group_id=event.group_id,
                message="登录超时，请重新尝试"
            )
        
    except Exception as e:
        print(f"生成二维码异常: {e}")
        await bot.send_group_msg(
            group_id=event.group_id,
            message="生成登录二维码失败，请稍后重试"
        )

# 添加代理设置命令（隐藏功能）
proxy_cmd = on_command(
    "设置代理",
    aliases={"代理设置", "更新代理"},
    permission=GROUP,
    priority=5,
    block=True
)

@proxy_cmd.handle()
async def handle_proxy(bot: Bot, event: GroupMessageEvent):
    # 检查是否是超级管理员
    if event.user_id not in plugin_config.live_super_admins:
        # 不显示何提示，假装这个命令不存在
        return

    msg = str(event.get_message()).strip()
    msg = msg.replace("设置代理", "").strip()
    msg = msg.replace("代理设置", "").strip()
    msg = msg.replace("更新代理", "").strip()
    
    if not msg:
        current_proxy = plugin_config.proxy or "未设置"
        await proxy_cmd.finish(
            f"当前代理设置：{current_proxy}\n"
            "设置方法：\n"
            "设置代理 http://127.0.0.1:7890\n"
            "设置代理 none (删除代理)"
        )
        return
        
    if msg.lower() == "none":
        plugin_config.proxy = None
        await proxy_cmd.finish("已删除代理设置")
        return
        
    if not (msg.startswith("http://") or msg.startswith("https://")):
        await proxy_cmd.finish("代理格式错误，必须以 http:// 或 https:// 开头")
        return
        
    plugin_config.proxy = msg
    await proxy_cmd.finish(f"代理已更新为：{msg}")

# 获取 Chromium 路径
CHROME_PATH = str(Path(".local-chromium/win64-1373764/chrome-win/chrome.exe").absolute())

async def capture_live_screenshot(room_id: int) -> Optional[bytes]:
    """获取直播间截图"""
    try:
        # 配置 Chrome 选项
        chrome_options = Options()
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--disable-software-rasterizer')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-logging')
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_argument('--mute-audio')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument('--disable-popup-blocking')
        chrome_options.add_argument('--enable-unsafe-webgl')
        chrome_options.add_argument('--autoplay-policy=no-user-gesture-required')  # 允许自动播放
        chrome_options.add_argument('--disable-features=PreloadMediaEngagementData,MediaEngagementBypassAutoplayPolicies')  # 禁用媒体参与度检查
        
        # 添加实验性选项
        chrome_options.add_experimental_option('prefs', {
            'profile.default_content_setting_values.media_stream': 1,  # 允许媒体流
            'profile.default_content_setting_values.notifications': 2,  # 禁用通知
            'profile.default_content_setting_values.automatic_downloads': 1,  # 允许自动下载
            'profile.managed_default_content_settings.images': 1,  # 允许图片
            'profile.default_content_setting_values.sound': 1,  # 允许声音
            'profile.managed_default_content_settings.javascript': 1,  # 允许 JavaScript
            'profile.default_content_settings.cookies': 1,  # 允许 cookies
            'profile.content_settings.exceptions.autoplay': {  # 允许自动播放
                '*': {
                    'setting': 1
                }
            }
        })
        
        # 添加代理支持
        if plugin_config.proxy:
            chrome_options.add_argument(f'--proxy-server={plugin_config.proxy}')
        
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # 最多重试3次
        for retry in range(3):
            try:
                # 创建 WebDriver
                service = Service(log_path=os.devnull)  # 禁用服务日志
                driver = webdriver.Chrome(service=service, options=chrome_options)
                
                try:
                    # 设置页面加载超时
                    driver.set_page_load_timeout(30)
                    driver.set_script_timeout(30)
                    
                    # 访问直播间
                    print(f"正在访问直播间: {room_id} (第{retry + 1}次尝试)")
                    driver.get(f'https://live.bilibili.com/{room_id}')
                    
                    # 等待直播画面加载
                    print("等待直播画面加载...")
                    wait = WebDriverWait(driver, 10)
                    player = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'live-player-mounter')))
                    
                    # 等待一些动态内容加载
                    print("等待动态内容加载...")
                    await asyncio.sleep(5)
                    
                    # 滚动到播放器位置
                    driver.execute_script("arguments[0].scrollIntoView(true);", player)
                    await asyncio.sleep(1)  # 等待滚动完成
                    
                    # 获取播放器位置和大小
                    location = player.location
                    size = player.size
                    
                    # 获取截图
                    print("正在获取截图...")
                    screenshot = driver.get_screenshot_as_png()
                    
                    # 裁剪截图，调整上下边框位置
                    from PIL import Image
                    from io import BytesIO
                    
                    image = Image.open(BytesIO(screenshot))
                    cropped = image.crop((
                        location['x'],  # 左边界不变
                        max(0, location['y'] - 200),  # 上边界向上200像素
                        location['x'] + size['width'],  # 右边界不变
                        location['y'] + size['height'] - 180  # 下边界向上200像素（从100改为200）
                    ))
                    
                    # 转换为字节
                    output = BytesIO()
                    cropped.save(output, format='PNG', quality=95)
                    screenshot_bytes = output.getvalue()
                    
                    print("截图获取成功")
                    return screenshot_bytes
                    
                except Exception as e:
                    print(f"截图过程发生错误 (第{retry + 1}次尝试): {e}")
                    if retry < 2:  # 如果不是最后一次尝试，继续重试
                        await asyncio.sleep(5)  # 等待5秒后重试
                        continue
                    raise  # 最后一次尝试失败，抛出异常
                    
                finally:
                    # 确保浏览器被关闭
                    try:
                        driver.quit()
                    except Exception as e:
                        print(f"关闭浏览器失败: {e}")
                        
            except Exception as e:
                print(f"WebDriver 创建失败 (第{retry + 1}次尝试): {e}")
                if retry < 2:  # 如果不是最后一次尝试，继续重试
                    await asyncio.sleep(5)  # 等待5秒后重试
                    continue
                raise  # 最后一次尝试失败，抛出异常
                
    except Exception as e:
        print(f"获取直播间截图失败: {e}")
        return None

# 添加定时截图任务
@scheduler.scheduled_job('interval', hours=1)
async def capture_live_screenshots():
    """定时获取直播截图"""
    print("\n=== 开始获取直播截图 ===")
    
    try:
        bot = get_bot()
    except ValueError as e:
        print(f"获取机器人实例失败: {e}")
        return
        
    room_ids = live_db.get_all_rooms()
    for room_id in room_ids:
        liver_info = live_db.get_liver_info(room_id)
        if not liver_info or not liver_info.live_status:
            continue
            
        print(f"正在获取直播间 {room_id} 的截图...")
        screenshot = await capture_live_screenshot(room_id)
        
        if screenshot:
            # 获取当前时间
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 构建消息
            msg = Message()
            msg += MessageSegment.image(screenshot)
            msg += MessageSegment.text(
                f"\n📸 直播间实时画面\n"
                f"主播：{liver_info.name}\n"
                f"标题：{liver_info.title}\n"
                f"时间：{current_time}"
            )
            
            # 发送到所有订阅的群
            for group_id in live_db._data.keys():
                if room_id in live_db.get_subscription(int(group_id)):
                    try:
                        await bot.send_group_msg(
                            group_id=int(group_id),
                            message=msg
                        )
                        print(f"已发送直播间 {room_id} 的截图到群 {group_id}")
                    except Exception as e:
                        print(f"发送截图到群 {group_id} 失败: {e}")
                        
            await asyncio.sleep(5)  # 等待一下，避免发送太快
            
    print("=== 截图获取完成 ===\n")

# 添加截图命令
screenshot_cmd = on_command(
    "截图",
    aliases={"直播截图", "查看直播"},
    permission=GROUP,
    priority=5,
    block=True
)

@screenshot_cmd.handle()
async def handle_screenshot(bot: Bot, event: GroupMessageEvent):
    # 检查是否是超级管理员
    if event.user_id not in plugin_config.live_super_admins:
        return  # 不是超级管理员直接返回，不显示任何提示
    
    # 获取所有正在直播的主播
    live_rooms = []
    for room_id in live_db.get_all_rooms():
        liver_info = live_db.get_liver_info(room_id)
        if liver_info and liver_info.live_status:
            live_rooms.append(liver_info)
    
    if not live_rooms:
        await screenshot_cmd.finish("当前没有主播在直播")
        return
    
    # 生成列表消息
    msg = "当前直播中的主播：\n"
    for idx, info in enumerate(live_rooms, 1):
        msg += f"{idx}. {info.name} - {info.title}\n"
    msg += "\n发送序号获取直播画面截图"
    
    # 保存状态
    screenshot_status[event.group_id] = {
        "rooms": live_rooms,
        "timestamp": time.time()
    }
    
    await screenshot_cmd.send(msg)

@screenshot_cmd.got("number")
async def handle_screenshot_number(bot: Bot, event: GroupMessageEvent, number: str = EventPlainText()):
    # 检查是否是超级管理员
    if event.user_id not in plugin_config.live_super_admins:
        return
        
    group_id = event.group_id
    
    # 检查是否在60秒内
    if (
        group_id not in screenshot_status or 
        time.time() - screenshot_status[group_id]["timestamp"] > 60
    ):
        del screenshot_status[group_id]
        await screenshot_cmd.finish()
        return
        
    try:
        idx = int(number)
        rooms = screenshot_status[group_id]["rooms"]
        
        if not 1 <= idx <= len(rooms):
            del screenshot_status[group_id]
            await screenshot_cmd.finish()
            return
            
        liver_info = rooms[idx - 1]
        
        # 发送等待消息
        wait_msg = await bot.send_group_msg(
            group_id=group_id,
            message=f"正在获取 {liver_info.name} 的直播画面，请稍候..."
        )
        
        # 获取截图
        screenshot = await capture_live_screenshot(liver_info.room_id)
        
        if screenshot:
            # 获取当前时间
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 构建消息
            msg = Message()
            msg += MessageSegment.image(screenshot)
            msg += MessageSegment.text(
                f"\n📸 直播间实时画面\n"
                f"主播：{liver_info.name}\n"
                f"标题：{liver_info.title}\n"
                f"分区：{liver_info.area_name}\n"
                f"时间：{current_time}"
            )
            
            await screenshot_cmd.finish(msg)
        else:
            await screenshot_cmd.finish("获取直播画面失败，请稍后重试")
            
    except ValueError:
        del screenshot_status[group_id]
        await screenshot_cmd.finish()
        return
    finally:
        if group_id in screenshot_status:
            del screenshot_status[group_id]

# 添加状态典
screenshot_status = {}

# 添加定时清理任务
@scheduler.scheduled_job('interval', minutes=1)
async def clean_screenshot_status():
    """清理超时的截图状态"""
    current_time = time.time()
    for group_id in list(screenshot_status.keys()):
        if current_time - screenshot_status[group_id]["timestamp"] > 60:
            del screenshot_status[group_id]
