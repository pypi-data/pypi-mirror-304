import json
import traceback
from datetime import datetime
import requests
from obs import ObsClient


def generate_log_filename(sdk_name):
    """
    生成日志文件名。

    :param sdk_name: SDK名称。
    :return: 生成的日志文件名和当前时间。
    """
    # 获取当前时间
    now = datetime.now()
    # 格式化时间为 "年-月-日 时：分：秒" 的形式
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    json_name = f"{sdk_name}_{formatted_time}.json"
    return json_name, formatted_time


def send_log(sdk_name, log_content):
    """
    发送日志到日志服务器。

    :param sdk_name: SDK名称。
    :param log_content: 日志内容。
    """
    # 目标URL
    url = "http://nodered.glwsq.cn/weixin"
    log_url = f"http://xmzsdk.mizhoubaobei.top/{log_content}"
    params = {
        "to": "tlhjwqdoud",
        "body": f"有人在{log_content}使用了接口{sdk_name}，具体日志为{log_url}",
    }
    requests.get(url, params=params)


class LogHandler:
    def __init__(self, ak=None, sk=None, server=None, bucket_name=None):
        """
        初始化LogHandler类。

        :param ak: 访问密钥AK。
        :param sk: 访问密钥SK。
        :param server: OBS服务器地址。
        :param bucket_name: OBS存储桶名称。
        """
        self.ak = "CHRZSAE9JCAZCZRVQNNT"
        self.sk = "Q2lFSm4QAxUiWtQHEIK0bTU5jURc8dvi27rVHv1u"
        self.server = "obs.cn-east-3.myhuaweicloud.com"
        self.bucket_name = "xmzsdk"

    def get_ip_location(self):
        """
        获取IP地理位置信息。

        :return: IP地理位置信息的JSON数据。
        """
        url = "https://webapi-pc.meitu.com/common/ip_location"
        response = requests.get(url)
        return response.json()

    def merge_and_format_json(self, json_str1, json_str2):
        """
        合并两个JSON字符串，并返回格式化后的JSON字符串。

        :param json_str1: 第一个JSON字符串。
        :param json_str2: 第二个JSON字符串或字典。
        :return: 格式化后的合并JSON字符串。
        """

        def deep_merge(x, m):
            """递归地合并两个字典，适配嵌套字典。"""
            merged_dict = x.copy()
            for key, value in m.items():
                if (
                    key in merged_dict
                    and isinstance(merged_dict[key], dict)
                    and isinstance(value, dict)
                ):
                    merged_dict[key] = deep_merge(merged_dict[key], value)
                else:
                    merged_dict[key] = value
            return merged_dict

        # 将第一个JSON字符串解析为字典
        dict1 = json.loads(json_str1) if isinstance(json_str1, str) else json_str1

        # 如果第二个参数是字符串，则解析为字典
        dict2 = json.loads(json_str2) if isinstance(json_str2, str) else json_str2

        # 使用函数合并两个字典
        combined_dict = deep_merge(dict1, dict2)

        # 将合并后的字典转换为格式化的JSON字符串
        formatted_json = json.dumps(combined_dict, indent=4)
        return formatted_json

    def put_content_to_obs(self, object_name, content):
        """
        将内容上传到OBS。

        :param object_name: OBS对象名称。
        :param content: 要上传的内容。
        :return: 上传结果。
        """
        # 创建ObsClient实例
        obs_client = ObsClient(
            access_key_id=self.ak, secret_access_key=self.sk, server=self.server
        )
        try:
            # 上传文本对象
            resp = obs_client.putContent(self.bucket_name, object_name, content)
            # 检查上传是否成功
            if resp.status < 300:
                return {
                    "message": "Put Content Succeeded",
                    "requestId": resp.requestId,
                    "etag": resp.body.etag,
                }
            else:
                return {
                    "message": "Put Content Failed",
                    "requestId": resp.requestId,
                    "errorCode": resp.errorCode,
                    "errorMessage": resp.errorMessage,
                }
        except Exception as e:
            print("Put Content Failed")
            print(traceback.format_exc())
            print(e)
            return None

    def merge_and_format_json(self, json_str1, json_str2):
        """
        合并两个JSON字符串，并返回格式化后的JSON字符串。

        :param json_str1: 第一个JSON字符串。
        :param json_str2: 第二个JSON字符串。
        :return: 格式化后的合并JSON字符串。
        """

    def process_log(self, additional_data, sdk_name):
        """
        处理日志，包括获取IP位置信息，合并日志数据，上传到OBS，发送日志通知。

        :param additional_data: 额外的日志数据。
        :param sdk_name: SDK名称。
        """
        ip_data = self.get_ip_location()
        merged_data = self.merge_and_format_json(json.dumps(ip_data), additional_data)
        log_filename, log_time = generate_log_filename(sdk_name)
        upload_result = self.put_content_to_obs(log_filename, merged_data)
        if upload_result:
            send_log(sdk_name, log_time)
        else:
            print("日志上传成功.")
