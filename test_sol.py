from sol import nullstellen
import numpy as np
def test_nullstellen():
    # Test case 1: Function becomes zero at x = 0
    def f(x):
        return x

    result = nullstellen(f, -1000, 1000)
    np.testing.assert_allclose(result, 0, rtol=1e-03, err_msg='Test case 1 failed', verbose=True)

    # Test case 2: Function becomes zero at x = 5
    def g(x):
        return x - 5

    result = nullstellen(g, -1000, 1000)
    np.testing.assert_allclose(result, 5, rtol=1e-03, err_msg='Test case 2 failed', verbose=True)

    # Test case 3: Function becomes zero at x = -3
    def h(x):
        return x + 3

    result = nullstellen(h, -1000, 1000)
    np.testing.assert_allclose(result, -3, rtol=1e-03, err_msg='Test case 3 failed', verbose=True)

    
    # Test case 4: Function becomes zero at x = 2
    def i(x):
        return x**2 - 4*x + 4 
    
    result = nullstellen(i, -1000, 1000)
    np.testing.assert_allclose(result, 2, rtol=1e-03, err_msg='Test case 4 failed', verbose=True)
    
    print("All test cases passed")
    
test_nullstellen()
