from schematics.models import Model
from schematics.types import StringType
from schematics.types.compound import ListType, DictType
from schematics.exceptions import BaseError, ValidationError
from schematics.transforms import EMPTY_LIST


class StrictListType(ListType):
    def _force_list(self, value):
        if value is None or value == EMPTY_LIST:
            return []

        try:
            if isinstance(value, basestring):
                raise TypeError()

            if isinstance(value, dict):
                return [value[unicode(k)] for k in sorted(map(int, value.keys()))]

            return list(value)
        except TypeError:
            raise ValidationError("Not a valid list %s" % (value))


class StrictStringType(StringType):
    allow_casts = (str)


class Request(Model):
    columns = StrictListType(StrictStringType(), required=True)
    data = StrictListType(StrictListType(StrictStringType()), required=True)

    def validate_output(self):
        req_columns = self.columns
        req_data = self.data
        if any(len(req_columns) != len(d) for d in req_data):
            raise ValidationError('columns and data must be of same size')


# Create data
requests = [
    dict(columns=['name', 0], data=['David Bowie', 3]),
    dict(columns=['name', 'age'], data=[['David Bowie'],]),
    dict(columns=['name', 'age'], data=[['David Bowie', 3],]),
    dict(columns=['name', 'age'], data='David Bowie'),
    dict(columns=[['name'], 'age'], data='David Bowie'),
    dict(columns=["name"], data=[[]], boo=1),
    "David",
    dict(columns=['name', 'age'], data=[['David Bowie', '3'],]),
]

for request in requests:
    try:
        print "INPUT", request
        request_obj = Request(request, strict=False)
        request_obj.validate_output()
        print request_obj.keys()
        for k, v in request_obj.items():
            print k, v
        for d in request_obj.data:
            print dict(zip(request_obj.columns, d))
    except BaseError as e:
        print "ERROR", e

