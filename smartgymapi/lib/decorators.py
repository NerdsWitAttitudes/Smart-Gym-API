from marshmallow import ValidationError
from pyramid.httpexceptions import HTTPBadRequest


def singleton(class_):
    """Decorator to turn class into singleton"""
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


def handler_wrapper(validation_schema):
    """
    from python docs: https://wiki.python.org/moin/FunctionWrappers

    FunctionWrapper is a design pattern used when dealing with relatively
    complicated functions. The wrapper function typically performs some
    prologue and epilogue tasks
    """
    def decorate(func):
        def call(self):
            # validation
            try:
                if self.request.method == "GET":
                    result, errors = validation_schema(strict=True).load(
                        self.request.GET)
                else:
                    result, errors = validation_schema(strict=True).load(
                        self.request.json_body)
            except ValidationError as e:
                raise HTTPBadRequest(json={'message': str(e)})
            return func(self, result)
        return call
    return decorate
