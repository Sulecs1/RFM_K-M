############################################################
#   Customer Segmentation with K-Means Algorithm           #
############################################################


#InvoiceNo: Fatura numarası. Her işleme yani faturaya ait eşsiz numara. Eğer bu kod C ile başlıyorsa işlemin iptal edildiğini ifade eder.
#StockCode: Ürün kodu. Her bir ürün için eşsiz numara.
#Description: Ürün ismi
#Quantity: Ürün adedi. Faturalardaki ürünlerden kaçar tane satıldığını ifade etmektedir.
#InvoiceDate: Fatura tarihi ve zamanı.
#UnitPrice: Ürün fiyatı (Sterlin cinsinden)
#CustomerID: Eşsiz müşteri numarası
#Country: Ülke ismi.Müşterinin yaşadığı ülke


#Kütüphanelerin Eklenmesi
import pandas as pd
import numpy as np
import datetime as dt
import seaborn as sns
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

#tüm sütunları ve satırların görüntülenmesi
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

#virgülden sonra gösterilecek olan sayı miktarı
pd.set_option('display.float_format', lambda x: '%.0f' % x)

data = pd.read_excel(r"C:\Users\Suleakcay\PycharmProjects\pythonProject3\HAFTA3\online_retail_II.xlsx", sheet_name="Year 2010-2011")
#bize eksik değerleri getir!
df.isnull().sum()
df.shape
df.info() # verilerimiz tipi hakkında bilgi aldık
df.columns

#Veri Setini İnceleme İşlemi #

#1- Öbek sayınızı (K) seçtikten sonra rastgele K adet merkez seçilir.
#2- Her veri noktasıyla merkez arasındaki uzaklık hesaplandıktan sonra en yakın öbeğe atanır.
#3- Daha sonra öbeklerde bulunan verilerin ortalamasına göre yeni merkezler belirlenir ve tekrardan noktalar yakın olduğu öbeklere atanır.
#4- Bu işlem öbek merkezlerinde değişiklik olmayana kadar devam e