import numpy as np
def generate_random_number(strt_num: int, end_num: int):
    print(np.random.randint(strt_num, end_num))
    return {"lists": np.random.randint(strt_num, end_num)}