import logging
import traceback
import uuid

from grpc import RpcError

import taichu_serve.grpc_predict_v2_pb2_grpc as grpc_predict_v2_pb2_grpc
import taichu_serve.grpc_predict_v2_pb2 as grpc_predict_v2_pb2
from taichu_serve.app import model_inference

from taichu_serve.error_code import ModelNotFoundError, ModelPredictError
from taichu_serve.common import grpc_interceptor

logger = logging.getLogger(__name__)


def parameters_to_dict(parameters):
    dic = {}

    for key, value in parameters.items():
        if value.HasField('bool_param'):
            dic[key] = value.bool_param
        elif value.HasField('float_param'):
            dic[key] = value.float_param
        elif value.HasField('string_param'):
            dic[key] = value.string_param
        else:
            print('error type: ', type(value))

    return dic


class GrpcModelService(grpc_predict_v2_pb2_grpc.GRPCInferenceServiceServicer):

    def __init__(self):
        logger.info('init grpc server')

    def make_response(self, dic):
        resp = grpc_predict_v2_pb2.ModelInferResponse()

        if dic is None:
            return resp

        for key, value in dic.items():
            if type(value) == int:
                resp.parameters[key].float_param = float(value)
            elif type(value) == bool:
                resp.parameters[key].bool_param = value
            elif type(value) == float:
                resp.parameters[key].float_param = value
            elif type(value) == str:
                resp.parameters[key].string_param = value
            else:
                print('error type: ', type(value))

        return resp

    @grpc_interceptor
    def ModelInfer(self, request, context):
        request_id = str(uuid.uuid4())
        rec_dict = parameters_to_dict(request.parameters)
        try:
            ret = model_inference(request.model_name, request.model_version, rec_dict, request_id)
        except Exception as e:
            logger.error('Algorithm crashed!')
            logger.error(traceback.format_exc())
            raise ModelPredictError(message=str(e))
        resp = self.make_response(ret)
        resp.model_name = request.model_name
        resp.model_version = request.model_version
        resp.id = request.id

        return resp

    @grpc_interceptor
    def ModelStreamInfer(self, request, context):
        # 检测是否有客户端断开连接
        request_id = str(uuid.uuid4())

        while context.is_active():
            for req in request:
                logger.info('recv a request')
                if req.id and len(req.id) > 0:
                    request_id = req.id

                rec_dict = parameters_to_dict(req.parameters)
                try:
                    res = model_inference(req.model_name, req.model_version, rec_dict, request_id)
                except Exception as e:
                    logger.error('Algorithm crashed!, %s', str(e))
                    logger.error(traceback.format_exc())
                    raise ModelPredictError(message=str(e))


                resp = self.make_response(res)
                resp.model_name = req.model_name
                resp.model_version = req.model_version
                resp.id = request_id

                yield resp

    def ServerLive(self, request, context):
        resp = grpc_predict_v2_pb2.ServerLiveResponse(
            live=True,
        )
        return resp

    def ServerReady(self, request, context):
        resp = grpc_predict_v2_pb2.ServerReadyResponse(
            ready=True,
        )
        return resp
