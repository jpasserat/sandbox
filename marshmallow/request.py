# from https://marshmallow.readthedocs.org/en/latest/
import copy 
import json
from datetime import date

from marshmallow import (
    Schema, SchemaOpts,
    validates_schema, fields,
    ValidationError,
    post_load,)


class RequestOps(SchemaOpts):
    def __init__(self, meta):
        SchemaOpts.__init__(self, meta)
        self.strict = True


class RequestSchema(Schema):
    OPTIONS_CLASS = RequestOps

    len_data = fields.Constant(3)
    columns = fields.List(fields.String)
    data = fields.List(
        fields.List(fields.String),
        error_messages={'required': 'Field is mandatory.'})
    req_dict = fields.Method("build_dict", deserialize="build_dict", dump_only=False)
    
    @post_load
    def make_object(self, data):
        print "POST_LOAD", data
        data['as_dict'] = dict(zip(data.get('columns'), data.get('data')[0]))
        return data

    @validates_schema
    def validate_request(self, data):
        if self._unmarshal.errors:
            return
        req_columns = data['columns']
        req_data = data['data']
        if any(len(req_columns) != len(d) for d in req_data):
            raise ValidationError('columns and data must be of same size')

    def build_dict(self, obj):
        print "build_dict", obj
        #return zip(obj.get('columns'), obj.get('data'))


request_schema = RequestSchema()

# Create data
requests = [
    dict(columns=['name', 'age'], data=['David Bowie', 3]),
    dict(columns=['name', 'age'], data=[['David Bowie'],]),
    dict(columns=['name', 'age'], data=[['David Bowie', '3'],]),
]

for request in requests:
    try:
        print request
        print request_schema.load(request).data
    except ValidationError as e:
        print "ERROR", e

