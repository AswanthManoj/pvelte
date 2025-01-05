# pvelte

## Pvelte = Svelte.replace("javascript", "python")

Pvelte is an experimental web application framework that combines Python with Svelte-like reactivity. It allows you to write Svelte-style components using Python instead of JavaScript, which then get compiled to JavaScript.

# Key Features

- Write components in Python with Svelte-like syntax
- Reactive state management using $state runes (inspired by Svelte 5)
- Automatic compilation to JavaScript
- Simple component lifecycle and DOM updates

# Installation

- Clone the repo `git clone https://github.com/yourusername/pvelte.git` 
- `cd pvelte`
- Install astral UV `pip install uv`
- Install dependencies `uv sync`

# Basic Usage

Create a `.pvelte` component file (eg., `counte.pvelte`):

```pvelte
<script lang="py">
count = $state(0)

def increment():
    count += 1

def decrement():
    count -= 1
</script>

<button onclick={increment}>Increment</button>
<h2>The count is {count}</h2>
<button onclick={decrement}>Decrement</button>
```

Create an HTML file to use your component:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Pvelte App</title>
</head>
<body>
    <div id="app"></div>

    <script src="../src/runtime/runtime.js"></script>
    <script src="counter/output/counter.js"></script>
    
    <script>
        const app = Counter();
        app.mount(document.getElementById('app'));
    </script>
</body>
</html>
```

Compile your component:
```python
from src import compile_component

compile_component('path/to/counter.pvelte', 'output/directory')
```


# How It Works
Pvelte works by:
1. Parsing .pvelte files to separate Python code and HTML template
2. Converting Python state declarations and functions to JavaScript
3. Transforming the template with reactive bindings
4. Generating a JavaScript component with reactive updates


# Current Status
This is an experimental framework in early development. Currently supports:

- Basic state management
- Simple event handling
- Component compilation
- DOM updates


# Limitations

- Only supports basic state operations
- Limited Python-to-JavaScript transformations
- No component composition yet
- Basic templating features only


# Acknowledgments

- Inspired by Svelte and particularly Svelte 5's runes