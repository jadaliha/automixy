import weakref


def print_debug(*args):
    ...
    # print('\033[91mDEBUG: \033[0m', *args )

class binding:
    def __init__(self, initial_value=None):
        self._value = initial_value
        self._observers = set()  # Change to regular set
        print_debug(f"Created binding with initial value {initial_value}")

    @property
    def value(self):
        print_debug(f"Accessing binding value: {self._value}")
        return self._value

    def set(self, new_value):
        print_debug(f"Attempting to set binding value from {self._value} to {new_value}")
        if self._value != new_value:
            self._value = new_value
            print_debug(f"Value changed. Notifying {len(self._observers)} observers")
            self._notify_observers()
        else:
            print_debug("Value unchanged, not notifying observers")

    def add_observer(self, observer):
        print_debug(f"Adding observer {observer} to binding")
        self._observers.add(observer)
        print_debug(f"Current observers: {list(self._observers)}")

    def _notify_observers(self):
        print_debug(f"Notifying {len(self._observers)} observers")
        for observer in list(self._observers):
            print_debug(f"Notifying observer {observer}")
            observer()._on_dependency_change()

class reactive:
    def __init__(self, func, *dependencies, is_lazy=True):
        self._func = func
        self._dependencies = dependencies
        self._is_lazy = is_lazy
        self._observers = set()  # Change to regular set
        self._value = None
        self._is_dirty = True
        print_debug(f"Created reactive with func {func}, dependencies {dependencies}, is_lazy={is_lazy}")
        self._setup_dependencies()
        if not is_lazy:
            self._update()

    def _setup_dependencies(self):
        for dep in self._dependencies:
            if isinstance(dep, (binding, reactive)):
                print_debug(f"Setting up dependency {dep}")
                dep.add_observer(weakref.ref(self))

    def _on_dependency_change(self):
        print_debug(f"Dependency changed for reactive {self}")
        if self._is_lazy:
            self._mark_dirty()
        else:
            self._update()
        self._notify_observers()  # Add this line to propagate changes

    def _update(self):
        print_debug(f"Updating reactive {self}")
        dep_values = [dep.value if isinstance(dep, (binding, reactive)) else dep for dep in self._dependencies]
        new_value = self._func(*dep_values)
        print_debug(f"Calculated new value: {new_value}")
        if self._value != new_value:
            self._value = new_value
            self._is_dirty = False
            print_debug(f"Value changed. Notifying {len(self._observers)} observers")
            self._notify_observers()
        else:
            print("DEBUG: Value unchanged")

    def _mark_dirty(self):
        if not self._is_dirty:
            print_debug(f"Marking reactive {self} as dirty")
            self._is_dirty = True
            self._notify_observers()

    def _notify_observers(self):
        print_debug(f"Notifying {len(self._observers)} observers of reactive {self}")
        for observer in list(self._observers):
            print_debug(f"Notifying observer {observer}")
            observer()

    def add_observer(self, observer):
        print_debug(f"Adding observer {observer} to reactive {self}")
        self._observers.add(observer)
        print_debug(f"Current observers: {list(self._observers)}")

    def __call__(self):
        print_debug(f"Calling reactive {self}")
        if self._is_dirty:
            self._update()
        return self._value

    @property
    def value(self):
        return self.__call__()

    def __del__(self):
        print_debug(f"Cleaning up reactive {self}")
        weakref.getweakrefs(self)
        for dep in self._dependencies:
            if isinstance(dep, (binding, reactive)):
                dependancies = set()
                while dep._observers:
                    o = dep._observers.pop()
                    if o() == self:
                        break
                    else:
                        dependancies.add(o)
                while dependancies:
                    o = dependancies.pop()
                    dep._observers.add(o)
