#Lab 1. Численно интегрирование

def integrate(f, a, b, *, n_iter=1000):
    h = (b - a) / n_iter
    s = 0
    x = a
    while (x <= (b - h)):
        s += f(x)
        x += h
    res = round(h * s, 8)
    return res


def test():
    from math import sin, cos, tan
    assert integrate(sin, 0, 1)
    assert integrate(cos, 0, 1)
    assert integrate(tan, 0, 1)


if __name__ == '__main__':
    test()
    from math import sin, cos, tan
    print('Tests')
    print('Result sin =', integrate(sin, 0, 1))
    print('Result cos =', integrate(cos, 0, 1))
    print('Result tan =', integrate(tan, 0, 1))