import numpy as np
from spektrafilm.utils.lut import compute_with_lut, warmup_luts

def mycalculation(x):
    y = np.zeros_like(x)
    y[:,:,0] = 3*x[:,:,1] + x[:,:,0]
    y[:,:,1] = 3*x[:,:,2] + x[:,:,1]
    y[:,:,2] = 3*x[:,:,0] + x[:,:,2]
    return y

warmup_luts()
sample_data = np.random.uniform(0.0, 1.0, size=(10, 10, 3))
data_finterp, lut3d = compute_with_lut(sample_data, mycalculation, xmin=0.0, xmax=1.0)
print("SUCCESS")
