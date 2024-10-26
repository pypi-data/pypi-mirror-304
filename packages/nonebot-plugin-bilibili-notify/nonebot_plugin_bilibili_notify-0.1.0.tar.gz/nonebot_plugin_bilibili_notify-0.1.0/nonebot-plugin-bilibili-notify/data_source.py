import json
import qrcode
import asyncio
import aiohttp
from io import BytesIO
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
from bilibili_api import user, live, Credential
from .models import LiverInfo, SubscriptionInfo
from .config import plugin_config

class LiveDB:
    """直播数据管理"""
    def __init__(self):
        self.db_file = Path("data/live_subscription/db.json")
        self.cookie_file = Path("data/live_subscription/cookie.json")
        self.db_file.parent.mkdir(parents=True, exist_ok=True)
        self._data: Dict[str, SubscriptionInfo] = {}
        self._liver_info: Dict[int, LiverInfo] = {}
        self._credential: Optional[Credential] = None
        self._load()
        self._load_credential()

    def _load(self):
        """加载数据"""
        if self.db_file.exists():
            with open(self.db_file, "r", encoding="utf8") as f:
                data = json.load(f)
                self._data = {
                    k: SubscriptionInfo.parse_obj(v) for k, v in data.get("subscriptions", {}).items()
                }
                self._liver_info = {
                    int(k): LiverInfo.parse_obj(v) for k, v in data.get("liver_info", {}).items()
                }

    def _save(self):
        """保存数据"""
        with open(self.db_file, "w", encoding="utf8") as f:
            json.dump(
                {
                    "subscriptions": {k: v.dict() for k, v in self._data.items()},
                    "liver_info": {k: v.dict() for k, v in self._liver_info.items()},
                },
                f,
                ensure_ascii=False,
                indent=2,
            )

    def add_subscription(self, group_id: int, room_id: int) -> bool:
        """添加订阅"""
        group_str = str(group_id)
        if group_str not in self._data:
            self._data[group_str] = SubscriptionInfo(group_id=group_id)
        if room_id not in self._data[group_str].room_ids:
            self._data[group_str].room_ids.append(room_id)
            self._save()
            return True
        return False

    def remove_subscription(self, group_id: int, room_id: int) -> bool:
        """移除订阅"""
        group_str = str(group_id)
        if group_str in self._data and room_id in self._data[group_str].room_ids:
            # 移除群订阅
            self._data[group_str].room_ids.remove(room_id)
            
            # 检查是否还有其他群订阅这个主播
            is_subscribed = False
            for sub in self._data.values():
                if room_id in sub.room_ids:
                    is_subscribed = True
                    break
            
            # 如果没有任何群订阅了，就删除主播信息
            if not is_subscribed and room_id in self._liver_info:
                del self._liver_info[room_id]
            
            self._save()
            return True
        return False

    def get_subscription(self, group_id: int) -> List[int]:
        """获取群订阅列表"""
        return self._data.get(str(group_id), SubscriptionInfo(group_id=group_id)).room_ids

    def get_all_rooms(self) -> List[int]:
        """获取所有订阅的房间号"""
        rooms = set()
        for sub in self._data.values():
            rooms.update(sub.room_ids)
        return list(rooms)

    def update_liver_info(self, info: LiverInfo):
        """更新主播信息"""
        self._liver_info[info.room_id] = info
        self._save()

    def get_liver_info(self, room_id: int) -> Optional[LiverInfo]:
        """获取主播信息"""
        return self._liver_info.get(room_id)

    def _load_credential(self):
        """加载凭证"""
        if self.cookie_file.exists():
            try:
                with open(self.cookie_file, "r", encoding="utf8") as f:
                    cookie_data = json.load(f)
                    self._credential = Credential(
                        sessdata=cookie_data.get("sessdata", ""),
                        bili_jct=cookie_data.get("bili_jct", ""),
                        buvid3=cookie_data.get("buvid3", "")
                    )
            except Exception as e:
                print(f"加载凭证失败: {e}")
                self._credential = None

    def save_credential(self, credential: Credential):
        """保存凭证"""
        self._credential = credential
        cookie_data = {
            "sessdata": credential.sessdata,
            "bili_jct": credential.bili_jct,
            "buvid3": credential.buvid3
        }
        with open(self.cookie_file, "w", encoding="utf8") as f:
            json.dump(cookie_data, f, ensure_ascii=False, indent=2)

    def get_credential(self) -> Optional[Credential]:
        """获取凭证"""
        return self._credential

live_db = LiveDB()

async def generate_qrcode() -> Tuple[bytes, str]:
    """生成登录二维码，返回二维码图片和key"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Origin": "https://www.bilibili.com",
            "Referer": "https://www.bilibili.com/"
        }
        
        async with aiohttp.ClientSession(headers=headers) as session:
            # 获取二维码和key
            async with session.get("https://passport.bilibili.com/x/passport-login/web/qrcode/generate") as resp:
                qr_data = await resp.json()
                if qr_data["code"] != 0:
                    raise Exception(f"获取二维码失败: {qr_data['message']}")
                
                qr_url = qr_data["data"]["url"]
                qr_key = qr_data["data"]["qrcode_key"]
                
                # 生成二维码图片
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=2,
                )
                qr.add_data(qr_url)
                qr.make(fit=True)
                
                img = qr.make_image(fill_color="black", back_color="white")
                
                # 转换为字节流
                bio = BytesIO()
                img.save(bio, format='PNG')
                qrcode_bytes = bio.getvalue()
                
                return qrcode_bytes, qr_key
    except Exception as e:
        print(f"生成二维码异常: {e}")
        raise

async def check_qrcode_status(qr_key: str) -> Union[str, Credential]:
    """检查二维码状态"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Origin": "https://www.bilibili.com",
            "Referer": "https://www.bilibili.com/"
        }
        
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(
                "https://passport.bilibili.com/x/passport-login/web/qrcode/poll",
                params={"qrcode_key": qr_key}
            ) as resp:
                result = await resp.json()
                print(f"扫码状态返回: {result}")  # 调试输出
                
                if result["code"] != 0:
                    return f"检查状态失败: {result['message']}"
                
                code = result["data"]["code"]
                message = result["data"].get("message", "")
                
                # 扫码成功
                if code == 0:
                    # 从返回数据中获取 cookie
                    data = result["data"]
                    url = data.get("url", "")
                    if "?" in url:
                        params = dict(item.split("=") for item in url.split("?")[1].split("&"))
                        credential = Credential(
                            sessdata=params.get("SESSDATA", ""),
                            bili_jct=params.get("bili_jct", ""),
                            buvid3=params.get("buvid3", "")
                        )
                        return credential
                    
                    # 如果 url 中没有参数，尝试从其他字段获取
                    refresh_token = data.get("refresh_token", "")
                    if refresh_token:
                        credential = Credential(
                            sessdata=refresh_token,
                            bili_jct=data.get("bili_jct", ""),
                            buvid3=data.get("buvid3", "")
                        )
                        return credential
                    
                    return "登录成功但获取凭证失败"
                    
                # 返回状态信息
                status_map = {
                    86101: "请扫码",
                    86090: "已扫码，请在手机上确认登录",  # 修改提示文本
                    86038: "二维码已失效",
                    86039: "二维码已失效",
                    86036: "等待确认",
                }
                return status_map.get(code, message or "未知状态")
                
    except Exception as e:
        print(f"检查扫码状态异常: {e}")
        return f"检查状态失败: {str(e)}"

class NeedLoginError(Exception):
    """需要登录的异常"""
    pass

class RateLimitError(Exception):
    """请求频率限制异常"""
    pass

async def get_live_info_by_uid(uid: int) -> Optional[LiverInfo]:
    """通过UP主的uid获取直播间信息"""
    credential = live_db.get_credential()
    if not credential:
        raise NeedLoginError("需要登录才能获取直播间信息")
        
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Origin": "https://space.bilibili.com",
            "Referer": f"https://space.bilibili.com/{uid}/",
            "Cookie": f"SESSDATA={credential.sessdata}; bili_jct={credential.bili_jct}; buvid3={credential.buvid3}"
        }
        
        # 添加代理支持
        connector = None
        if plugin_config.proxy:
            connector = aiohttp.TCPConnector(ssl=False)  # 如果使用代理，禁用SSL验证
            
        async with aiohttp.ClientSession(
            headers=headers,
            connector=connector,
            trust_env=True,  # 允许从环境变量读取代理设置
        ) as session:
            if plugin_config.proxy:
                session.proxy = plugin_config.proxy  # 设置代理
                
            # 获取用户信息，添加重试机制
            for retry in range(3):  # 最多重试3次
                if retry > 0:
                    await asyncio.sleep(10)  # 重试前等待10秒
                try:
                    await asyncio.sleep(5)  # 请求前等待5秒
                    async with session.get(f"https://api.bilibili.com/x/space/acc/info?mid={uid}") as resp:
                        user_info = await resp.json()
                        if user_info["code"] == 0:
                            break  # 成功则跳出重试循环
                        elif user_info["code"] == -799:  # 请求频繁
                            print(f"获取用户信息被限制，等待重试: {user_info}")
                            if retry == 2:  # 最后一次重试也失败
                                raise RateLimitError(
                                    "⚠️ B站API请求频率超限\n"
                                    "请等待5分钟后再试"
                                )
                            await asyncio.sleep(10)  # 额外等待10秒
                            continue
                        else:
                            print(f"获取用户信息失败: {user_info}")
                            return None
                except RateLimitError:
                    raise
                except Exception as e:
                    print(f"获取用户信息异常: {e}")
                    if retry == 2:  # 最后一次重试也失败
                        return None
                    continue
                    
            user_info = user_info["data"]
            live_room = user_info.get("live_room", {})
            
            if not live_room or not live_room.get("roomid"):
                print(f"用户 {uid} 没有直播间")
                return None
            
            room_id = live_room["roomid"]
            
            # 获取直播间信息
            await asyncio.sleep(2)  # 增加等待时间
            async with session.get(f"https://api.live.bilibili.com/xlive/web-room/v1/index/getInfoByRoom?room_id={room_id}") as resp:
                room_info = await resp.json()
                if room_info["code"] != 0:
                    print(f"获取直播间信息失败: {room_info}")
                    return None
                room_info = room_info["data"]["room_info"]
            
            # 获取粉丝数
            await asyncio.sleep(2)  # 增加等待时间
            async with session.get(f"https://api.bilibili.com/x/relation/stat?vmid={uid}") as resp:
                stat_info = await resp.json()
                followers = stat_info["data"]["follower"] if stat_info["code"] == 0 else 0
            
            # 构建返回数据
            return LiverInfo(
                uid=uid,
                room_id=room_id,
                name=user_info["name"],
                live_status=live_room["liveStatus"] == 1,
                title=room_info["title"],
                cover=room_info["cover"],
                area_name=f"{room_info['parent_area_name']}-{room_info['area_name']}",
                followers=followers,
                attention=0,
                tags=room_info.get("tags", "").split(",") if room_info.get("tags") else []
            )

    except RateLimitError:
        raise
    except Exception as e:
        print(f"获取直播间信息异常: {e}")
        if "风控校验失败" in str(e):
            raise NeedLoginError(
                "登录已失效，请选择以下方式之一：\n"
                "1. 发送 账号状态 命令重新登录\n"
                "2. 等待1小时后再试"
            )
        return None

async def get_live_info(room_id: int) -> Optional[LiverInfo]:
    """获取直播信息（通过房间号）"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Origin": "https://live.bilibili.com",
            "Referer": f"https://live.bilibili.com/{room_id}"
        }
        
        async with aiohttp.ClientSession(headers=headers) as session:
            # 获取直播间信息
            for retry in range(3):  # 添加重试机制
                if retry > 0:
                    await asyncio.sleep(5)  # 重试前等待5秒
                try:
                    await asyncio.sleep(2)  # 请求前等待2秒
                    async with session.get(f"https://api.live.bilibili.com/xlive/web-room/v1/index/getInfoByRoom?room_id={room_id}") as resp:
                        room_info = await resp.json()
                        if room_info["code"] == 0:
                            break
                        elif room_info["code"] == -799:  # 请求频繁
                            print(f"获取直播间信息被限制，等待重试: {room_info}")
                            if retry == 2:  # 最后一次重试也失败
                                return None
                            continue
                        else:
                            print(f"获取直播间信息失败: {room_info}")
                            return None
                except Exception as e:
                    print(f"获取直播间信息异常: {e}")
                    if retry == 2:
                        return None
                    continue

            room_info = room_info["data"]["room_info"]
            uid = room_info["uid"]
            
            # 获取用户信息
            await asyncio.sleep(2)
            for retry in range(3):
                if retry > 0:
                    await asyncio.sleep(5)
                try:
                    async with session.get(f"https://api.bilibili.com/x/space/acc/info?mid={uid}") as resp:
                        user_info = await resp.json()
                        if user_info["code"] == 0:
                            break
                        elif user_info["code"] == -799:
                            print(f"获取用户信息被限制，等待重试: {user_info}")
                            if retry == 2:
                                return None
                            continue
                        else:
                            print(f"获取用户信息失败: {user_info}")
                            return None
                except Exception as e:
                    print(f"获取用户信息异常: {e}")
                    if retry == 2:
                        return None
                    continue

            user_info = user_info["data"]
            
            # 构建返回数据（不再获取粉丝数，减少API请求）
            return LiverInfo(
                uid=uid,
                room_id=room_id,
                name=user_info["name"],
                live_status=room_info["live_status"] == 1,
                title=room_info["title"],
                cover=room_info["cover"],
                area_name=f"{room_info['parent_area_name']}-{room_info['area_name']}",
                followers=0,  # 不再获取粉丝数
                attention=0,
                tags=room_info.get("tags", "").split(",") if room_info.get("tags") else []
            )
    except Exception as e:
        print(f"获取直播间信息异常: {e}")
        return None

