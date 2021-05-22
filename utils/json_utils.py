from datetime import date, datetime
import json


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (date, datetime)):
            return o.isoformat()
        return super(CustomJSONEncoder, self).default(o)


def dumps(o, **kwargs):
    kwargs.setdefault('cls', CustomJSONEncoder)
    return json.dumps(o, **kwargs)


def loads(s, **kwargs):  # pragma: no cover
    return json.loads(s, **kwargs)


def jsonify(o):
    if hasattr(o, 'to_dict'):
        o = o.to_dict()
    s = dumps(o)
    s = s.replace('""', 'null')
    return loads(s)
