from src.compiler.parser import PvelteCompiler
from src.compiler.transformer import JSTransformer
from src.compiler.generator import JSGenerator
import os

def compile_component(source_path: str, output_dir: str):
    """Compile a .pysvelte file to JavaScript."""
    # Read source file
    with open(source_path, 'r') as f:
        source = f.read()
    
    # Parse component
    compiler = PvelteCompiler()
    parsed = compiler.parse_component(source)
    
    # Extract states and functions using the new combined method
    states, functions = compiler.extract_states_and_functions(parsed['script'])
    
    # Transform to JavaScript
    transformer = JSTransformer()
    js_states = transformer.transform_state(states)
    
    # Transform all functions
    js_functions = []
    for func_name, func_node in functions.items():
        js_functions.append(transformer.transform_function(func_name, func_node))
    js_functions = '\n'.join(js_functions)
    
    # Transform template with all states and functions
    js_template = transformer.transform_template(parsed['template'], states, functions)
    
    # Generate final JavaScript
    generator = JSGenerator()
    output = generator.generate_component(
        'Counter', 
        js_states, 
        js_functions, 
        js_template,
        list(states.keys()),  # Pass state names
        functions  # Pass function dictionary
    )
    
    # Write output
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'counter.js')
    with open(output_path, 'w') as f:
        f.write(output)