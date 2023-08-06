# Flask settings
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
