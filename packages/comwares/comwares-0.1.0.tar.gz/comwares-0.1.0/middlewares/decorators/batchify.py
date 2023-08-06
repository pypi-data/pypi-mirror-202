import functools


def batchify(batch_size=500):
    def decorator(f):
        def wrapper(self, *args, **kwargs):
            data = args[0]
            assert isinstance(data, list), "args[0] must be a list."
            total = len(data)
            results = None
            for i in range(total // batch_size + 1):
                low = i * batch_size
                high = min((i + 1) * batch_size, total)
                data_slice = data[low:high]
                if len(data_slice) > 0:
                    result = f(data_slice)
                    if isinstance(result, dict):
                        if results is None:
                            results = dict()
                        results = {**results, **result}
                    elif result is not None:
                        if results is None:
                            results = []
                        results += result
            return results
        return wrapper
    return decorator


if __name__ == '__main__':

    test_data = [i for i in range(1000)]

    @batchify(batch_size=10)
    def inner_product(data: list):
        print(str(data))
        prod = 1
        for num in data:
            prod *= num
        print(f'product = {prod}')

    inner_product(test_data)
