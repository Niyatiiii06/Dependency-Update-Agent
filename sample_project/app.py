import pandas as pd

df = pd.DataFrame({"name": ["A", "B"]})
df.append({"name": "C"}, ignore_index=True)