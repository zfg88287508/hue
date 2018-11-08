def expr_min(data):
    result = (data[0], 0)
    for i, v in enumerate(data):
        if v < result[0]:
            result = (v, i)
    return result


def expr_max(data):
    result = (data[0], 0)
    for i, v in enumerate(data):
        if v > result[0]:
            result = (v, i)
    return result


def expr_avg(data):
    return (sum(data) / float(len(data)), None)


def expr_sum(data):
    return (sum(data), None)


class Expr:

    @classmethod
    def evaluate(self, expr, vars):
        return eval(compile(expr, "<string>", "eval"), vars)
