from bs4 import BeautifulSoup
import re
import os
import matplotlib.pyplot as plt
import numpy as np


'''tu dien & vietnamese stopword'''
f0 = open(r'Dict-UTF8.txt', 'r', encoding='utf-8')
f=f0.read()
#print(f)

sw0 = open(r'vnstw.txt', 'r', encoding = 'utf8')
sw=sw0.read()
#print(sw)
''''''


'''file xml'''
# allfile = os.listdir(r'D:\Tai Lieu\20191\PROJ1\project1\Dantri_xml_60k')
# for file in allfile: #duyet tat ca cac file
#     f1 = open(file, 'r', encoding='utf-8')
#     soup1 = BeautifulSoup(f1, 'lxml')
#     soup = soup.find_all('body') #tach body
#     body1=re.sub('[.,:;!?"()-]', '', soup) #tach cau
#     body=body1.lower() # dua ve chu thuong
''''''


'''Test'''
body0 = u'(Dân trí) - 2014 có thể nói là năm đại hỷ của làng giải trí Việt khi nhiều tên tuổi nổi tiếng đều lần lượt lên xe hoa. Mỗi đám cưới mang một phong cách khác nhau nhưng có một điểm chung là đều thu hút sự quan tâm đặc biệt là của công chúng.'
body1=re.sub('[.,:;!?"()-]', '', body0)
body=body1.lower()
#print(body)
''''''


'''tach tu''' 
#tu dai nhat co 4 am tiet
a = body.split(' ') #dua body ve dang list moi phan tu la 1 am tiet
j = len(a) #moi phan tu la 1 am tiet
#print(j)
i = 0
o = ''
done = False
#print(a[0])="dong"

while(i<j) and (not done):
    #print(i)
    if (i == j-1):
        o = ' '.join([o, a[i]])
        done = True
    elif(i <= j-1):
        if i >= j - 2:
            tu2 = '_'.join([a[i], a[i+1]])
            if tu2 in f:
                o = ' '.join([o, tu2])
                i += 2
            else:
                o = ' '.join([o, a[i]])
                i += 1
        elif i >= j-3:
            tu3 = '_'.join([a[i], a[i+1], a[i+2]])
            tu2 = '_'.join([a[i], a[i+1]])
            if tu3 in f: 
                o = ' '.join([o, tu3])
                i += 3
            elif tu2 in f:
                o = ' '.join([o, tu2])
                i += 2
            else:
                o = ' '.join([o, a[i]])
                i+=1
        elif(i <= j-4):
            tu4 = '_'.join([a[i], a[i+1], a[i+2], a[i+3]])
            tu3 = '_'.join([a[i], a[i+1], a[i+2]])
            tu2 = '_'.join([a[i], a[i+1]])
            if tu4 in f:
                 o = ' '.join([o, tu4])
                 i += 4
                 
            elif tu3 in f:
                 o = ' '.join([o, tu3])
                 i += 3
                 
            elif tu2 in f:
                 o = ' '.join([o, tu2])
                 i += 2
                 
            else:
                 o = ' '.join([o, a[i]])
                 i += 1
                 
    #print(o)
    #print(type(o))
#print(o)
''''''    
    

'''loai bo stopword'''
o1 = o.split(' ') #dua ve mang words
#print(o1)

'''test'''
# s = o1[19]
# o1.remove(s)
# print(s)
# print(o1)

for i1 in range(20):
    s = o1[i1]
    #print(i1)
    #print(s)
    if s in sw:
        #print(s)
        o1.remove(s)
print(o1)
#print(len(o1))
''''''


'''output file txt'''
#     fn = open(r'output.txt', 'w')
#     fn.write(o)
''''''


'''trực quan hóa'''
'''đếm từ'''
count = np.ones(len(o1))
print("Số lượng các từ:")
for i in range(len(o1)):
    for j in range(i+1, len(o1)):
        if (o1[i] == o1[j]):
            count[i] = count[i]+1
            #count = np.delete(count, j)
    print(o1[i],":", count[i], "lần")


'''plot'''
divisions = o1
print(divisions)
divisions_average_marks = count

plt.bar(divisions, divisions_average_marks)
plt.title("Trực quan hóa")
plt.xlabel("Các từ")
plt.ylabel("Số lượng")
plt.show()