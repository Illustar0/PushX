import json
import httpx
import logging
from typing import Union, Optional
from pydantic import Field, AliasChoices
from pushx.provider import ProviderMetadata, BasePushProvider, BaseProviderParams


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


# Metadata
class NotifyParams(BaseProviderParams):
    """Notify 所需参数"""
    title: str = Field(..., validation_alias=AliasChoices("title", "text"))
    """通知的标题"""
    # noinspection SpellCheckingInspection
    desp: str = Field(None, validation_alias=AliasChoices("desp", "content", "message"))
    """通知的内容，支持 Markdown"""
    tags: str = None
    """通知的 tags"""
    short: str = None
    """通知的略缩"""


class NotifierParams(BaseProviderParams):
    """Notifier 所需参数"""
    # noinspection SpellCheckingInspection
    sendkey: str
    """ServerChan3 的 SendKey"""
    uid: int
    """ServerChan3 的 UID"""


__provider_meta__ = ProviderMetadata(
    name="ServerChan3",
    class_name="ServerChan3",
    description="ServerChan3 Provider",
    notifier_params=NotifierParams,
    notify_params=NotifyParams,
    extra={},
)


class ServerChan3(BasePushProvider):
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
            f"https://{self._notifier_params.uid}.push.ft07.com/send/{self._notifier_params.sendkey}.send",
            json=json.loads(notify_params.model_dump_json()),
        )
        try:
            if json.loads(response.text)["code"] != 0:
                logger.error(f"ServerChan3 Push error, detail:{response.text}")
                return False
            else:
                return True
        except Exception as e:
            logger.error(
                f"ServerChan3 Push error, detail:{e}, response detail: {response.text}"
            )
            return False
