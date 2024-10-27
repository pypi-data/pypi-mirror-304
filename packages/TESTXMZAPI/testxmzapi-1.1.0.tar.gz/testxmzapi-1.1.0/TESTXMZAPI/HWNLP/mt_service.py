from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdknlp.v2 import (
    RunFileTranslationRequest,
    FileTranslationReq,
    RunGetFileTranslationResultRequest,
    RunLanguageDetectionRequest,
    LanguageDetectionReq,
    RunTextTranslationRequest,
    TextTranslationReq,
)

from XMZ.TESTXMZAPI.APM import OpenTelemetryConfigurator, get_tracer
from XMZ.TESTXMZAPI.KVS import LogHandler
from .auth_config import get_nlp_client

log = LogHandler()


class MTService:
    """
    机器翻译服务类，提供文本翻译和文档翻译功能。
    """

    def __init__(self):
        self.client = get_nlp_client()  # 初始化NLP客户端
        # 创建 OpenTelemetryConfigurator 实例
        self.configurator = OpenTelemetryConfigurator(
            host_name="MTService",
            service_name="XMZSDK",
            service_version="1.0.0",
            deployment_environment="prod",
            endpoint="http://tracing-analysis-dc-sh.aliyuncs.com/adapt_i8ucd7m6kr@c81a1d4e5cb019a_i8ucd7m6kr@53df7ad2afe8301/api/otlp/traces",
        )
        # 初始化 OpenTelemetry
        self.configurator.init_opentelemetry()
        # 获取 Tracer 实例
        self.tracer = get_tracer()

    def file_translation(self, url, file_type, lang_from, lang_to):
        """
        文档翻译接口。

        :param url: 文档的URL
        :param file_type: 文档类型,默认为docx
        :param lang_from: 源语言,默认为zh
        :param lang_to: 目标语言,默认为en
        :return: 翻译任务的响应结果
        """
        with self.tracer.start_as_current_span("file_translation") as span:
            if not url:
                raise ValueError("URL是必需的，且不能为空。")
            file_type = file_type or "docx"
            lang_to = lang_to or "zh"
            lang_from = lang_from or "en"
            span.set_attribute("url", url)
            span.set_attribute("file_type", file_type)
            try:
                request = RunFileTranslationRequest()
                request.body = FileTranslationReq(
                    type=file_type, to=lang_to, _from=lang_from, url=url
                )
                response = self.client.run_file_translation(request)
                log.process_log(response.to_dict(), "文档翻译", tracer=self.tracer)
                span.set_attribute("url", url)
                span.set_attribute("file_type", file_type)
                span.set_attribute("lang_from", lang_from)
                span.set_attribute("lang_to", lang_to)
                span.set_attribute("job_id", response.job_id)
                span.set_attribute("file_type", file_type)
                span.set_attribute("lang_from", lang_from)
                span.set_attribute("lang_to", lang_to)
                span.set_attribute("response", response.to_dict())
                span_context = span.get_span_context()
                trace_id = span_context.trace_id
                span_id = span_context.span_id
                x = response.to_dict()
                x["trace_id"] = trace_id
                x["span_id"] = span_id
                return x
            except exceptions.ClientRequestException as e:
                # 获取当前的 Span 上下文
                span_context = span.get_span_context()
                trace_id = span_context.trace_id
                span_id = span_context.span_id
                # 将 TraceID 和 SpanID 添加到错误日志中
                error_message = f"Error occurred: {str(e)}\nTrace ID: {trace_id}\nSpan ID: {span_id}"
                span.set_attribute("error", True)
                span.set_attribute("trace_id", trace_id)
                span.set_attribute("span_id", span_id)
                print_error(error_message)
                return None

    def get_file_translation_result(self, job_id):
        """
        获取文档翻译结果。

        :param job_id: 翻译任务ID，通过文档翻译接口返回即翻译任务的唯一标识符且不能为空
        :return: 文档翻译结果
        """
        with self.tracer.start_as_current_span("get_file_translation_result") as span:
            if not job_id:
                raise ValueError("Job是必需的，且不能为空。")
            try:
                request = RunGetFileTranslationResultRequest()
                request.job_id = job_id
                response = self.client.run_get_file_translation_result(request)
                log.process_log(
                    response.to_dict(), "获取文档翻译结果", tracer=self.tracer
                )
                span.set_attribute("job_id", job_id)
                span.set_attribute("response", response.to_dict())
                span.set_attribute("status_code", response.status)
                span.set_attribute("url", response.url)
                m = response.to_dict()
                span_context = span.get_span_context()
                trace_id = span_context.trace_id
                span_id = span_context.span_id
                m["trace_id"] = trace_id
                m["span_id"] = span_id
                return m
            except exceptions.ClientRequestException as e:
                span_context = span.get_span_context()
                trace_id = span_context.trace_id
                span_id = span_context.span_id
                # 将 TraceID 和 SpanID 添加到错误日志中
                error_message = f"Error occurred: {str(e)}\nTrace ID: {trace_id}\nSpan ID: {span_id}"
                span.set_attribute("error", True)
                span.set_attribute("trace_id", trace_id)
                span.set_attribute("span_id", span_id)
                print(error_message)
                return None

    def language_detection(self, text):
        """
        语种检测接口。

        :param text: 待检测的文本,不能为空
        :return: 检测结果
        """
        with self.tracer.start_as_current_span("language_detection") as span:
            if not text:
                raise ValueError("Text是必需的，且不能为空。")
            try:
                request = RunLanguageDetectionRequest()
                request.body = LanguageDetectionReq(text=text)
                response = self.client.run_language_detection(request)
                log.process_log(response.to_dict(), "语种检测", tracer=self.tracer)
                span.set_attribute("text", text)
                span.set_attribute("detected_language", response.detected_language)
                m = response.to_dict()
                span_context = span.get_span_context()
                trace_id = span_context.trace_id
                span_id = span_context.span_id
                m["trace_id"] = trace_id
                m["span_id"] = span_id
                return m
            except exceptions.ClientRequestException as e:
                span_context = span.get_span_context()
                trace_id = span_context.trace_id
                span_id = span_context.span_id
                # 将 TraceID 和 SpanID 添加到错误日志中
                error_message = f"Error occurred: {str(e)}\nTrace ID: {trace_id}\nSpan ID: {span_id}"
                span.set_attribute("error", True)
                span.set_attribute("trace_id", trace_id)
                span.set_attribute("span_id", span_id)
                print(error_message)
                return None

    def text_translation(self, text, lang_from, lang_to, scene="common"):
        """
        文本翻译接口。

        :param text: 待翻译的文本，不能为空
        :param lang_from: 源语言,默认为auto
        :param lang_to: 目标语言,默认为en
        :param scene: 翻译场景,默认为common
        :return: 翻译结果
        """
        with self.tracer.start_as_current_span("text_translation") as span:
            if not text:
                raise ValueError("Text是必需的，且不能为空。")
            lang_from = lang_from or "auto"
            lang_to = lang_to or "zh"
            scene = "common"
            try:
                request = RunTextTranslationRequest()
                request.body = TextTranslationReq(
                    scene=scene, to=lang_to, _from=lang_from, text=text
                )
                response = self.client.run_text_translation(request)
                log.process_log(response.to_dict(), "文本翻译", tracer=self.tracer)
                span.set_attribute("text", text)
                span.set_attribute("lang_from", lang_from)
                span.set_attribute("lang_to", lang_to)
                span.set_attribute("scene", scene)
                span.set_attribute("response", response.to_dict())
                span.set_attribute("src_text", response.src_text)
                span.set_attribute("translated_text", response.translated_text)
                span.set_attribute("from", response._from)
                span.set_attribute("to", response.to)
                m = response.to_dict()
                span_context = span.get_span_context()
                trace_id = span_context.trace_id
                span_id = span_context.span_id
                m["trace_id"] = trace_id
                m["span_id"] = span_id
                return m
            except exceptions.ClientRequestException as e:
                span_context = span.get_span_context()
                trace_id = span_context.trace_id
                span_id = span_context.span_id
                # 将 TraceID 和 SpanID 添加到错误日志中
                error_message = f"Error occurred: {str(e)}\nTrace ID: {trace_id}\nSpan ID: {span_id}"
                span.set_attribute("error", True)
                span.set_attribute("trace_id", trace_id)
                span.set_attribute("span_id", span_id)
                print(error_message)
                return None


def print_error(e):
    """
    打印错误信息。

    :param e: 异常实例
    """
    for attr in ["status_code", "request_id", "error_code", "error_msg"]:
        value = getattr(e, attr)
        if value is not None:
            print("{}: {}".format(attr, value))


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
