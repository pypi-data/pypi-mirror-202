# coding: utf-8
import logging
import sys
import argparse
import os
import time
import uuid
from concurrent import futures

from gunicorn.app.wsgiapp import WSGIApplication

import grpc
import grpc_predict_v2_pb2_grpc

from app import app
from error_code import ModelNotFoundError
from grpc_server import GrpcModelService


LOGGER = logging.getLogger(__name__)


class MyUnaryServerInterceptor(grpc.ServerInterceptor):
    def intercept_service(self, continuation, handler_call_details):
        try:
            ret = continuation(handler_call_details)
        except ModelNotFoundError as e:

            return grpc.RpcError(grpc.StatusCode.NOT_FOUND, e.message)
        return ret


def infer_server_start():
    parser = argparse.ArgumentParser(description='Taichu Model Server')
    parser.add_argument('--grpc_port', action="store", default=8889, type=int)
    parser.add_argument('--http_port', action="store", default=8888, type=int)
    parser.add_argument('--worker', action="store", default=100, type=int)

    args = parser.parse_args()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=args.worker),
                         maximum_concurrent_rpcs=args.worker,
                         interceptors=[MyUnaryServerInterceptor()])
    grpc_predict_v2_pb2_grpc.add_GRPCInferenceServiceServicer_to_server(GrpcModelService(), server)
    server.add_insecure_port(f'[::]:{args.grpc_port}')

    server.start()
    LOGGER.info("grpc server start at port %s", args.grpc_port)
    # server.wait_for_termination()

    app.run(host='0.0.0.0', port=args.http_port)
