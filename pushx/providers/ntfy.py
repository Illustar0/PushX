import json
import logging
from enum import Enum
from typing import List, Dict, Optional

import httpx
from pydantic import Field, AliasChoices, ConfigDict

from pushx.provider import ProviderMetadata, BasePushProvider, BaseProviderParams, PushResult

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


# Metadata
class Priority(Enum):
    """priority 的枚举类"""

    max = 5
    high = 4
    default = 3
    low = 2
    min = 1


# noinspection SpellCheckingInspection
class NotifyParams(BaseProviderParams):
    """Notify 所需参数"""

    model_config = ConfigDict(use_enum_values=True)

    topic: str = None
    """无实际作用，会被覆盖"""
    title: str = Field(..., validation_alias=AliasChoices("title", "Title"))
    """通知的标题"""
    message: str = Field(None, validation_alias=AliasChoices("message", "content"))
    """通知的内容，支持 Markdown"""
    tags: List[str] = None
    """通知的 tags"""
    priority: int | Priority = None
    """通知的优先级"""
    actions: List[Dict] = None
    """通知的 Actions"""
    click: str = None
    """点击通知时打开的 URL"""
    markdown: bool = None
    """message 是否为 Markdown 格式"""
    icon: str = None
    """通知图标的 URL"""
    attach: str = None
    """附件的 URL"""
    filename: str = None
    """附件的文件名"""
    delay: int = None
    """延迟交付的时间戳或持续时间"""


# noinspection SpellCheckingInspection
class NotifierParams(BaseProviderParams):
    """Notifier 所需参数"""

    topic: str
    """Ntfy 的 topic"""
    base_url: str = "https://ntfy.sh"
    """Ntfy 服务器 URL"""


__provider_meta__ = ProviderMetadata(
    name="Ntfy",
    class_name="Ntfy",
    description="Ntfy Provider",
    notifier_params=NotifierParams,
    notify_params=NotifyParams,
    extra={},
)


class Ntfy(BasePushProvider):
    def _set_notifier_params(self, params: Optional[NotifierParams] = None, **kwargs):
        if params is None:
            self._notifier_params = NotifierParams(**kwargs)
        elif kwargs:
            raise ValueError("You cannot pass NotifierParams objects and keyword arguments at the same time")
        else:
            self._notifier_params = params

    def _notify(self, params: Optional[NotifyParams] = None, **kwargs) -> PushResult:
        if params is None:
            notify_params = NotifyParams(**kwargs)
        elif kwargs:
            raise ValueError("You cannot pass in NotifyParams objects and keyword arguments at the same time")
        else:
            notify_params = params
        response = httpx.post(
            f"{self._notifier_params.base_url}",
            json=json.loads(
                notify_params.model_copy(
                    update={"topic": self._notifier_params.topic}
                ).model_dump_json()
            ),
        )
        try:
            if "id" and "time" and "expires" in json.loads(response.text):
                return PushResult(success=True,code=200)
            else:
                logger.error(f"Ntfy Push error, detail:{response.text}")
                return PushResult(success=False,code=500,msg="An unexpected situation occurred, please refer to the response in data",data=response.text)
        except Exception as e:
            logger.error(
                f"Ntfy Push error, detail:{e}, response detail: {response.text}"
            )
            return PushResult(success=False,code=500,msg="An unexpected situation occurred, please refer to the response in data",data=response.text)
