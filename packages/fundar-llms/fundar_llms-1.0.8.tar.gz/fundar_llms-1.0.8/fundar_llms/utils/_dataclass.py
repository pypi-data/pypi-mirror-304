from abc import ABC as AbstractBaseClass
from dataclasses import asdict
from typing import Any
from collections.abc import Iterable

class DataclassDictUtilsMixin(AbstractBaseClass):
    @classmethod
    def from_dict(cls, data: dict[str, Any]):
        return cls(**data)
    
    def to_dict(self, exclude=None, compact=False) -> dict[str, Any]:
        data = asdict(self) # type: ignore
        
        if exclude and isinstance(exclude, Iterable):
            assert all(isinstance(x, str) for x in exclude)
            data = {k:v for k,v in data.items() if not k in exclude}
            if 'extra' in data:
                data['extra'] = {
                    k:v 
                    for k,v in data['extra'].items()
                    if not k in [
                        x.split('extra.')[1] for x in exclude
                        if x.startswith('extra.')
                    ]
                }

        if compact :
            data = {k:v for k,v in data.items() if v}
        
        return data