def add_to_gen(x):

    def add_to(data):
        return data + x

    return add_to


def mult_with_gen(x):

    def mult_with(data):
        return data * x

    return mult_with
