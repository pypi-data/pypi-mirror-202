from typing import Optional
from jinja2 import Environment, BaseLoader
from .script import Script
from .splinter import Splinter
from random import randint


IMPORT_PLACEHOLDER = "##__IMPORTS__##"

class Renderer():

    def __init__(self, script : Script, script_sequence: list[int], splinters: dict[str, Splinter]):
        self.script = script
        self.script_sequence = script_sequence
        self.splinters = splinters
        self.block_at = -1
        self.param_at = -1
        self.env : Optional[Environment] = None
        self.imports_needed = set()


    def render(self):
        self.env = Environment(loader=BaseLoader)

        self.env.globals['splinter'] = self.splinter_handler
        self.env.globals['imports'] = self.imports_handler
        
        rendered_source = self.env.from_string(self.script.source).render()

        rendered_source = rendered_source.replace(IMPORT_PLACEHOLDER, "\n".join(self.imports_needed))

        return rendered_source


    def imports_handler(self):
        return IMPORT_PLACEHOLDER

    def splinter_handler(self, ref_name, splinter_tasks, **kwargs):
        ref = self.script.refs.get(ref_name)

        self.block_at += 1
        splinter_gene = self.script_sequence[self.block_at]
        splinter_gene = int(splinter_gene % len(ref.splinters))

        splinter_to_render = list(ref.splinters)[splinter_gene]

        splinter = self.splinters.get(splinter_to_render)

        render_params = dict()
        for var_name in splinter.vars.keys():
            render_params[var_name] = ref.vars[var_name]

        for param_name in splinter.params.keys():
            self.param_at += 1
            param_gene = self.script_sequence[self.script.splinter_blocks + self.param_at]

            render_params[param_name] = self.gene_to_value(param_gene, param_name, splinter)

        rendererd_splinter = self.env.from_string(splinter.source) \
            .render(**render_params)
        
        self.imports_needed = self.imports_needed.union(splinter.imports)

        return rendererd_splinter
    
    def gene_to_value(self, value, param_name, splinter):
        param_type = splinter.params[param_name][1]
        if param_type == "int":
            return self._gene_to_value_int(value, param_name, splinter)
        if param_type == "float":
            return self._gene_to_value_float(value, param_name, splinter)
        if param_type == "str":
            return self._gene_to_value_str(value, param_name, splinter)
        
        return value
    
    def _gene_to_value_int(self, value, param_name, splinter):
        from .optibot import MAX_SIZE

        opts = splinter.params[param_name][-1]

        lowest_possible = -MAX_SIZE
        highest_possible = MAX_SIZE
        max_range = highest_possible - lowest_possible
        original_delta = (value - lowest_possible) / max_range

        if "min" in opts:
            lowest_possible = max(lowest_possible, opts["min"])

        if "max" in opts:
            highest_possible = min(highest_possible, opts["max"])

        scaled_range = highest_possible - lowest_possible
        
        scaled_value = lowest_possible + (scaled_range * original_delta)

        return int(scaled_value)

    def _gene_to_value_float(self, value, param_name, splinter):
        from .optibot import MAX_SIZE

        opts = splinter.params[param_name][-1]

        lowest_possible = -MAX_SIZE
        highest_possible = MAX_SIZE
        max_range = highest_possible - lowest_possible
        original_delta = (value - lowest_possible) / max_range

        if "ratio" in opts and opts["ratio"]:
            return original_delta


        if "min" in opts:
            lowest_possible = max(lowest_possible, opts["min"])

        if "max" in opts:
            highest_possible = min(highest_possible, opts["max"])

        scaled_range = highest_possible - lowest_possible
        
        scaled_value = lowest_possible + (scaled_range * original_delta)

        return scaled_value

    def _gene_to_value_str(self, value, param_name, splinter):
        from .optibot import MAX_SIZE

        opts = splinter.params[param_name][-1]
        
        value = value % len(opts["choices"])

        return f'\"{opts["choices"][value]}\"'
