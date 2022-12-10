# since the model is linear with just need to solve a linear system
import numpy as np
from phe import pailler as pl
from homo_encryption import query_pred

D = 10
b = 1

keys = pl.generate_pailler_keypair()
x, y = [], []
# We know D=10, so we need D+1 queries
for i in range(D+1):
    rand = np.random.random_sample(D)
    y.append(query_pred(rand, keys))
    # Append the bias
    x.append(np.append(rand, b))

x, y = np.array(x), np.array(y)
ans = np.linalg.solve(x, y)
wi, bias = ans[:-1], ans[-1]
print(f'w_i={wi}, b={bias}')