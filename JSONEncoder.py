import datetime
import json
from bson import ObjectId


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, str):
            return str(obj)
        return json.JSONEncoder.default(self, obj)