# coding: utf-8
import logging
from concurrent import futures

import grpc

from taichu_serve.grpc_predict_v2_pb2_grpc import add_GRPCInferenceServiceServicer_to_server
from taichu_serve.app import app, init_model_service_instance
from taichu_serve.error_code import ModelNotFoundError,TooManyRequestsError
from taichu_serve.grpc_server import GrpcModelService
from taichu_serve.ratelimiter import semaphore
from taichu_serve.settings import parse_args

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
        except TooManyRequestsError as e:
            return grpc.RpcError(grpc.StatusCode.RESOURCE_EXHAUSTED, "Too many requests")
        finally:
            if ok:
                semaphore.release()


def infer_server_start():
    args = parse_args()
    init_model_service_instance()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=args.max_concurrent_requests),
                         maximum_concurrent_rpcs=args.max_concurrent_requests + 5,
                         interceptors=[GrpcServerInterceptor()])

    add_GRPCInferenceServiceServicer_to_server(GrpcModelService(), server)
    server.add_insecure_port(f'[::]:{args.grpc_port}')

    server.start()
    LOGGER.info("grpc server start at port %s", args.grpc_port)
    # from gevent.pywsgi import WSGIServer
    # http_server = WSGIServer(("0.0.0.0", args.http_port), app)
    # LOGGER.info("http server start at port %s", args.http_port)
    #
    # http_server.serve_forever()
    if args.grpc_only:
        server.wait_for_termination()

    app.run("0.0.0.0", args.http_port)
    return app
