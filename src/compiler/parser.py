# src/compiler/parser.py
import re
import ast
from typing import Dict, Any, List, Tuple

class PvelteCompiler:
    def parse_component(self, source: str) -> Dict[str, str]:
        """Parse a .pvelte component file into script and template parts."""
        script_match = re.search(r'<script.*?>(.*?)</script>', source, re.DOTALL)
        template_match = re.search(r'</script>(.*?)$', source, re.DOTALL)
        
        if not script_match or not template_match:
            raise ValueError("Invalid component format")
        
        return {
            'script': script_match.group(1).strip(),
            'template': template_match.group(1).strip()
        }
    
    def preprocess_script(self, script: str) -> str:
        """Convert $state syntax to valid Python."""
        return script.replace('$state', 'create_state')
    
    def extract_states_and_functions(self, python_code: str) -> Tuple[Dict[str, Any], Dict[str, ast.FunctionDef]]:
        """Extract both state variables and functions from Python code."""
        processed_code = self.preprocess_script(python_code)
        tree = ast.parse(processed_code)
        
        state_vars = {}
        functions = {}
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(node.value, ast.Call):
                        if getattr(node.value.func, 'id', '') == 'create_state':
                            try:
                                value = ast.literal_eval(node.value.args[0])
                                state_vars[target.id] = value
                            except (ValueError, SyntaxError):
                                # Handle non-literal state initializations
                                state_vars[target.id] = 'null'
            
            elif isinstance(node, ast.FunctionDef):
                functions[node.name] = node
        
        return state_vars, functions