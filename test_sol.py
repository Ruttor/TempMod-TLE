from sol import nullstellen

def test_nullstellen():
    # Test case 1: Function becomes zero at x = 0
    def f(x):
        return x

    result = nullstellen(f, -10, 10)
    assert result == 0, "Test case 1 failed"

    # Test case 2: Function becomes zero at x = 5
    def g(x):
        return x - 5

    result = nullstellen(g, 0, 10)
    assert result == 5, "Test case 2 failed"

    # Test case 3: Function becomes zero at x = -3
    def h(x):
        return x + 3

    result = nullstellen(h, -10, 0)
    assert result == -3, "Test case 3 failed"

    
    # Test case 4: Function becomes zero at x = 4000
    def i(x):
        return x**2 - 4*x + 4 
    
    result = nullstellen(i, 0, 5)
    assert result == 2, "Test case 4 failed"
    
    print("All test cases passed")
    
test_nullstellen()
