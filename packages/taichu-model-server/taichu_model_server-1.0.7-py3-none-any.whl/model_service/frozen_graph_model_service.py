# Copyright 2019 ModelArts Authors from Huawei Cloud. All Rights Reserved.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import os

import numpy as np
import tensorflow as tf
from PIL import Image
from tensorflow.core.protobuf.rewriter_config_pb2 import RewriterConfig

from model_service.model_service import SingleNodeService

logger = logging.getLogger(__name__)


def is_davinci_device():
    for file in os.listdir("/dev"):
        if file.startswith("davinci"):
            return True
    return False


if is_davinci_device():
    logger.info("detected npu device, use davinci npu")
    from npu_bridge.estimator import npu_ops
    logger.info("npu_bridge file is %s" % npu_ops.__file__)


def get_model_file_name(model_path):
    default_model = "model.pb"
    models = []

    for file in os.listdir(model_path):
        if file.endswith(".pb"):
            models.append(file)
    if len(models) > 1:
        return default_model
    elif len(models) == 1:
        return models[0]
    else:
        raise Exception("frozen graph pb model is not exist")


class FrozenGraphBaseService(SingleNodeService):
    def __init__(self, model_name, model_path):
        super(FrozenGraphBaseService, self).__init__(model_name, model_path)
        self.model_path = model_path
        self.model_inputs = {}
        self.model_outputs = {}
        self.config = self.get_npu_config()
        self.sess_init()

    def get_npu_config(self):
        config = tf.ConfigProto()
        custom_op = config.graph_options.rewrite_options.custom_optimizers.add()
        custom_op.name = "NpuOptimizer"

        custom_op.parameter_map["use_off_line"].b = True
        custom_op.parameter_map["precision_mode"].s = tf.compat.as_bytes("force_fp16")
        custom_op.parameter_map["graph_run_mode"].i = 0
        config.graph_options.rewrite_options.remapping = RewriterConfig.OFF

        return config

    def sess_init(self):
        model_file_name = get_model_file_name(self.model_path)

        with tf.gfile.FastGFile(os.path.join(self.model_path, model_file_name), 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
        tf.import_graph_def(
            graph_def,
            input_map=None,
            return_elements=None,
            name="",
            op_dict=None,
            producer_op_list=None
        )
        self.graph_keys = [tensor.name for tensor in graph_def.node]
        self.sess = tf.Session(config=self.config)

    def _preprocess(self, data):
        # http 两种请求形式
        # form-data 文件格式的请求对应 data = {"请求key值":{"文件名":<文件io>}}
        # json格式对应 data = json.loads("接口传入的json体")

        preprocessed_data = {}
        for k, v in data.items():
            images = []
            for file_name, file_content in v.items():
                image1 = Image.open(file_content)
                image1 = image1.convert("RGB")
                image1 = np.array(image1, dtype=np.float32)
                image1 = image1[:, :, :]
                images.append(image1.tolist())

            preprocessed_data[k] = images

        return preprocessed_data

    def _inference(self, data):
        feed_dict = {}

        for k, v in data.items():
            if k not in self.model_inputs:
                logger.error("input key %s is not in model inputs %s", k, list(self.model_inputs.keys()))
                raise Exception("input key %s is not in model inputs %s" % (k, self.graph_keys))
            feed_dict[self.model_inputs[k]] = v

        result = self.sess.run(self.model_outputs, feed_dict=feed_dict)

        return result

    def _postprocess(self, data):
        return data

    def __del__(self):
        self.sess.close()
