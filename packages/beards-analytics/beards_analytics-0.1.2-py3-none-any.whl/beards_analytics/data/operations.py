from slugify import slugify
import typing as t


_T = t.TypeVar('_T')

def slugify_object_keys(obj, separator='-', lowercase=False):
    def inner_func(data):        
        if isinstance(data, dict):
            new_data = {}
            for key, value in data.items():
                new_key = slugify(key, separator=separator, lowercase=lowercase)
                new_value = inner_func(value)
                new_data[new_key] = new_value
            return new_data
        elif isinstance(data, list):
            return [inner_func(item) for item in data]
        else:
            return data

    return inner_func(obj)

def chunk_list(lst: t.List[_T], chunk_size: int):
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]
