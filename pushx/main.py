import types
from loguru import logger

from pushx import providers
from pushx.provider import BaseProviderParams, PushResult


class Notifier:
    """
    初始化一个 Notifier

    :param provider: Push Provider
    :param kwargs: 参数，根据 provider 的 `__provider_meta__.notifier_params` 定义
    """

    def __init__(self, provider: types.ModuleType | str, **kwargs):
        try:
            if isinstance(provider, str):
                try:
                    provider = getattr(providers, provider)
                except AttributeError:
                    raise ValueError(f"Provider '{provider}' not found.")
            _meta = getattr(provider, "__provider_meta__")
            cls = getattr(provider, _meta.class_name)
            self.provider = cls()
            logger.info(f"Provider '{provider}' initialized.")
            self.provider._set_notifier_params(**kwargs)
        except Exception as e:
            logger.error(f"Failed to initialize notifier: {str(e)}")
            raise

    def notify(self, params: BaseProviderParams = None, **kwargs) -> PushResult:
        """
        notify 发送通知

        :param params: 通过 provider 的 `__provider_meta__.notify_params` 构建
        :param kwargs: 参数，根据 provider 的 `__provider_meta__.notify_params` 定义
        :return: PushResult
        :rtype: PushResult
        """
        try:
            result = self.provider._notify(params, **kwargs)
            if result.success:
                logger.debug(f"Notification sent successfully: {result.code}")
            else:
                logger.warning(f"Notification failed: {result.code}, {result.msg}")
            return result
        except Exception as e:
            logger.error(f"Error sending notification: {str(e)}")
            return PushResult(success=False, code=500, msg=f"Internal error: {str(e)}")
