# coding: utf-8
import logging
from concurrent import futures

import grpc

from model_service.grpc_predict_v2_pb2_grpc import add_GRPCInferenceServiceServicer_to_server
from model_service.app import app, init_model_service_instance
from model_service.error_code import ModelNotFoundError
from model_service.grpc_server import GrpcModelService
from model_service.ratelimiter import semaphore
from model_service.settings import parse_args

LOGGER = logging.getLogger(__name__)


class GrpcServerInterceptor(grpc.ServerInterceptor):
    def intercept_service(self, continuation, handler_call_details):
        try:
            LOGGER.info("grpc request: %s", handler_call_details)
            # 跳过health check
            if handler_call_details.method == "/taichu_infer.GRPCInferenceService/ServerLive" or \
                    handler_call_details.method == "/taichu_infer.GRPCInferenceService/ServerReady":
                return continuation(handler_call_details)

            ok = semaphore.acquire(blocking=True, timeout=1)
            if not ok:
                return grpc.RpcError(grpc.StatusCode.RESOURCE_EXHAUSTED, "Too many requests")
            return continuation(handler_call_details)

        except ModelNotFoundError as e:

            return grpc.RpcError(grpc.StatusCode.NOT_FOUND, e.message)
        finally:
            if ok:
                semaphore.release()


def infer_server_start():
    args = parse_args()
    init_model_service_instance()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=args.workers),
                         maximum_concurrent_rpcs=args.max_concurrent_requests,
                         interceptors=[GrpcServerInterceptor()])

    add_GRPCInferenceServiceServicer_to_server(GrpcModelService(), server)
    server.add_insecure_port(f'[::]:{args.grpc_port}')

    server.start()
    LOGGER.info("grpc server start at port %s", args.grpc_port)
    # server.wait_for_termination()
    app.run(host='0.0.0.0', port=args.http_port)
