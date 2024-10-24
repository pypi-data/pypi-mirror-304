import pandas as pd
import matplotlib.pyplot as plt
df=pd.read_csv('MelaSales.csv')
df.pivot_table(index='Week',columns='Day',values='Sales').plot(kind='bar')
plt.title('Sales for Three Weeks')
plt.xlabel('Week')
plt.ylabel('Sales')
plt.show()
