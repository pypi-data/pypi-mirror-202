from functools import cached_property

class Splinter:
    
    def __init__(self):
        self.id = None
        self.vars = dict()
        self.params = dict()
        self.imports = set()
        self.tasks = set()
        self.source = None
        self.description = ""

        self._param_size = None
        self._signature = None
    
    @cached_property
    def signature(self):
        return set(self.vars.keys())
    
    @cached_property
    def param_size(self):
        return len(self.params)

    def optiid_handler(self, splinter_id):
        if self.id is not None:
            raise ValueError(f"Splinter {self.id} already has id defined.")

        self.id = splinter_id
    
    def optidesc_handler(self, desciption):
        self.description = desciption
    
    def optitask_handler(self, task: str):
        self.tasks.add(task)

    def optiimport_handler(self, import_str: str):
        self.imports.add(import_str)

    def optivar_handler(self, var_name: str, required : bool =False):
        if var_name in self.vars:
            raise ValueError(f"Splinter '{self.id}' already has var '{var_name}' defined ")

        self.vars[var_name] = (var_name, required)

    def optiparam_handler(self, param_name: str, param_type: str, param_values: list = None, **kwargs):
        if param_name in self.params:
            raise ValueError(f"Splinter '{self.id}' already has param '{param_name}' defined ")

        self.params[param_name] = (param_name, param_type, param_values, kwargs)
    
    
    

