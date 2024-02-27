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
        return self.__dict__[item]

    def describe(self):
        """Returns a description of the parameters"""
        return yaml.dump(self.dictionary, default_flow_style=False)

    def get_param_keys(self, nested_dict=None, parent_key='', key_separator='_'):
        keys = []
        if nested_dict == None:
            nested_dict = self.dictionary
        for key, value in nested_dict.items():
            new_key = parent_key + key_separator + key if parent_key else key
            if isinstance(value, dict):
                # Recursively call the function if the value is another dictionary
                keys.extend(self.get_param_keys(value, new_key, key_separator))
            else:
                # Append the key to the list if it's the lowest level
                keys.append(new_key)
        return keys

    def get_param_values(self, nested_dict=None):
        values = []
        if nested_dict == None:
            nested_dict = self.dictionary
        for value in nested_dict.values():
            if isinstance(value, dict):
                # Recursively call the function if the value is another dictionary
                values.extend(self.get_param_values(value))
            else:
                # Append the value to the list if it's the lowest level
                values.append(value)
        return values
