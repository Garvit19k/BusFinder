import dotsi
from rest_framework.response import Response

# d = dotsi.Dict({"foo": {"bar": "baz"}})
# d.foo.bar
# install dotsi and rest frame work

def ResponseBack(status='', message='', data={}, local=False):
    if local == True:
        obj = {
            'status': status,
            'message': message,
            'data': data,
        }
        model = dotsi.Dict(obj)
        return model
    if local == False:
        obj = {
            'status': status,
            'message': message,
            'data': data,
        }
        return Response(obj)