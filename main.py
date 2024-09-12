from typing import Callable

class binding:
    def __init__(self, initial_value):
        self._value = initial_value
        self._observers = []

    @property
    def value(self):
        return self._value

    def set(self, new_value):
        if self._value != new_value:
            self._value = new_value
            for observer in self._observers:
                observer()

    def add_observer(self, observer):
        self._observers.append(observer)

class reactive:
    def __init__(self):
        self._func = None
        self._dependencies = []
        self._value = None
        self._is_lazy = False
        self._is_dirty = True

    def __lshift__(self, args):
        self._func, *self._dependencies = args
        self._is_lazy = False
        self._update()
        for dep in self._dependencies:
            if isinstance(dep, binding):
                dep.add_observer(self._update)
        return self

    def __lt__(self, args):
        self._func, *self._dependencies = args
        self._is_lazy = True
        self._is_dirty = True
        for dep in self._dependencies:
            if isinstance(dep, binding):
                dep.add_observer(self._mark_dirty)
        return self

    def _update(self):
        dep_values = [dep.value if isinstance(dep, binding) else dep for dep in self._dependencies]
        self._value = self._func(*dep_values)
        self._is_dirty = False

    def _mark_dirty(self):
        self._is_dirty = True

    def __call__(self):
        if self._is_lazy and self._is_dirty:
            self._update()
        return self._value

    @property
    def value(self):
        return self.__call__()

def func(x):
    print("function called")
    return x + 1  # Call x to get its value

# Usage examples
b = binding(5)  # Set initial value in constructor

# Eager evaluation
# func(b.value) will be evaluated immediately when b.value is set the result is cached and returned when a() is called
a = reactive()
a << {func, b}
print("Eager evaluation result:", a())  # Should print 6 without re-evaluating func because the value is calculated once we execute a << {func, b} and when we set b the value is recalculated and cached eagerly


# New usage example with lazy binding using <
c = reactive()
c < {func, b}

# the func(b.value) is not calculated till you call c(), the value is cashed until we set b again, when you need the value of c:
result = c()
print("Lazy binding result:", result)  # Should print 6

# Demonstrate that changing b's value affects both a and c
print("Updating b.value to 10")
b.set(10)
print("Updated eager evaluation result (a):", a.value)  # Should print 11
print("Updated lazy binding result (c):", c())  # should call func(b.value) and print 11 

