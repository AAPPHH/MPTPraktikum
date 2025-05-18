import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import pandas as pd

samples = np.random.normal(3.0, 1.0, 400000)

mapped_samples = samples**2

fig, axs = plt.subplots(figsize=(8, 4), ncols=2)
df = pd.DataFrame(samples, columns=["x"])
sns.histplot(df, bins=64, ax=axs[0])

df = pd.DataFrame(mapped_samples, columns=["x**2"])
sns.histplot(df, bins=64, ax=axs[1])

plt.show()
