from __future__ import print_function

import logging
import time

import grpc
import grpc_predict_v2_pb2
import grpc_predict_v2_pb2_grpc


def guide_list_features(stub):
    num = 10

    while True:

        def generator():
            while True:

                req = grpc_predict_v2_pb2.ModelInferRequest()
                req.model_name = 'test'
                req.model_version = '1'
                req.id = '1'

                req.parameters['input'].int64_param = num
                yield req

                time.sleep(1)

        resp = stub.ModelStreamInfer(generator())
        print(resp)
        for feature in resp:
            print(feature)
            time.sleep(1)

    # for feature in features:  #流式返回的结果
    #     now = time.localtime()
    #     now_time = time.strftime("%Y-%m-%d %H:%M:%S", now)
    #     print('time:', now_time)
    #     print('receive',feature.reply)


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:8889') as channel:
        stub = grpc_predict_v2_pb2_grpc.GRPCInferenceServiceStub(channel)
        # print("-------------- GetFeature --------------")
        # guide_get_feature(stub)
        print("-------------- ListFeatures --------------")
        guide_list_features(stub)
        # print("-------------- RecordRoute --------------")
        # guide_record_route(stub)
        # print("-------------- RouteChat --------------")
        # guide_route_chat(stub)


if __name__ == '__main__':
    logging.basicConfig()
    run()
