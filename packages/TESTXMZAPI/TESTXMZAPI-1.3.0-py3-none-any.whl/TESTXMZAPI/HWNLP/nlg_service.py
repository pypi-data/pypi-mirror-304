from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdknlp.v2 import (
    RunPoemRequest,
    CreatePoem,
    RunSummaryRequest,
    SummaryReq,
    RunSummaryDomainRequest,
    SummaryDomainReq,
)
from .auth_config import get_nlp_client
from ..KVS import LogHandler

log = LogHandler()


class NLGService:
    """
    自然语言生成服务类，提供诗歌生成和文本摘要功能。
    """

    def __init__(self):
        self.client = get_nlp_client()  # 初始化NLP客户端

    def poem(self, title, type, acrostic=False):
        """
        生成诗歌。
        :param title: 诗歌标题,不能为空
        :param type: 诗歌类型，默认为0
        :param acrostic: 是否为藏头诗，默认为false
        :return: 生成的诗歌内容
        """
        if not title:
            raise ValueError("title为必须参数")
        type = type or 0
        acrostic = acrostic or "false"
        try:
            request = RunPoemRequest()
            request.body = CreatePoem(acrostic=acrostic, type=type, title=title)
            response = self.client.run_poem(request)
            log.process_log(response.to_dict(), "诗歌生成", tracer=self.tracer)
            return response.to_dict()
        except exceptions.ClientRequestException as e:
            print_error(e)
            return None

    def summary(self, content, lang="zh", length_limit=0.3, title=None):
        """
        生成文本摘要。

        :param content: 原始文本内容,不能为空
        :param lang: 语言,默认为zh
        :param length_limit: 摘要长度限制,默认为0.3
        :param title: 文本标题,默认为0
        :return: 文本摘要内容
        """
        if not content:
            raise ValueError("content为必须参数")
        title = title or "0"
        lang = lang or "zh"
        length_limit = length_limit or 0.3
        try:
            request = RunSummaryRequest()
            request.body = SummaryReq(
                title=title, length_limit=length_limit, lang=lang, content=content
            )
            response = self.client.run_summary(request)
            return response.to_dict()
        except exceptions.ClientRequestException as e:
            print_error(e)
            return None

    def summary_domain(self, content, lang="zh", length_limit=None, title=None, type=0):
        """
        生成领域特定文本摘要。

        :param content: 原始文本内容,不能为空
        :param lang: 语言,默认为zh
        :param length_limit: 摘要长度限制,默默认为0.3
        :param title: 文本标题,默认为0
        :param type: 领域类型,默认为0
        :return: 领域特定文本摘要内容
        """
        if not content:
            raise ValueError("content为必须参数")
        title = title or "0"
        lang = lang or "zh"
        length_limit = length_limit or 0.3
        try:
            request = RunSummaryDomainRequest()
            request.body = SummaryDomainReq(
                type=type,
                content=content,
                lang=lang,
                title=title,
                length_limit=length_limit,
            )
            response = self.client.run_summary_domain(request)
            return response.to_dict()
        except exceptions.ClientRequestException as e:
            print_error(e)
            return None


def print_error(e):
    """
    打印错误信息。

    :param e: 异常实例
    """
    for attr in ["status_code", "request_id", "error_code", "error_msg"]:
        value = getattr(e, attr)
        if value is not None:
            print(f"{attr}: {value}")


def __enter__(self):
    """
    在进入 with 语句块时调用。
    这个方法允许在 with 语句块执行之前执行一些初始化工作。
    在 with 语句块执行完毕后，会自动调用 __exit__() 方法。
    返回的是实例本身，这样在 with 语句块中可以直接使用实例的方法和属性。
    """
    return self


def __exit__(self, exc_type, exc_val, exc_tb):
    """
    在退出 with 语句块时调用。
    无论 with 语句块中的代码是否成功执行，都会调用此方法。
    :param exc_type: 异常类型，如果 with 块中没有发生异常，则为 None。
    :param exc_val: 异常值，如果 with 块中没有发生异常，则为 None。
    :param exc_tb: 异常的 traceback 对象，如果 with 块中没有发生异常，则为 None。
    :return: 如果返回 False 或 None，则异常会正常抛出。
            如果返回 True，则异常会被抑制（不推荐这么做，除非有充分的理由）。
    """
    self.configurator.shutdown()
