import matplotlib.pyplot as plt
Height=[121.9,124.5,129.5,134.6,139.7,147.3,152.4,157.5,162.6]
Weight=[19.7,21.3,23.5,25.9,28.5,32.1,35.7,39.6,43.2]
Age=[8,9,10,11,12,13,14,15,16]
plt.plot(Age,Height,label='Height')
plt.plot(Age,Weight,label='Weight')
plt.xlabel('Age')
plt.ylabel('Height/Weight')
plt.title('Average Height and Weight of Persons')
plt.legend()
plt.show()
