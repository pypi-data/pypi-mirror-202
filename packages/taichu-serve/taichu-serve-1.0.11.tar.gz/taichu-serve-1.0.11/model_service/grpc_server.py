import logging
import traceback

from grpc import RpcError

import grpc_predict_v2_pb2_grpc
import grpc_predict_v2_pb2
from app import get_model_service

from error_code import ModelNotFoundError, ModelPredictError
from common import grpc_interceptor

logger = logging.getLogger(__name__)


def parameters_to_dict(parameters):
    dic = {}

    for key, value in parameters.items():
        if value.HasField('int64_param'):
            dic[key] = value.int64_param
        elif value.HasField('bool_param'):
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
                resp.parameters[key].int64_param = value
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
        ctx = {}
        rec_dict = parameters_to_dict(request.parameters)
        instance = get_model_service(request.model_name, request.model_version)
        try:
            ret = instance.inference(rec_dict, context=ctx)
        except Exception as e:
            logger.error('Algorithm crashed!')
            logger.error(traceback.format_exc())
            raise ModelPredictError(message=str(e))
        resp = self.make_response(ret)
        resp.model_name = request.model_name
        resp.model_version = request.model_version

        return resp

    @grpc_interceptor
    def ModelStreamInfer(self, request, context):
        # 检测是否有客户端断开连接
        ctx = {}
        while context.is_active():
            for req in request:
                # logger.info('recv: %s', req)
                ctx['model_name'] = req.model_name
                ctx['model_version'] = req.model_version

                instance = get_model_service(req.model_name, req.model_version)

                rec_dict = parameters_to_dict(req.parameters)

                try:
                    res = instance.inference(rec_dict, context=ctx)
                except Exception as e:
                    logger.error('Algorithm crashed!, %s', str(e))
                    logger.error(traceback.format_exc())
                    raise ModelPredictError(message=str(e))

                # logger.info('ret: %s', res)
                resp = self.make_response(res)
                resp.model_name = req.model_name
                resp.model_version = req.model_version

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
