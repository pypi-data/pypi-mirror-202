# coding: utf-8

import re
import six



from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class VideoTranslateTaskInputData:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'bucket': 'str',
        'path': 'str',
        'url': 'str',
        'key': 'str'
    }

    attribute_map = {
        'bucket': 'bucket',
        'path': 'path',
        'url': 'url',
        'key': 'key'
    }

    def __init__(self, bucket=None, path=None, url=None, key=None):
        """VideoTranslateTaskInputData

        The model defined in huaweicloud sdk

        :param bucket: OBS桶名，当输入为obs类型时必填。
        :type bucket: str
        :param path: OBS的路径，当输入为obs类型时必填。
        :type path: str
        :param url: url输入源的地址，当输入为url类型时必填。 长度不超过1000。
        :type url: str
        :param key: 数据标识。多输入场景下必选，值由算法定义；单输入场景非必选。视频翻译场景，输入视频key为video；音频文件为audio；字幕文件为subtitle
        :type key: str
        """
        
        

        self._bucket = None
        self._path = None
        self._url = None
        self._key = None
        self.discriminator = None

        if bucket is not None:
            self.bucket = bucket
        if path is not None:
            self.path = path
        if url is not None:
            self.url = url
        if key is not None:
            self.key = key

    @property
    def bucket(self):
        """Gets the bucket of this VideoTranslateTaskInputData.

        OBS桶名，当输入为obs类型时必填。

        :return: The bucket of this VideoTranslateTaskInputData.
        :rtype: str
        """
        return self._bucket

    @bucket.setter
    def bucket(self, bucket):
        """Sets the bucket of this VideoTranslateTaskInputData.

        OBS桶名，当输入为obs类型时必填。

        :param bucket: The bucket of this VideoTranslateTaskInputData.
        :type bucket: str
        """
        self._bucket = bucket

    @property
    def path(self):
        """Gets the path of this VideoTranslateTaskInputData.

        OBS的路径，当输入为obs类型时必填。

        :return: The path of this VideoTranslateTaskInputData.
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, path):
        """Sets the path of this VideoTranslateTaskInputData.

        OBS的路径，当输入为obs类型时必填。

        :param path: The path of this VideoTranslateTaskInputData.
        :type path: str
        """
        self._path = path

    @property
    def url(self):
        """Gets the url of this VideoTranslateTaskInputData.

        url输入源的地址，当输入为url类型时必填。 长度不超过1000。

        :return: The url of this VideoTranslateTaskInputData.
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this VideoTranslateTaskInputData.

        url输入源的地址，当输入为url类型时必填。 长度不超过1000。

        :param url: The url of this VideoTranslateTaskInputData.
        :type url: str
        """
        self._url = url

    @property
    def key(self):
        """Gets the key of this VideoTranslateTaskInputData.

        数据标识。多输入场景下必选，值由算法定义；单输入场景非必选。视频翻译场景，输入视频key为video；音频文件为audio；字幕文件为subtitle

        :return: The key of this VideoTranslateTaskInputData.
        :rtype: str
        """
        return self._key

    @key.setter
    def key(self, key):
        """Sets the key of this VideoTranslateTaskInputData.

        数据标识。多输入场景下必选，值由算法定义；单输入场景非必选。视频翻译场景，输入视频key为video；音频文件为audio；字幕文件为subtitle

        :param key: The key of this VideoTranslateTaskInputData.
        :type key: str
        """
        self._key = key

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                if attr in self.sensitive_list:
                    result[attr] = "****"
                else:
                    result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        import simplejson as json
        if six.PY2:
            import sys
            reload(sys)
            sys.setdefaultencoding("utf-8")
        return json.dumps(sanitize_for_serialization(self), ensure_ascii=False)

    def __repr__(self):
        """For `print`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, VideoTranslateTaskInputData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
