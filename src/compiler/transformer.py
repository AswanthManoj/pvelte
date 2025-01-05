import ast
from typing import Dict, Any

class JSTransformer:
    def transform_state(self, states: Dict[str, Any]) -> str:
        """Transform state declarations to JavaScript."""
        js_states = []
        for name, value in states.items():
            js_states.append(f"const {name} = createState({value});")
        return '\n'.join(js_states)
    
    def transform_function(self, func_name: str, func_node) -> str:
        """Transform Python function to JavaScript."""
        body = func_node.body[0]
        if isinstance(body, ast.AugAssign):
            target = body.target.id
            return f"""
function {func_name}() {{
    {target}.set({target}.get() + 1);
}}
"""
        return ""

    def transform_template(self, template: str, states: Dict[str, Any]) -> str:
        """Transform template with interpolation."""
        for state_name in states:
            template = template.replace(
                f"{{{state_name}}}", 
                "${" + f"{state_name}.get()" + "}"
            )
        return template