import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

data = pd.read_csv("surveyb2.csv")
data.convert_dtypes()

data["pie"].value_counts().plot.bar(color="#ffcc99")

plt.title("Pie Popularity")
plt.xlabel("Pie Type")
plt.ylabel("# of responses")
plt.tight_layout()
plt.show()