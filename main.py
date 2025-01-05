from src import compile_component

def main():
    compile_component('examples/counter/counter.pvelte', 'examples/counter/output')


if __name__ == "__main__":
    main()