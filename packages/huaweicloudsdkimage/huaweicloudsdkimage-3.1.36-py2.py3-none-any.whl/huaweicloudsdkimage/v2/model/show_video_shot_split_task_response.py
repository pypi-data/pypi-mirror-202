# coding: utf-8

import re
import six


from huaweicloudsdkcore.sdk_response import SdkResponse
from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class ShowVideoShotSplitTaskResponse(SdkResponse):

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'task_id': 'str',
        'create_time': 'str',
        'update_time': 'str',
        'state': 'str',
        'input': 'VideoSplitTaskInput',
        'output': 'TaskOutput',
        'param_callback': 'TaskCallback',
        'x_request_id': 'str'
    }

    attribute_map = {
        'task_id': 'task_id',
        'create_time': 'create_time',
        'update_time': 'update_time',
        'state': 'state',
        'input': 'input',
        'output': 'output',
        'param_callback': 'callback',
        'x_request_id': 'X-request-id'
    }

    def __init__(self, task_id=None, create_time=None, update_time=None, state=None, input=None, output=None, param_callback=None, x_request_id=None):
        """ShowVideoShotSplitTaskResponse

        The model defined in huaweicloud sdk

        :param task_id: 任务id
        :type task_id: str
        :param create_time: 任务创建时间，格式为ISO8601：YYYY-MM-DDThh:mm:ssZ
        :type create_time: str
        :param update_time: 任务更新时间，格式为ISO8601：YYYY-MM-DDThh:mm:ssZ
        :type update_time: str
        :param state: 任务当前的状态，分别为SUCCEEDED（运行成功），FAILED（运行失败），RUNNING（运行中）。
        :type state: str
        :param input: 
        :type input: :class:`huaweicloudsdkimage.v2.VideoSplitTaskInput`
        :param output: 
        :type output: :class:`huaweicloudsdkimage.v2.TaskOutput`
        :param param_callback: 
        :type param_callback: :class:`huaweicloudsdkimage.v2.TaskCallback`
        :param x_request_id: 
        :type x_request_id: str
        """
        
        super(ShowVideoShotSplitTaskResponse, self).__init__()

        self._task_id = None
        self._create_time = None
        self._update_time = None
        self._state = None
        self._input = None
        self._output = None
        self._param_callback = None
        self._x_request_id = None
        self.discriminator = None

        if task_id is not None:
            self.task_id = task_id
        if create_time is not None:
            self.create_time = create_time
        if update_time is not None:
            self.update_time = update_time
        if state is not None:
            self.state = state
        if input is not None:
            self.input = input
        if output is not None:
            self.output = output
        if param_callback is not None:
            self.param_callback = param_callback
        if x_request_id is not None:
            self.x_request_id = x_request_id

    @property
    def task_id(self):
        """Gets the task_id of this ShowVideoShotSplitTaskResponse.

        任务id

        :return: The task_id of this ShowVideoShotSplitTaskResponse.
        :rtype: str
        """
        return self._task_id

    @task_id.setter
    def task_id(self, task_id):
        """Sets the task_id of this ShowVideoShotSplitTaskResponse.

        任务id

        :param task_id: The task_id of this ShowVideoShotSplitTaskResponse.
        :type task_id: str
        """
        self._task_id = task_id

    @property
    def create_time(self):
        """Gets the create_time of this ShowVideoShotSplitTaskResponse.

        任务创建时间，格式为ISO8601：YYYY-MM-DDThh:mm:ssZ

        :return: The create_time of this ShowVideoShotSplitTaskResponse.
        :rtype: str
        """
        return self._create_time

    @create_time.setter
    def create_time(self, create_time):
        """Sets the create_time of this ShowVideoShotSplitTaskResponse.

        任务创建时间，格式为ISO8601：YYYY-MM-DDThh:mm:ssZ

        :param create_time: The create_time of this ShowVideoShotSplitTaskResponse.
        :type create_time: str
        """
        self._create_time = create_time

    @property
    def update_time(self):
        """Gets the update_time of this ShowVideoShotSplitTaskResponse.

        任务更新时间，格式为ISO8601：YYYY-MM-DDThh:mm:ssZ

        :return: The update_time of this ShowVideoShotSplitTaskResponse.
        :rtype: str
        """
        return self._update_time

    @update_time.setter
    def update_time(self, update_time):
        """Sets the update_time of this ShowVideoShotSplitTaskResponse.

        任务更新时间，格式为ISO8601：YYYY-MM-DDThh:mm:ssZ

        :param update_time: The update_time of this ShowVideoShotSplitTaskResponse.
        :type update_time: str
        """
        self._update_time = update_time

    @property
    def state(self):
        """Gets the state of this ShowVideoShotSplitTaskResponse.

        任务当前的状态，分别为SUCCEEDED（运行成功），FAILED（运行失败），RUNNING（运行中）。

        :return: The state of this ShowVideoShotSplitTaskResponse.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this ShowVideoShotSplitTaskResponse.

        任务当前的状态，分别为SUCCEEDED（运行成功），FAILED（运行失败），RUNNING（运行中）。

        :param state: The state of this ShowVideoShotSplitTaskResponse.
        :type state: str
        """
        self._state = state

    @property
    def input(self):
        """Gets the input of this ShowVideoShotSplitTaskResponse.

        :return: The input of this ShowVideoShotSplitTaskResponse.
        :rtype: :class:`huaweicloudsdkimage.v2.VideoSplitTaskInput`
        """
        return self._input

    @input.setter
    def input(self, input):
        """Sets the input of this ShowVideoShotSplitTaskResponse.

        :param input: The input of this ShowVideoShotSplitTaskResponse.
        :type input: :class:`huaweicloudsdkimage.v2.VideoSplitTaskInput`
        """
        self._input = input

    @property
    def output(self):
        """Gets the output of this ShowVideoShotSplitTaskResponse.

        :return: The output of this ShowVideoShotSplitTaskResponse.
        :rtype: :class:`huaweicloudsdkimage.v2.TaskOutput`
        """
        return self._output

    @output.setter
    def output(self, output):
        """Sets the output of this ShowVideoShotSplitTaskResponse.

        :param output: The output of this ShowVideoShotSplitTaskResponse.
        :type output: :class:`huaweicloudsdkimage.v2.TaskOutput`
        """
        self._output = output

    @property
    def param_callback(self):
        """Gets the param_callback of this ShowVideoShotSplitTaskResponse.

        :return: The param_callback of this ShowVideoShotSplitTaskResponse.
        :rtype: :class:`huaweicloudsdkimage.v2.TaskCallback`
        """
        return self._param_callback

    @param_callback.setter
    def param_callback(self, param_callback):
        """Sets the param_callback of this ShowVideoShotSplitTaskResponse.

        :param param_callback: The param_callback of this ShowVideoShotSplitTaskResponse.
        :type param_callback: :class:`huaweicloudsdkimage.v2.TaskCallback`
        """
        self._param_callback = param_callback

    @property
    def x_request_id(self):
        """Gets the x_request_id of this ShowVideoShotSplitTaskResponse.

        :return: The x_request_id of this ShowVideoShotSplitTaskResponse.
        :rtype: str
        """
        return self._x_request_id

    @x_request_id.setter
    def x_request_id(self, x_request_id):
        """Sets the x_request_id of this ShowVideoShotSplitTaskResponse.

        :param x_request_id: The x_request_id of this ShowVideoShotSplitTaskResponse.
        :type x_request_id: str
        """
        self._x_request_id = x_request_id

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
        if not isinstance(other, ShowVideoShotSplitTaskResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
