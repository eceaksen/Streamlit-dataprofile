import numpy as np

#index 0dan başlar
data_list=[1,2,3]
arr=np.array(data_list)
print(arr)

data_list2=[[1,2],[3,4],[5,3]]
data_list2=np.array(data_list2)
print(data_list2[1,1])
print(data_list2)

#Diffrent examples
np.ones((2,4))#sıfırlarla dolu bit matrix
np.linspace(0,100,5) #1 ile 100'ü 5'e böler
np.eye(6) #diagoneller 1 olan bir fonksiyon

np.random.randint(0,10) #rndom rakamlar generate eder o aralıkta
np.random.randint(1,10,5)# 1 ile 10 arasında beş random değer
np.random.randint(5) #random 5 değer 0-1 arasında

np.random.randn(5)#gausian dist negatif sayılarda geldi

newArray=np.random.randint(1,100,10)
newArray.max()
newArray.min()
newArray.sum()
newArray.mean()
newArray.argmax() #kacıncı index max
newArray.argmin() #kacıncı index min

#session2

arr=[1,2,3,5,6,7,8,9,10]
arr[1:5]
arr[:4]
arr[::2]#baştan sona iki atlayarak
arr[:3]=25 #o aralıktaki değerler 25 oldu.
arr2[:3]

arr2=[1,2,3,5,6,7,8,9,10]
arr2=arr #dendiği zaman değişiklik yapılursa iki tarafta da yapılır
arr2=arr.copy() #birbiirnden etkilenmez

#session2.2

newArray=np.arange(1,21)#birden 21e ddegerler ardasık olustu
newArray=newArray.reshape(5,4)
newArray[:,:2]#bütün satıralr ama sütünlaı ilk iki değeri alındı.


arr=[1,2,3,5,6,7,8,9,10]
booleanArray=arr>3
arr[booleanArray] #FALSE değerleri arrayden atar truelar kalır.

#session3
arr1=np.array([1,2,3,5,6,7,8,9,10])
arr2=np.array([4,4,3,5,6,7,3,9,8])
arr1+arr2
arr1-arr2
arr1*arr2
arr1+10

