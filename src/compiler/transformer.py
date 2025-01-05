# src/compiler/transformer.py
import ast
from typing import Dict, Any

class JSTransformer:
    def transform_state(self, states: Dict[str, Any]) -> str:
        """Transform state declarations to JavaScript."""
        js_states = []
        for name, value in states.items():
            js_states.append(f"const {name} = createState({value});")
        return '\n'.join(js_states)
    
    def transform_function(self, func_name: str, func_node: ast.FunctionDef) -> str:
        """Transform Python function to JavaScript."""
        js_body = []
        
        for node in func_node.body:
            if isinstance(node, ast.AugAssign):
                target = node.target.id
                op = self._get_js_operator(node.op)
                js_body.append(f"{target}.set({target}.get() {op} 1);")
        
        return f"""
function {func_name}() {{
    {'; '.join(js_body)}
}}
"""

    def _get_js_operator(self, op: ast.operator) -> str:
        """Convert Python operator to JavaScript operator."""
        op_map = {
            ast.Add: '+',
            ast.Sub: '-',
            ast.Mult: '*',
            ast.Div: '/',
        }
        return op_map.get(type(op), '+')

    def transform_template(self, template: str, states: Dict[str, Any], functions: Dict[str, Any]) -> str:
        """Transform template with interpolation and event handlers."""
        # Replace state interpolation
        for state_name in states:
            template = template.replace(
                f"{{{state_name}}}", 
                f'<span data-bind="{state_name}">${{{state_name}.get()}}</span>'
            )
        
        # Replace event handlers
        for func_name in functions:
            template = template.replace(
                f'onclick={{{func_name}}}',
                f'data-onclick="{func_name}"'
            )
        
        return template