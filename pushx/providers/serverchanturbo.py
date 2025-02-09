import json
import httpx
import logging
from typing import Union, Optional
from pydantic import Field, AliasChoices, field_serializer
from pushx.provider import ProviderMetadata, BasePushProvider, BaseProviderParams


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


# Metadata
# noinspection SpellCheckingInspection
class NotifyParams(BaseProviderParams):
    """Notify 所需参数"""
    title: str = Field(..., validation_alias=AliasChoices("title", "text"))
    """通知的标题"""
    desp: str = Field(None, validation_alias=AliasChoices("desp", "content", "message"))
    """通知的内容，支持 Markdown"""
    tags: str = None
    """通知的 tags"""
    short: str = None
    """通知的略缩"""
    noip: bool = None
    """是否隐藏调用 IP"""
    channel: str = None
    """使用的消息通道"""
    openid: str = None
    """消息抄送的 OPENID"""

    @field_serializer("noip")
    def serialize_noip(self, value: bool) -> int:
        return int(value) if value is not None else None


# noinspection SpellCheckingInspection
class NotifierParams(BaseProviderParams):
    """Notifier 所需参数"""
    sendkey: str
    """ServerChanTurbo 的 SendKey"""


__provider_meta__ = ProviderMetadata(
    name="ServerChanTurbo",
    class_name="ServerChanTurbo",
    description="ServerChanTurbo Provider",
    notifier_params=NotifierParams,
    notify_params=NotifyParams,
    extra={},
)


class ServerChanTurbo(BasePushProvider):
    def _set_notifier_params(self, params: Optional[NotifierParams] = None,**kwargs):
        if params is None:
            self._notifier_params = NotifierParams(**kwargs)
        elif kwargs:
            raise ValueError("不能同时传入 NotifierParams 对象和关键字参数")
        else:
            self._notifier_params = params

    def _notify(self, params: Optional[NotifyParams] = None,**kwargs) -> bool:
        if params is None:
            notify_params = NotifyParams(**kwargs)
        elif kwargs:
            raise ValueError("不能同时传入 NotifyParams 对象和关键字参数")
        else:
            notify_params = params
        response = httpx.post(
            f"https://sctapi.ftqq.com/{self._notifier_params.sendkey}.send",
            json=json.loads(notify_params.model_dump_json()),
        )
        try:
            if json.loads(response.text)["code"] != 0:
                logger.error(f"ServerChanTurbo Push error, detail:{response.text}")
                return False
            else:
                return True
        except Exception as e:
            logger.error(f"ServerChanTurbo Push error, detail:{e}, response detail:")
            return False
