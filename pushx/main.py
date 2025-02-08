import types


class Notifier:
    def __init__(self, provider: types.ModuleType, **kwargs):
        """
        初始化一个 Notifier
        :param provider_name: Push Provider
        :param kwargs: 参数，根据 provider 的 `__provider_meta__.notifier_params` 定义
        """
        _meta = getattr(provider, "__provider_meta__")
        cls = getattr(provider, _meta.class_name)
        self.provider = cls()
        self.provider._set_notifier_params(**kwargs)

    def notify(self, **kwargs):
        """
        初始化一个 Notifier
        :param kwargs: 参数，根据 provider 的 `__provider_meta__.notify_params` 定义
        """
        return self.provider._notify(**kwargs)
