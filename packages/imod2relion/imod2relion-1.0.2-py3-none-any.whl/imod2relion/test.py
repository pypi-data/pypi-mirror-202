import pandas as pd
import numpy as np
# result = pd.DataFrame()
# for i in range(0, df.shape[0], 2):
#     df_x_mean = (df['X'].iloc[i] + df['X'].iloc[i+1]) / 2
#     df_y_mean = (df['Y'].iloc[i] + df['Y'].iloc[i+1]) / 2
#     df_z_mean = (df['Z'].iloc[i] + df['Z'].iloc[i+1]) / 2
#     result = result.append({'X': df_x_mean, 'Y': df_y_mean, 'Z': df_z_mean}, ignore_index=True)

# print(result)

# data = {'X': [1, 2, 3, 4, 5, 6], 'Y': [7, 8, 9, 10, 11, 12], 'Z': [13, 14, 15, 16, 17, 18]}
# df = pd.DataFrame(data)

# result = pd.concat([pd.DataFrame({'rlnCoordinateX': [(df['X'].iloc[i] + df['X'].iloc[i+1]) / 2],
#                                    'rlnCoordinateY': [(df['Y'].iloc[i] + df['Y'].iloc[i+1]) / 2],
#                                    'rlnCoordinateZ': [(df['Z'].iloc[i] + df['Z'].iloc[i+1]) / 2]}) 
#                     for i in range(0, df.shape[0], 2)], ignore_index=True)

# print(result)


data = {'X': [1, 2, 3, 4, 5, 6], 'Y': [7, 8, 9, 10, 11, 12], 'Z': [13, 14, 15, 16, 17, 18]}
df = pd.DataFrame(data)

def cal_euleangle(x1,x2,y1,y2,z1,z2):
    x = x2 - x1
    y = y2 - y1
    z = z2 - z1
    if x == 0:
        phi = np.pi / 2
    else:
        phi = np.arctan2(y, x)
    if z == 0:
        theta = np.pi / 2
    else:
        theta = np.arctan2(np.sqrt(x ** 2 + y ** 2), z)
    psi = 0
    phi = np.rad2deg(phi)
    theta = np.rad2deg(theta)
    psi = np.rad2deg(psi)
    return phi, theta, psi

for i in range(0, df.shape[0], 2):
    result = cal_euleangle(df['X'].iloc[i], df['X'].iloc[i], df['Y'].iloc[i], df['Y'].iloc[i+1], df['Z'].iloc[i], df['Z'].iloc[i+1])

print(cal_euleangle(0,1,0,1,0,1))