from wtforms import Form
from flask import request
from app.api.error.exceptions import ParameterException


class BaseForm(Form):
    def __init__(self, **kwargs):
        self.jsonData = request.json
        if request.json:
            self.jsonKeys = request.json.keys()
        super().__init__(data=self.jsonData, **kwargs)

    def validateForApi(self):
        validate = super(BaseForm, self).validate()
        if not validate:
            raise ParameterException(information=self.errors)
        return self
