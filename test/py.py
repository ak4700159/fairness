class Stock:
    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

    def cost(self):
        return self.shares * self.price

    def sell(self, nshares):
        self.shares -= nshares

stockA = Stock("A", 100, 10.0)
# stockA.new_const = 200 # 새로운 속성 추가 
# print(stockA.__dict__)
# print(Stock.__dict__)

def logged(func):
    def wrapper(*args, **kwargs):
        print('Calling', func.__name__)
        return func(*args, **kwargs)
    return wrapper

def timethis(func):
    def wrapper(*args, **kwargs):
        import time
        start = time.time()
        r = func(*args, **kwargs)
        end = time.time()
        print('%s.%s: %f' % (func.__module__, func.__name__, end-start))
        return r
    return wrapper

# 무조건 timethis 함수에 
@timethis
def count(x):
    while x >= 0:
        yield x
        x -= 1

@timethis
def custom_sum(x):
    total = 0
    for i in range(x):
        total += i
    return total

custom_sum(10000000)

# for i in count(100000):
#     print("decreasing count : ", i * i)
