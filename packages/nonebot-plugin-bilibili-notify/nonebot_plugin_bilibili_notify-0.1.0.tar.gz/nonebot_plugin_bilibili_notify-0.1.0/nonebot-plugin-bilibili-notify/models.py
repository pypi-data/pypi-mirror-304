from typing import List, Optional
from pydantic import BaseModel

class LiverInfo(BaseModel):
    """主播信息"""
    uid: int
    room_id: int
    name: str
    live_status: bool = False
    title: str = ""  # 直播间标题
    cover: str = ""  # 直播间封面
    area_name: str = ""  # 直播分区
    followers: int = 0  # 粉丝数
    attention: int = 0  # 关注数
    tags: List[str] = []  # 直播间标签
    
class SubscriptionInfo(BaseModel):
    """订阅信息"""
    group_id: int  # QQ群号
    room_ids: List[int] = []  # 订阅的房间号列表
    admin_users: List[int] = []  # 管理员列表
