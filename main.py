# from firedom.pretty import i
from typing import Callable

class binding:
    def __init__(self, initial_value = None):
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

    def __repr__(self):
        return f"binding({self._value})"

    def __str__(self):
        return str(self._value)

class reactive:
    def __init__(self, func: Callable = lambda: None, *dependencies: binding, is_lazy: bool = True):
        self._func = func
        self._dependencies = list(dependencies)
        self._is_lazy = is_lazy
        self._observers = []
        self._value = None
        if not is_lazy:
            self._update()
        else:
            self._is_dirty = True

    def __lshift__(self, args):
        if isinstance(args, (tuple, set)):
            self._func, *self._dependencies = args
        else:
            self._func = args
            self._dependencies = []
        self._is_lazy = False
        self._setup_dependencies()
        self._update()
        return self

    def __lt__(self, args):
        if isinstance(args, (tuple, set)):
            self._func, *self._dependencies = args
        else:
            self._func = args
            self._dependencies = []
        self._is_lazy = True
        self._is_dirty = True
        self._setup_dependencies()
        return self

    def _setup_dependencies(self):
        for dep in self._dependencies:
            if isinstance(dep, binding):
                dep.add_observer(self._mark_dirty)
            elif isinstance(dep, reactive):
                dep.add_observer(self._mark_dirty)

    def _update(self):
        dep_values = [dep.value if isinstance(dep, (binding, reactive)) else dep for dep in self._dependencies]
        self._value = self._func(*dep_values)
        self._is_dirty = False
        self._notify_observers()

    def _mark_dirty(self):
        if not self._is_dirty:
            self._is_dirty = True
            self._notify_observers()

    def _notify_observers(self):
        for observer in self._observers:
            observer()

    def add_observer(self, observer):
        self._observers.append(observer)

    def __call__(self):
        if self._is_dirty:
            self._update()
        return self._value
    
    def __repr__(self):
        return f"reactive({self._func}, {self._dependencies})"
    
    @property
    def value(self):
        return self.__call__()

def PLUS_ONE(x):
    print("PLUS_ONE called")
    return x + 1  # Call x to get its value

# Usage examples
b = binding()
b.set(5)


# Eager evaluation
# PLUS_ONE(b.value) will be evaluated immediately when b.value is set the result is cached and returned when a() is called
a = reactive()
a << {PLUS_ONE, b};
print("Eager evaluation result:", a())  # Should print 6 without re-evaluating func because the value is calculated once we execute a << {func, b} and when we set b the value is recalculated and cached eagerly


# New usage example with lazy binding using <
c = reactive()
c < {PLUS_ONE, b}

# the PLUS_ONE(b.value) is not calculated till you call c(), the value is cashed until we set b again, when you need the value of c:
result = c()
print("Lazy binding result:", result)  # Should print 6

# Demonstrate that changing b's value affects both a and c
print("Updating b.value to 10")
b.set(10)
print("Updated eager evaluation result (a):", a.value)  # Should print 11
print("Updated lazy binding result (c):", c())  # should call PLUS_ONE(b.value) and print 11 

def SUM_TRIPLE(x, y, z):
    print("SUM_TRIPLE called")
    return x + y + z

B = binding(2)
A = reactive(SUM_TRIPLE, b, B, 3)
A()  # This will evaluate SUM_TRIPLE immediately

print("Value of A depends on B, and b:", A())

B.set(10)
b.set(20)
print("Value of A depends on B, and b and should be 33:", A())



def SUM_TUPLE(x, y):
    print("SUM_TUPLE called")
    return x+y
R = reactive(SUM_TUPLE, a, B)
print("Value of R depends on b and B, because a depends on b:", R())


# Ultimate Test
# reactive evaluation based on another reactive
# here a is a reactive function of b, and P is a reactive function of a and B, and b, therefore P is a reactive function of b and B
P = reactive(SUM_TRIPLE, a, B, b, is_lazy=False)
P()
