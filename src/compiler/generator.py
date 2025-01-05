
class JSGenerator:
    COMPONENT_TEMPLATE = """
// Generated by Pvelte
const %s = () => {
    %s
    %s
    
    return {
        mount: (target) => {
            const template = `%s`;
            target.innerHTML = template;
            const button = target.querySelector('button');
            button.addEventListener('click', %s);
            
            // Setup state subscriptions
            %s.subscribe(value => {
                target.querySelector('h2').textContent = `The count is ${value}`;
            });
        }
    };
};
"""

    def generate_component(self, name: str, states: str, functions: str, 
                         template: str, main_function: str, main_state: str) -> str:
        return self.COMPONENT_TEMPLATE % (
            name, states, functions, template, main_function, main_state
        )