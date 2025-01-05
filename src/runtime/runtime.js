function createState(initialValue) {
    let subscribers = new Set();
    let value = initialValue;
    
    return {
        get: () => value,
        set: (newValue) => {
            value = newValue;
            subscribers.forEach(fn => fn(value));
        },
        subscribe: (fn) => {
            subscribers.add(fn);
            fn(value); // Initial call
            return () => subscribers.delete(fn);
        }
    };
}