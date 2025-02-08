from dataclasses import dataclass, field
from typing import Any, Type, Union
from pydantic import BaseModel


class BaseProviderParams(BaseModel):
    pass


class NotifyParams(BaseProviderParams):
    pass


class NotifierParams(BaseProviderParams):
    pass


class BasePushProvider:
    def _notify(self, **kwargs: Union[NotifyParams, dict]):
        pass

    def _set_notifier_params(self, **kwargs: Union[NotifierParams, dict]) -> bool:
        pass


@dataclass(eq=False)
class ProviderMetadata:
    """Provider 元数据"""

    name: str
    """Provider 名称"""
    class_name: str
    """Provider 类名"""
    description: str
    """Provider 介绍"""
    notifier_params: Type[BaseProviderParams]
    """Notifier 所需参数"""
    notify_params: Type[BaseProviderParams]
    """Notify 所需参数"""
    extra: dict[Any, Any] = field(default_factory=dict)
    """额外信息，可自由定义"""
