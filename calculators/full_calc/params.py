import yaml

class Params:
    """Wrapper to unpack the params.yml file and allow for easy access to its
    parameters via dot notation"""
    def __init__(self, params_dict=None):

        if params_dict is None:
            with open('calculators/full_calc/params.yml', 'r', encoding="utf-8") as stream:
                params_dict = yaml.safe_load(stream)

        self.dictionary = params_dict

        for key, value in params_dict.items():
            if isinstance(value, dict):
                value = Params(value)
            self.__dict__[key] = value


    def __getattr__(self, item):
        return self.__dict__.get(item, None)
