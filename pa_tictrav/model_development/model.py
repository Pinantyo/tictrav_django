import pandas as pd 
import numpy as np

# Statistik
from scipy.stats.stats import pearsonr  


# Model tensorflow
import tensorflow as tf

# Model Path
import os

from django.http import Http404



from . import dataPreprocessing as dp

""" 
Sort:
	Quicksort Referensi GeeksforGeeks dan Sort
"""
def parti(numpyArray, minIndex, maxIndex,sort,targetIndex):
    # Inisialisasi pivot dengan nilai index terakhir
    pivot = numpyArray[maxIndex]
    i=minIndex-1
    if(sort=='desc'):
        for j in range(minIndex,maxIndex):
            if(numpyArray[j][targetIndex] >= pivot[targetIndex]): #Bandingkan nilai array dengan pivot
                i+=1
                numpyArray[i],numpyArray[j] = numpyArray[j],numpyArray[i] # Menukar nilai dari index

        numpyArray[i+1],numpyArray[maxIndex] = numpyArray[maxIndex],numpyArray[i+1]
        
    else:
        for j in range(minIndex,maxIndex):
            if(numpyArray[j][targetIndex] <= pivot[targetIndex]):
                i+=1
                numpyArray[i],numpyArray[j] = numpyArray[j],numpyArray[i]

        numpyArray[i+1],numpyArray[maxIndex] = numpyArray[maxIndex],numpyArray[i+1]
    
    return i+1

def quicksort(numpyArray, minIndex, maxIndex, sort='asc',targetIndex=0):
    # Pengecekan apakah nilai index lebih kecil dibandingkan panjang array
    if(minIndex<maxIndex):
        partition = parti(numpyArray, minIndex, maxIndex,sort,targetIndex)
        # Kiri
        quicksort(numpyArray, minIndex, partition-1,sort,targetIndex)
        # Kanan
        quicksort(numpyArray,partition+1,maxIndex,sort,targetIndex)

# Model (Nanti dipindah di dalam folder baru)
class Model:
    def __init__(self, modelName, data):
        self.__model = tf.keras.models.load_model(os.getcwd()+f'//model_development//model//Multiclass//{modelName}.h5')
        self.__data = pd.DataFrame(data)

    def predict(self,userId,age,target=None):
        features = ['user_id','place_id','age']
        if(not features):
            return None

        recommend = None
        """
            Untuk keperluan pengujian performa model 
            if(target):
            y = [data[i] for i in target]
            result = self.__modelName.predict(x=x,y=y)
            else:
        """

		# self.__model.predict(x=x)

		# Penyeleksian fitur data yang akan digunakan untuk prediksi hasil model.
        data = self.generateUserData(userId, age)        
        try:
            recommend = self.getRecommendation(userId,features,data)

			# print(f'Recommended sebelum sort: {recommend}')
            # print(recommend)
        except:
            print("error 500")
            # raise Http404()
        else:
            recommend = [i for i in recommend[:5]]
            """
			     Diisi dengan rekomendasi berdasarkan trending sekarang
            """
            print(recommend)
        return recommend

    """
        pembuatan data prediksi dan mendapatkan rekomendasi tempat
    """
    def generateUserData(self, userId, age):
        length = self.__data.shape[0]
        newDf = pd.DataFrame({
	        'user_id':[userId for i in range(length)],
	        'place_id':[i for i in self.__data.place_id],
	        'age':[age for i in range(length)],
	        'category':[i for i in self.__data.category]
        })
        newDf['category'] = newDf['category'].replace([3, 2, 5, 4, 1],[2, 1, 4, 3, 0])
        return newDf

    """
        Kumpulan fungsi modul yang digunakan di backend nantinya untuk melakukan pengolahan data
    """
    def getRecommendation(self, userId, fitur, data):
        targetUser = data[data['user_id']==userId]
        placeId = np.array(targetUser['place_id'])
        x = [targetUser[i] for i in fitur]
        recommendation = self.__model.predict(x=x)
        placeRecommendation = [[placeId[i],np.argmax(recommendation[i]),max(recommendation[i])] for i in range(len(recommendation))]

        # Penyortiran rekomendasi tempat
        quicksort(placeRecommendation,0,len(placeRecommendation)-1,'desc',2)
        quicksort(placeRecommendation,0,len(placeRecommendation)-1,'desc',1)

        # Pengambilan tempat wisata yang telah disortir
        placeRecommendation = [i[0] for i in placeRecommendation]
        return placeRecommendation


"""
Cara Penggunaan:


colabs = colaborative_calculation(data_tourism)
userSim = colabs.userSimilarity(1,1)
userCor = colabs.userCorr(1,1)
userNearest = colabs.kSimilarUser(1,25)


recommended_data = colaborative_calculation(data_item).itemRecommendedByItem(place_wisat, k)

"""
class colaborative_calculation_statistik:
    def __init__(self, data):
        self.__listUser = np.array(data)
        self.__df_data  = data
    """
        Kumpulan fungsi untuk melakukan perhitungan aritmatika menggunakan cosine similarity, 
        dan pearson corr
    """
    # Correlation
    def userCorr(self,user1=0,user2=0):
        if(user1 and user2 == 0):
            return None
        return pearsonr(self.__listUser[user1-1,1:],self.__listUser[user2-1,1:])[1]
    
    # Cosine Similarity
    def userSimilarity(self,user1=0,user2=0):
        if(user1 and user2 == 0):
            return None
        return np.dot(self.__listUser[user1-1,1:],self.__listUser[user2-1,1:])/(np.linalg.norm(self.__listUser[user1-1,1:])*np.linalg.norm(self.__listUser[user2-1,1:]))
    
    # K User
    def kSimilarUser(self, user1=0, k=0):
        listCorrSim = []
        """
            Perhitungan user1 dengan semua user yang terdapat pada data
        """
        for i in range(0,len(self.__listUser)):
            listCorrSim.append((i+1,self.userCorr(user1, i+1),self.userSimilarity(user1,i+1)))
        
        listCorrSim = np.sort(np.array(listCorrSim, dtype=[('user', 'int'), ('p-value', float),('similarity', float)]),order=['similarity','p-value'])
        """
            Hanya mengambil data teratas berjumlah k
        """
        return listCorrSim[::-1][1:k+1]
    
    """
        Fungsi yang digunakan untuk perhitungan korelasi
    """
   
    # Pengambilan rekomendasi tempat yang memiliki korelasi tinggi berdasarkan kunjungan beberapa user
    """
        k = Jumlah item yang di rekomendasikan
    """
    def itemRecommendedByItem(self, placeName, k):
        if(not (placeName or k)):
            return None
        __data = self.__df_data.corr()
        recommend = pd.DataFrame(__data.iloc[__data.columns.get_loc(f'Place_Name_{placeName}'),
                                           :]).sort_values(by=__data.iloc[__data.columns.get_loc(f'Place_Name_{placeName}'),:].name,
                                                           ascending=False)[1:k+1]
        return recommend.index
    
    """
        Pengambilan data item yang memiliki
        kemiripan berdasarkan rating
    """
    def itemSimilarByItem(self, placeName, k):
        if(not (placeName or k)):
            return None

        listSimItem = []
        __data = self.__df_data.T
        placeWisat = list(__data.index)

        item1 = np.array(__data)[list(__data.index).index("Place_Name_"+placeName),:]
        for i in placeWisat:
            item2 = np.array(__data)[list(__data.index).index(i),:]
            listSimItem.append((i,
                                np.dot(item1,item2,)/(np.linalg.norm(item1)*np.linalg.norm(item2))))
        
        
        quicksort(listSimItem, 0, len(listSimItem)-1,'desc',targetIndex=1)
        return listSimItem[1:k+1]

