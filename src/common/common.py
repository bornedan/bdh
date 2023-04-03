import yaml
import os
config = None

def list_replace_value(l: list, old: str, new: str) -> list:
    x = []
    for e in l:
        if isinstance(e, list):
            e = list_replace_value(e, old, new)
        elif isinstance(e, dict):
            e = dict_replace_value(e, old, new)
        elif isinstance(e, str):
            e = e.replace(old, new)
        x.append(e)
    return x
def dict_replace_value(d: dict, old: str, new: str) -> dict:
    x = {}
    for k, v in d.items():
        if isinstance(v, dict):
            v = dict_replace_value(v, old, new)
        elif isinstance(v, list):
            v = list_replace_value(v, old, new)
        elif isinstance(v, str):
            v = v.replace(old, new)
        x[k] = v
    return x


def get_config():
    global config
    if config == None:
        with open("./../../config.yaml") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        path = os.path.dirname(os.path.dirname(os.getcwd())) + "\\"
        config = dict_replace_value(config, "@path@", path)

def get_api_headers():
    get_config()
    api_key_file = open(config['token-url'],"r")
    api_key = api_key_file.read()
    api_key_file.close()
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'x-access-token': api_key
    }
    return headers


if __name__ == '__main__':
    print(get_api_headers())