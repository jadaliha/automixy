
from firedom.pretty import i
from main import reactive, binding
def PLUS_ONE(x):
    print("PLUS_ONE called")
    return x + 1  # Call x to get its value

# Usage examples
b = binding(5)

# Eager evaluation
# PLUS_ONE(b.value) will be evaluated immediately when b.value is set the result is cached and returned when a() is called
a = reactive(PLUS_ONE, b, is_lazy=False)
print("Eager evaluation result:", a())  # Should print 6 without re-evaluating func because the value is calculated once we execute a << {func, b} and when we set b the value is recalculated and cached eagerly


# New usage example with lazy binding using <
c = reactive(PLUS_ONE, b, is_lazy=True)

# the PLUS_ONE(b.value) is not calculated till you call c(), the value is cashed until we set b again, when you need the value of c:
result = c()
print("Lazy binding result:", result)  # Should print 6

# Demonstrate that changing b's value affects both a and c
b.set(16)
print("Updated eager evaluation result (a):", a.value)  # Should print 11
print("Updated lazy binding result (c):", c())  # should call PLUS_ONE(b.value) and print 11 

def SUM_TRIPLE(x, y, z):
    print("SUM_TRIPLE called")
    return x + y + z

B = binding(2)
A = reactive(SUM_TRIPLE, b, B, 3, is_lazy=True)
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