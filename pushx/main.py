import types

from pushx.provider import BaseProviderParams, PushResult


class Notifier:
    """
    初始化一个 Notifier

    :param provider: Push Provider
    :param kwargs: 参数，根据 provider 的 `__provider_meta__.notifier_params` 定义
    """

    def __init__(self, provider: types.ModuleType, **kwargs):
        _meta = getattr(provider, "__provider_meta__")
        cls = getattr(provider, _meta.class_name)
        self.provider = cls()
        self.provider._set_notifier_params(**kwargs)

    def notify(self, params: BaseProviderParams = None, **kwargs) -> PushResult:
        """
        notify 发送通知

        :param params: 通过 provider 的 `__provider_meta__.notify_params` 构建
        :param kwargs: 参数，根据 provider 的 `__provider_meta__.notify_params` 定义
        :return: PushResult
        :rtype: PushResult
        """
        return self.provider._notify(params, **kwargs)
