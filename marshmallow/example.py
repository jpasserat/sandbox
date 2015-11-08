# from https://marshmallow.readthedocs.org/en/latest/
import copy 
import json
from datetime import date

from marshmallow import (
    Schema, fields,
    ValidationError,
    pprint,)


class ArtistSchema(Schema):
    name = fields.Str(
        required=True,
        error_messages={'required': 'Field name is mandatory.'})
    age = fields.Int()

class AlbumSchema(Schema):
    title = fields.Str()
    release_date = fields.Date()
    artist = fields.Nested(ArtistSchema)


artist_schema = ArtistSchema(strict=True)
album_schema = AlbumSchema(strict=True)

def execute(func, *args, **kwargs):
    try: 
        data, errors = func(*args, **kwargs)
        print "OK", type(data), data
    except ValidationError as e:
        print "ERROR", type(e), e


# Serialize

# Create objects
artist_obj = dict(name='David Bowie')
album_obj = dict(artist=artist_obj, title='Hunky Dory', release_date=date(1971, 12, 17))

# Dump
execute(artist_schema.dump, artist_obj)

execute(album_schema.dump, album_obj)

# Deserialize

# Create data
artist_data = dict(age='123', name='David Bowie', surname='Ziggy Stardust')
album_data = dict(artist=artist_data, title='Let''s Dance', release_date="1983-01-01")

# Load
execute(artist_schema.load, artist_data)
execute(artist_schema.loads, json.dumps(artist_data))

artist_data_m = dict(age='34')
execute(artist_schema.load, artist_data_m)
execute(artist_schema.load, artist_data_m, partial=True)

execute(album_schema.load, album_data)

album_data2 = copy.deepcopy(album_data)
album_data2['release_date'] = "19830101"
execute(album_schema.load, album_data2)
