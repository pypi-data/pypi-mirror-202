# Author: ASU --<andrei.suiu@gmail.com>
import json
from typing import Any, Callable, Dict, Type


class JSONCompositeEncoder(json.JSONEncoder):
    """
    The main purpose of this class is that Pydantic's json_encoders functionality doesn't work with the classes that
    derive from the types that stdlib json encoder does already support (str, int, etc...),
    so we have to override json() method of the BaseModel and use this encoder instead of the default encoders.

    This encoder can receive Config.json_encoders dict, and it will use it to encode the types that are not supported by the default encoder.
    """

    class Builder:
        def __init__(self, encoders: Dict[Type, Callable]):
            self._encoders = encoders

        def __call__(self, *args, **kwargs) -> 'JSONCompositeEncoder':
            return JSONCompositeEncoder(self._encoders, *args, **kwargs)

    def __init__(self, encoders: Dict[Type, Callable], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._encoders = encoders

    def _change_to_encodable_type(self, o: Any):
        if isinstance(o, dict):
            new_o = o.copy()
            for k in new_o:
                new_o[k] = self._change_to_encodable_type(new_o[k])
            return new_o
        elif isinstance(o, list):
            return [self._change_to_encodable_type(x) for x in o]
        for type_, encoder in self._encoders.items():
            if isinstance(o, type_):
                return encoder(o)
        return o

    def encode(self, o):
        new_o = self._change_to_encodable_type(o)
        return super().encode(new_o)
