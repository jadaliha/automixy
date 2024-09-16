# Automixy Documentation

Automixy is a Python package that provides reactive programming primitives.

## Classes

### binding

The `binding` class represents a mutable value that can be observed for changes.

#### Methods:

- `__init__(initial_value=None)`: Initialize a binding with an optional initial value.
- `set(new_value)`: Set a new value for the binding.
- `value`: Property to get the current value of the binding.

### reactive

The `reactive` class represents a computed value that depends on one or more bindings.

#### Methods:

- `__init__(func, *dependencies, is_lazy=True)`: Initialize a reactive with a function and its dependencies.
- `__call__()`: Get the current value of the reactive.
- `value`: Property to get the current value of the reactive.

## Usage Example