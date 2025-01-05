import re
import ast
from typing import Dict, Any

class PySvelteCompiler:
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
    
    def extract_states(self, python_code: str) -> Dict[str, Any]:
        """Extract state variables from Python code."""
        # Preprocess the code first
        processed_code = self.preprocess_script(python_code)
        tree = ast.parse(processed_code)
        state_vars = {}
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(node.value, ast.Call):
                        if getattr(node.value.func, 'id', '') == 'create_state':
                            state_vars[target.id] = ast.literal_eval(node.value.args[0])
        
        return state_vars

    def extract_functions(self, python_code: str) -> Dict[str, ast.FunctionDef]:
        """Extract function definitions from Python code."""
        processed_code = self.preprocess_script(python_code)
        tree = ast.parse(processed_code)
        functions = {}
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions[node.name] = node
        
        return functions