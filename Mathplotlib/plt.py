import matplotlib.pyplot as plt
import numpy as np


x = np.arange(1,5)
y = x**3

''''''
plt.figure(figsize=(15,5))
plt.subplot(1,2,1)
plt.plot([1,2,3,4], [1,4,9,16],'go', x, y, 'r^')
plt.title("First Sub-plot")
plt.xlabel(" X lable")
plt.ylabel("Y lable")

plt.subplot(1,2,2)
plt.plot([1,2,3,4], [1,4,9,16],'g', x, y, 'r')
plt.title("Second Sub-plot")
plt.xlabel(" X lable")
plt.ylabel("Y lable")
plt.suptitle("Sub-plots")
''''''


'''subplots'''
x = np.arange(1,5)
y = x**3
fig, ax = plt.subplots(nrows = 2, ncols = 2, figsize = (6,6))
ax[0,1].plot([1,2,3,4], [1,4,9,16], 'g')
ax[0,1].set_title("ax[0,1]: Squares")
ax[1,0].plot(x, y, 'r')
ax[1,0].set_title("ax[1,0]: Cubes")
plt.suptitle("Subplots")
''''''


'''Biểu đồ thanh'''
divisions = ["Div-A", "Div-B", "Div-C", "Div-D", "Div-E"]
divisions_average_marks = [70, 60, 80, 40, 50]
variances = [5, 4, 8, 6, 7]

plt.bar(divisions, divisions_average_marks, yerr = variances, color = 'green')
plt.title("Bar Graph")
plt.xlabel("Divisions")
plt.ylabel("Mark")
''''''

'''bar, legend, xticks'''
divisions = ["Div-A", "Div-B", "Div-C", "Div-D", "Div-E"]
divisions_average_marks = [70, 60, 80, 40, 50]
boy_average_marks = [65, 70, 70, 45, 60]

index = np.arange(5)
width = 0.30

plt.bar(index, divisions_average_marks, width, color='green', label = "Divison Marks")
plt.bar(index + width, boy_average_marks, width, color='blue', label = "Boys Marks")
plt.title("Bar Graph")
plt.xlabel("Divisions")
plt.ylabel("Marks")
plt.xticks(index + width/2, divisions)
plt.legend(loc = 'best')
''''''

'''bottom'''
divisions = ["Div-A", "Div-B", "Div-C", "Div-D", "Div-E"]
girl_average_marks = [70, 60, 80, 40, 50]
boy_average_marks = [65, 70, 70, 45, 60]

index = np.arange(5)
width = 0.30

plt.bar(index, girl_average_marks, width, color='red', label = "Girls Marks")
plt.bar(index, boy_average_marks, width, color='blue', label = "Boys Marks", bottom = girl_average_marks)
plt.title("Bar Graph")
plt.xlabel("Divisions")
plt.ylabel("Marks")
plt.xticks(index + width, divisions)
plt.legend(loc = 'best')
''''''

'''Biểu đồ tròn'''
firms = ["Firm A", "Firm B", "Firm C", "Firm D", "Firm E"]
market_share = [20, 25, 15, 10, 20]
Explode = [0, 0.2, 0, 0.2, 0]

plt.pie(market_share, explode = Explode, labels = firms, shadow = True, startangle = 45)
plt.axis('equal')
plt.legend(title = "list of firms")
''''''


plt.show()