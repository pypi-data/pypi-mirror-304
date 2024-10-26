from typing import List, Optional
from pydantic import BaseModel, Field
from nonebot import get_driver

class Config(BaseModel):
    # 直播检查间隔时间(秒)，改为60秒
    live_check_interval: int = Field(default=120)  # 从300改为60
    
    # bilibili API
    bili_api_room_by_uid: str = Field(
        default="https://api.bilibili.com/x/space/acc/info"  # 更新为新的API
    )
    bili_api_user_info: str = Field(
        default="https://api.bilibili.com/x/space/wbi/acc/info"  # 更新为新的API
    )
    bili_api_live_info: str = Field(
        default="https://api.live.bilibili.com/xlive/web-room/v1/index/getInfoByRoom"  # 更新为新的API
    )
    bili_api_user_stat: str = Field(
        default="https://api.bilibili.com/x/relation/stat"
    )
    bili_api_room_tags: str = Field(
        default="https://api.live.bilibili.com/xlive/web-room/v1/index/getRoomBaseInfo"  # 更新API
    )
    
    # 超级管理员
    live_super_admins: List[int] = Field(default_factory=list)

    # 代理设置
    proxy: Optional[str] = Field(default=None)  # 例如: "http://127.0.0.1:7890"

    class Config:
        extra = "ignore"

# 获取全局配置
global_config = get_driver().config

# 创建插件配置
plugin_config = Config(
    live_check_interval=getattr(global_config, "live_check_interval", 60),
    live_super_admins=getattr(global_config, "live_super_admins", []),
    proxy=getattr(global_config, "proxy", None),  # 添加代理配置
)
