def impute_default_gen(default):

    def impute(data):
        return data.fillna(default)

    return impute

def impute_zero(data):
    return data.fillna(0)

