# _*_coding:utf-8_*_

from rest_framework.views import APIView

from ..services.flow_basic_service import FlowBasicService
from ..utils.custom_response import util_response
from ..utils.request_params_wrapper import request_params_wrapper


class FlowNodeToActionList(APIView):
    @request_params_wrapper
    def get(self, *args, request_params=None, **kwargs):
        """
        流程作业
        """
        if request_params is None:
            request_params = {}
        flow_list, error_text = FlowBasicService.get_flow_node_to_action_list(params=request_params)

        return util_response(data=flow_list)
