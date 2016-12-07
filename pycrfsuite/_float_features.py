from __future__ import print_function, absolute_import


class FloatFeatures(object):
    def __init__(self, values):
        if not isinstance(values, list):
            raise ValueError("Values should be an instance of list()")
        try:
            self.values = [float(v) for v in values]
        except ValueError:
            print("All elements in values should be castable to type float.", file=sys.stderr)
            raise
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
