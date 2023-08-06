# -*- coding: utf-8 -*-
"""
DL webservice app
"""
import ctypes
import inspect
import json
import logging
import os
import threading
import time
import traceback
import uuid

from flask import Flask, request, g

from model_service.log import init_logger
from model_service.settings import parse_args
from model_service.ratelimiter import semaphore

init_logger()

app = Flask("aa")

from model_service.error_code import ModelNotFoundError, ModelPredictError

LOGGER = logging.getLogger(__name__)

from model_service.model_server import SingleNodeService
import multiprocessing

workers_pool = multiprocessing.Queue()
workers_status = []


def worker_main_loop(args, pipe, status):
    # pwd = os.path.dirname(os.path.abspath(__file__))

    # args = parse_args()

    LOGGER.info("args: %s", args)

    from model_service.model_server import load_service
    dict_model_service = {}

    model_path = os.path.abspath(args.model_path)
    # model_name = args.model_name

    model_service_file = args.service_file

    print(
        "model_path={} \n model_service_file={} "
        .format(model_path, model_service_file))

    module = load_service(os.path.join(model_path, model_service_file)
                          ) if model_service_file else SingleNodeService
    classes = [cls[1] for cls in inspect.getmembers(module, inspect.isclass)]

    # assert len(classes) >= 1, \
    #     'No valid python class derived from Base Model Service is in module file: %s' % \
    #     model_service_file

    class_defs = list(
        filter(
            lambda c: issubclass(c, SingleNodeService) and len(
                c.__subclasses__()) == 0, classes))

    # if len(class_defs) != 1:
    #     raise Exception(
    #         'There should be one user defined service derived from ModelService.'
    #     )

    for c in class_defs:
        LOGGER.info("class_defs: %s", c.__name__)
        instance = c(model_path)
        # threading.Thread(target=instance.warmup).start()
        instance.warmup()
        dict_model_service[f'{str(c.__name__).lower()}_{instance.model_version.lower()}'] = instance

    # model_service = class_defs[0](model_path)
    status.value = 0
    LOGGER.info("model service init done")

    while True:
        data = pipe.recv()
        try:
            model_name = data.get('model_name')
            model_version = data.get('model_version')
            ins = dict_model_service.get(f'{model_name.lower()}_{model_version.lower()}', None)
            if ins is None:
                ret = {
                    'data': None,
                    'status': 'error',
                    'error': 'model not found',
                }
            else:
                ret = {
                    'data': ins.inference(data.get('data'), data.get('context', {})),
                    'status': 'ok',
                }
        except Exception as e:
            LOGGER.error(traceback.format_exc())
            ret = {
                'data': None,
                'status': 'error',
                'error': str(e),
            }
        pipe.send(ret)

    # return dict_model_service


def model_inference(model_name, model_version, data, context={}):
    p = workers_pool.get(timeout=1)
    p.send({'model_name': model_name, 'model_version': model_version, 'data': data, 'context': context})
    ret = p.recv()
    workers_pool.put(p)
    if ret.get('status') == 'error':
        raise ModelPredictError(message=ret.get('error'))
    return ret.get('data')


args = parse_args()


def init_model_service_instance():
    for i in range(args.instances_num):
        p1, p2 = multiprocessing.Pipe()
        status = multiprocessing.Value('i', -1)
        workers_status.append(status)
        LOGGER.info("start worker %s", i)
        multiprocessing.Process(target=worker_main_loop, args=(args, p2, status)
                                ).start()
        workers_pool.put(p1)


# model_service = init_model_service_instance()


# def get_model_service(model_name, model_version):
#     model_name = model_name.lower()
#     model_version = model_version.lower()
#     ins = model_service.get(f'{model_name}_{model_version}', None)
#     if ins is None:
#         raise ModelNotFoundError(message=f'Model {model_name} version {model_version} not found')
#     return ins

def is_all_model_ready():
    for stat in workers_status:
        if stat.value != 0:
            return False

    return True


# def is_all_model_ready():
# if len(model_service) == 0:
#     return False
# for k, instance in model_service.items():
#     if not instance.ready:
#         return False

# return True


@app.before_request
def add_request_id():
    # 记录请求开始时间
    g.start = time.time()

    forwarded_for = request.headers.get('X-Forwarded-For')
    LOGGER.debug('X-Forwarded-For:{}'.format(forwarded_for))
    g.remote_addr = request.remote_addr
    if forwarded_for:
        g.remote_addr = forwarded_for.split(',')[0].strip()

    try:
        if 'x_request_id' in request.headers:
            request_id = request.headers.get('x_request_id')
        else:
            request_id = str(uuid.uuid4())
        setattr(g, 'request_id', request_id)
    except Exception as e:
        logging.error(str(e))


@app.before_request
def limiter():
    if request.path == '/health/live' or request.path == '/health/ready':
        return

    ok = semaphore.acquire(blocking=True, timeout=1)
    g.is_limited = not ok
    if not ok:
        return {'error': '请求过于频繁，请稍后再试'}, 429, {'Content-Type': 'application/json'}


@app.after_request
def after_request(response):
    if hasattr(g, 'is_limited') and not g.is_limited:
        semaphore.release()

    try:
        extra = {
            # 'id': str(uuid.uuid4()),
            'http_method': request.method,
            'endpoint': request.endpoint,
            'url_path': request.path,
            'url_query': request.query_string.decode('utf-8'),
            'host': request.host,
            'user_agent': '',
            'remote_addr': g.remote_addr,
            'content_type': request.content_type,
            'cost_time': round(time.time() - g.start, 3),
        }
        if 'user_agent' in request.headers:
            extra['user_agent'] = request.headers.get('user_agent')

        LOGGER.info('请求日志埋点', extra=extra)
    except Exception as e:
        LOGGER.error('{}\n{}'.format(repr(e), traceback.format_exc()))

    return response


@app.errorhandler(Exception)
def handle_exception(e):
    LOGGER.error('handle_exception: {}\n{}'.format(repr(e), traceback.format_exc()))
    if isinstance(e, ModelNotFoundError) or isinstance(e, ModelPredictError):
        return {'error': e.message}, 400, {'Content-Type': 'application/json'}

    return {'error': '系统内部错误，请联系维护人员'}, 400, {'Content-Type': 'application/json'}


@app.route('/health/live', methods=['GET'])
def live():
    ret = {'live': True}
    return json.dumps(ret, ensure_ascii=False), 200, {'Content-Type': 'application/json'}


@app.route('/health/ready', methods=['GET'])
def ready():
    is_ready = is_all_model_ready()
    ret = {'ready': is_ready}
    return json.dumps(ret, ensure_ascii=False), 200 if is_ready else 400, {'Content-Type': 'application/json'}


@app.route('/v2/models/<model_name>/versions/<model_version>/infer', methods=['POST'])
def predict(model_name, model_version):
    req = request.get_json()
    ctx = {}
    request_id = g.request_id

    ret = {
        'id': request_id,
        'model_name': model_name,
        'model_version': model_version,
        'parameters': {}
    }

    # instance = get_model_service(model_name, model_version)

    try:
        res = model_inference(model_name, model_version, req.get('parameters', {}), ctx)
    except Exception as e:
        LOGGER.error('Algorithm crashed!')
        LOGGER.error(traceback.format_exc())
        raise ModelPredictError(message=str(e))

    ret['parameters'] = res
    return json.dumps(ret, ensure_ascii=False), 200, {
        'Content-Type': 'application/json'
    }


# @app.route('/', methods=['POST'])
# def inference_task():
#     # get all data from different media
#     rec_dict = {}
#
#     def parse_file(f):
#         if isinstance(f.stream, tempfile.SpooledTemporaryFile):
#             return f.filename, io.BytesIO(f.stream.read())
#         elif isinstance(one.stream, io.BytesIO):
#             return f.filename, f.stream
#         else:
#             LOGGER.error('receive file not recognized!')
#             raise Exception
#
#     if request.form or request.files:
#         form = request.form
#         files = request.files
#         rec_dict = {}
#         for k, v in form.items():
#             rec_dict[k] = v
#
#         for k, file in files.items():
#             lst = files.getlist(k)
#             if len(lst) == 1:
#                 one = lst[0]
#                 filename, file_content = parse_file(one)
#                 rec_dict[k] = (filename, file_content)
#
#                 continue
#
#             filename_dict = collections.OrderedDict()
#             for one in lst:
#                 filename, file_content = parse_file(one)
#                 filename_dict[filename] = file_content
#
#             rec_dict[k] = filename_dict
#     elif request.json:
#
#         rec_dict = request.json
#     else:
#         return get_result_json(MR0101()), 400, {
#             'Content-Type': 'application/json'
#         }
#
#     args = request.args
#     for k, v in args.items():
#         rec_dict[k] = v
#
#     try:
#         res = model_service.inference(rec_dict)
#         return json.dumps(res, ensure_ascii=False), 200, {
#             'Content-Type': 'application/json'
#         }
#     except KeyError as k:
#         LOGGER.error('Algorithm crashed!')
#         LOGGER.error(traceback.format_exc())
#         return get_result_json(MR0105()), 400, {
#             'Content-Type': 'application/json'
#         }
#     except TypeError as te:
#         LOGGER.error('Algorithm crashed!')
#         LOGGER.error(traceback.format_exc())
#         return get_result_json(MR0105()), 400, {
#             'Content-Type': 'application/json'
#         }
#     except Exception as e:
#         LOGGER.error('Algorithm crashed!')
#         LOGGER.error(traceback.format_exc())
#         return get_result_json(MR0105()), 500, {
#             'Content-Type': 'application/json'
#         }


def get_result_json(ais_error):
    """
        Create a json response with error code and error message
    """
    data = ais_error.to_dict()
    data['words_result'] = {}

    return json.dumps(data, ensure_ascii=False)

# if __name__ == "__main__":
#     args = parser.parse_args()
# else:
#     args = parser.parse_args(os.environ['TF_MODEL_ARGS'].split())
