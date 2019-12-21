



def async_wrapper( func, *args):
	func(*args)

def test_func( a, b, c):
	print("a: {}, b: {}, c:{}".format(a, b, c))

async_wrapper( test_func, "flerb", "bleeb", "sneetch")

