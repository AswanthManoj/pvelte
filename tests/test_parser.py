import unittest
from src.compiler.parser import PySvelteCompiler

class TestPySvelteCompiler(unittest.TestCase):
    def setUp(self):
        self.compiler = PySvelteCompiler()
        self.test_source = """
<script lang="py">
count = $state(0)
def increment():
    count += 1
</script>

<button onclick={increment}>The count is {count}</button>
"""

    def test_parse_component(self):
        result = self.compiler.parse_component(self.test_source)
        self.assertIn('script', result)
        self.assertIn('template', result)
        self.assertIn('count = $state(0)', result['script'])
        self.assertIn('button', result['template'])

    def test_extract_states(self):
        result = self.compiler.parse_component(self.test_source)
        states = self.compiler.extract_states(result['script'])
        self.assertEqual(states['count'], 0)

if __name__ == '__main__':
    unittest.main()