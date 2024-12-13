import numpy as np



def cohen_d(x, y):
    x, y = np.array(x, dtype=float), np.array(y, dtype=float)
    nx, ny = len(x), len(y)
    
    if nx < 2 or ny < 2:
        print("Warning nan")
        return np.nan
    
    mean_x, mean_y = np.mean(x), np.mean(y)
    std_x, std_y = np.std(x, ddof=1), np.std(y, ddof=1)
    pooled_std = np.sqrt(((nx - 1) * std_x**2 + (ny - 1) * std_y**2) / (nx + ny - 2))
    
    if pooled_std == 0:
        print("Warning nan")
        return np.nan
    
    return (mean_x - mean_y) / pooled_std