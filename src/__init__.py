from src.compiler.parser import PySvelteCompiler
from src.compiler.transformer import JSTransformer
from src.compiler.generator import JSGenerator
import os

def compile_component(source_path: str, output_dir: str):
    """Compile a .pysvelte file to JavaScript."""
    # Read source file
    with open(source_path, 'r') as f:
        source = f.read()
    
    # Parse component
    compiler = PySvelteCompiler()
    parsed = compiler.parse_component(source)
    
    # Extract states and functions
    states = compiler.extract_states(parsed['script'])
    functions = compiler.extract_functions(parsed['script'])
    
    # Transform to JavaScript
    transformer = JSTransformer()
    js_states = transformer.transform_state(states)
    js_functions = transformer.transform_function('increment', functions['increment'])
    js_template = transformer.transform_template(parsed['template'], states)
    
    # Generate final JavaScript
    generator = JSGenerator()
    output = generator.generate_component(
        'Counter', js_states, js_functions, js_template, 'increment', 'count'
    )
    
    # Write output
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'counter.js')
    with open(output_path, 'w') as f:
        f.write(output)