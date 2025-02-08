import json
import httpx
import logging
from typing import Union
from pushx.provider import ProviderMetadata, BasePushProvider, BaseProviderParams


logger = logging.getLogger(__name__)


# Metadata
class NotifyParams(BaseProviderParams):
    title: str
    """通知的标题"""
    content: str = None
    """通知的内容，支持 Markdown"""
    tags: str = None
    """通知的 tags"""
    short: str = None
    """通知的略缩"""


class NotifierParams(BaseProviderParams):
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
    def _set_notifier_params(self, **kwargs: Union[NotifyParams, dict]):
        if isinstance(kwargs, dict):
            self._notifier_params = NotifierParams(**kwargs)
        else:
            self._notifier_params = kwargs

    def _notify(self, **kwargs: Union[NotifyParams, dict]) -> bool:
        if isinstance(kwargs, dict):
            notify_params = NotifyParams(**kwargs)
        else:
            notify_params = kwargs
        response = httpx.post(
            f"https://{self._notifier_params.uid}.push.ft07.com/send/{self._notifier_params.sendkey}.send",
            json=json.loads(notify_params.model_dump_json()),
        )
        try:
            if json.loads(response.text)["code"] != 0:
                logger.error(f"ServerChan3 Push error ,detail:{response.text}")
                return False
            else:
                return True
        except Exception as e:
            logger.error(f"ServerChan3 Push error ,detail:{e}")
