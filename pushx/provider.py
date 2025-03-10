from dataclasses import dataclass, field
from typing import Any, Type, Optional, Dict
from pydantic import BaseModel
from abc import ABC, abstractmethod


class PushResult(BaseModel):
    success: bool
    """是否成功"""
    code: int
    """状态码"""
    msg: str = None
    """具体信息"""
    data: Optional[Any] = None
    """可能的数据"""


class BaseNotifyParams(BaseModel):
    pass


class BaseNotifierParams(BaseModel):
    pass


class BasePushProvider(ABC):
    _notifier_params: BaseNotifierParams

    @abstractmethod
    def _notify(
        self, params: Optional[BaseNotifyParams] = None, **kwargs
    ) -> PushResult:
        """
        发送通知的抽象方法

        :param params: 通知参数对象
        :param kwargs: 通知参数关键字参数
        :return: 推送结果
        """
        pass

    @abstractmethod
    def _set_notifier_params(self, params: Optional[NotifierParams] = None, **kwargs) -> None:
        """
        设置通知器参数的抽象方法

        :param params: 通知器参数对象
        :param kwargs: 通知器参数关键字参数
        """
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
    notifier_params: Type[BaseNotifierParams]
    """Notifier 所需参数"""
    notify_params: Type[BaseNotifyParams]
    """Notify 所需参数"""
    extra: Dict[Any, Any] = field(default_factory=dict)
    """额外信息，可自由定义"""
