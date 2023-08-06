# Flask settings
import argparse

DEFAULT_FLASK_SERVER_NAME = '0.0.0.0'
DEFAULT_FLASK_SERVER_PORT = '5001'
DEFAULT_FLASK_DEBUG = True  # Do not use debug mode in production

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False

# tensorflow serving client settings
DEFAULT_TF_SERVER_NAME = '127.0.0.1'
DEFAULT_TF_SERVER_PORT = 8500


def parse_args():
    parser = argparse.ArgumentParser(description='Taichu Model Server')
    parser.add_argument('--grpc_port', action="store", default=8889, type=int)
    parser.add_argument('--http_port', action="store", default=8888, type=int)
    parser.add_argument('--worker', action="store", default=100, type=int)
    parser.add_argument('--model_path',
                        action="store",
                        default='./',
                        type=str)
    parser.add_argument('--service_file', action="store", default='customize_service.py', type=str)

    args = parser.parse_args()

    return args
