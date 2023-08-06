# -*- coding: utf-8 -*-
import logging
import threading

import numpy as np
import tensorflow as tf
from PIL import Image

from model_service.model_service import SingleNodeService


logger = logging.getLogger(__name__)


class TfServingBaseService(SingleNodeService):

    def __init__(self, model_name, model_path):
        self.model_name = model_name
        self.model_path = model_path
        self.model_inputs = {}
        self.model_outputs = {}

        # label文件可以在这里加载,在后处理函数里使用
        # label.txt放在obs和模型包的目录

        # with open(os.path.join(self.model_path, 'label.txt')) as f:
        #     self.label = json.load(f)

        # 非阻塞方式加载saved_model模型，防止阻塞超时
        thread = threading.Thread(target=self.get_tf_sess)
        thread.start()

    def get_tf_sess(self):
        # load saved_model 格式的模型

        # session要重用，不要用with语句
        sess = tf.Session(graph=tf.Graph())
        meta_graph_def = tf.saved_model.loader.load(sess, [tf.saved_model.tag_constants.SERVING], self.model_path)
        signature_defs = meta_graph_def.signature_def

        self.sess = sess

        signature = []

        # only one signature allowed
        for signature_def in signature_defs:
            signature.append(signature_def)
        if len(signature) == 1:
            model_signature = signature[0]
        else:
            logger.warning("signatures more than one, use serving_default signature")
            model_signature = tf.saved_model.signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY

        logger.info("model signature: %s", model_signature)

        for signature_name in meta_graph_def.signature_def[model_signature].inputs:
            tensorinfo = meta_graph_def.signature_def[model_signature].inputs[signature_name]
            name = tensorinfo.name
            op = self.sess.graph.get_tensor_by_name(name)
            self.model_inputs[signature_name] = op

        logger.info("model inputs: %s", self.model_inputs)

        for signature_name in meta_graph_def.signature_def[model_signature].outputs:
            tensorinfo = meta_graph_def.signature_def[model_signature].outputs[signature_name]
            name = tensorinfo.name
            op = self.sess.graph.get_tensor_by_name(name)

            self.model_outputs[signature_name] = op

        logger.info("model outputs: %s", self.model_outputs)

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
            if k not in self.model_inputs.keys():
                logger.error("input key %s is not in model inputs %s", k, list(self.model_inputs.keys()))
                raise Exception("input key %s is not in model inputs %s" % (k, list(self.model_inputs.keys())))
            feed_dict[self.model_inputs[k]] = v

        result = self.sess.run(self.model_outputs, feed_dict=feed_dict)
        logger.info('predict result : ' + str(result))

        return result

    def _postprocess(self, data):
        return data

    def __del__(self):
        self.sess.close()

    def ping(self):
        pass

    def signature(self):
        pass
