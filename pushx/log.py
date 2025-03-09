from os import PathLike
from loguru import logger
import sys

logger.remove()


def configure_logging(
    enable: bool = False,
    level: str = "INFO",
    log_to_console: bool = True,
    log_file: str | PathLike[str] = None,
    rotation: str = "10 MB",
    retention: str = "1 week",
    log_format: str = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> - <lvl>{level:^8}</> - <cyan>{name:^12}</cyan> : <cyan>{module:^7}</cyan> : <cyan>{line:^4}</cyan> - <lvl>{message}</>",
) -> logger:
    """
    配置日志记录器。

    :param enable: 是否启用日志记录
    :param level: 日志级别 ("TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL")
    :param log_to_console: 是否输出到控制台
    :param log_file: 日志文件路径，如果为 None 则不记录到文件
    :param rotation: 日志轮转条件，例如 "10 MB", "1 day", "1 week"
    :param retention: 保留历史日志的时间
    :param log_format: 日志格式
    :return: logger 对象
    """
    # 确保移除所有现有的处理器
    logger.remove()

    if not enable:
        # 如果不启用日志，仅返回logger
        return logger

    # 添加控制台处理器
    if log_to_console:
        logger.add(sys.stderr, level=level, format=log_format)

    # 添加文件处理器
    if log_file:
        logger.add(
            log_file,
            rotation=rotation,  # 轮转条件
            retention=retention,  # 保留策略
            level=level,
            format=log_format,
        )

    return logger
