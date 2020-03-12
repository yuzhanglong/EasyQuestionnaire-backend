from flask import Blueprint
from werkzeug.exceptions import HTTPException

from app.api.error.errorHandler import JobException
from flask import current_app

commonException = Blueprint('common', __name__)


@commonException.app_errorhandler(Exception)
def handleCommonException(error):
    if isinstance(error, JobException):
        return error
    if isinstance(error, HTTPException):
        code = error.code
        information = error.description
        return JobException(code=code, information=information)
    else:
        raise error
