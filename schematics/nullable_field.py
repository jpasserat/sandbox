from schematics.models import Model
from schematics.types import (
    StringType,
    FloatType)
from schematics.exceptions import (
    BaseError,
    DataError)


class MyModel(Model):
    field1 = StringType(required=True)
    field2 = StringType(required=True)


class Ticket(Model):
    name = StringType()
    departure = StringType()
    arrival = StringType()
    price = FloatType()
    member_ref = StringType(required=True)


if __name__ == "__main__":
    for fk, fv in MyModel.fields.items():
        print fk, fv.default

    model = MyModel({'field1': 'foo', 'field2': 'bar'})
    print model.items()
    model.validate()
    print model.to_native()

    model = MyModel({'field1': 'foo'})
    print model.items()
    try:
        model.validate()
    except DataError as e:
         print e

    model = MyModel({'field1': 'foo', 'field2': None})
    print model.items()
    model.validate()
