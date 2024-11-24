import numpy as np
import os.path

matrix = np.load("data/second_task.npy")

x, y, z = [], [], []

for i in range (matrix.shape[0]):
    for j in range(matrix.shape[1]):
        if matrix[i][j] > 533:
            x.append(i)
            y.append(j)
            z.append(matrix[i][j])

np.savez("result_second_task.npz", x=x, y=y, z=z)
np.savez_compressed("result_second_task_compress.npz", x=x, y=y, z=z)   

first_size = os.path.getsize('result_second_task.npz')
seconds_size = os.path.getsize('result_second_task_compress.npz')

print(f"savez = {first_size}")
print(f"savez_compressed = {seconds_size}")
print(f"diff = {first_size - seconds_size}")