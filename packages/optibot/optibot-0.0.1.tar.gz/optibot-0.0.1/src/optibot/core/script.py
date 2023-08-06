from __future__ import annotations
from functools import cached_property

class Script():
    
    def __init__(self, source):
        self.refs : dict[str, SplinterRef] = dict()
        self.source : str = source
        self.splinters_params = 0

    
    
    @cached_property
    def splinter_blocks(self):
        return len(self.refs.keys())
    
    def imports_handler(self):
        return ""
    
    def splinter_handler(self, ref_name, splinter_tasks, **kwargs):
        
        if ref_name in self.refs:
            raise SyntaxError(f"Script alread has a ref with name {ref_name}")
        
        self.refs[ref_name] = SplinterRef(ref_name, splinter_tasks, dict(**kwargs))


class SplinterRef():
    
    def __init__(self, name, tasks, vars):
        self.name = name
        self.tasks = tasks
        self.vars = vars
        self.splinters = set()
        self.max_param_size = 0

