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

df = pd.read_excel(r"C:\Users\Suleakcay\PycharmProjects\pythonProject3\HAFTA3\online_retail_II.xlsx", sheet_name="Year 2010-2011")
#bize eksik değerleri getir!
df.isnull().sum()
df.shape
df.info() # verilerimiz tipi hakkında bilgi aldık
df.columns


#Değişkenlerimizi Bulmaya Başlayalım!
print(f"Total number of observations:, df.shape[0]")
cat_cols = [col for col in df.columns if df[col].dtypes == "O"]
print(f"Categorical Variables:,{len(cat_cols)}:{cat_cols}")
num_cols = [col for col in df.columns if df[col].dtypes != "O"]
print(f"Numerical Variables:,{len(num_cols)}:{num_cols}")
num_but_num = [col for col in df.columns if df[col].nunique() < 4500 and df[col].dtypes != "O"]#!2.sayısal olan
print(f"Numerical Variables:,{len(num_but_num)}:{num_but_num}")
date_time = [col for col in df.columns if df[col].dtypes == "datetime64[ns]"]
print(f"Datetime Variables:,{len(date_time)}:{date_time}")

#eşsiz ürün sayısı:
df["Description"].nunique()

#eşsiz müşteri sayısı:
df["Customer ID"].nunique()

#Ürün çeşitlerimizin sayısı?
df["Description"].value_counts().head()     #value_counts değişken değerlerimizin sayısına ulaştık

#Her ülkeden toplamda kaç adet vardır?
df["Country"].value_counts().head()

#En çok sipariş eden ülke kim,ürün adedi?Kim o zengin ülke?? :)
df.groupby("Country").agg({"Quantity":"sum"}).sort_values("Quantity", ascending=False).head()

#Peki en çok tercih edilen ürünümüz ne ?
df.groupby("Description").agg({"Quantity":"sum"}).sort_values("Quantity", ascending=False).head()
df.reset_index(inplace=True)

#Toplam kesilen fatura sayısı nedir?
df["Invoice"].nunique()

#ürün kodu sayısı?
df["StockCode"].nunique()

#en pahalı ürünler hangileridir?
df.sort_values("Price", ascending=False).head(30)

# fatura basina ortalama kac para kazanilmistir?
df = df[~df["Invoice"].str.contains("C", na=False)] #na =False yaptık
df["TotalPrice"] = df["Quantity"] * df["Price"] #Burada ürünümüzün adedi ve ürünümüzün fiyatını çarpıp fiyatı bulduk

###############################################################
# Data Preparation- >veri ön işleme                           #
###############################################################
#bilinmeyen değerleri kaldırma işlemi gerçekleştiriyorum :)
df.isnull().sum() #eksik gözlem değerlerini gözlemledim
df.dropna(inplace=True) #eksik gözlem değerlerini kaldırdım
df.shape #boyut bilgisi
#Kartiller değerleri belirleyip oranlarına baktım
df.describe([0.01,0.05,0.10,0.25,0.50,0.75,0.90,0.95,0.99]).T #Buradaki incelemelerimi göre Price değişkeninde
#sıkıntılar mevcut!
###############################################################
#         Calculating RFM Metrics(Hesaplama İşlemi)           #
###############################################################
#Receny=Bugünün  tarihi -Son satın alma tarihi

df["InvoiceDate"].max()   #veri setindeki son tarih
df["InvoiceDate"].min()
thisday=dt.datetime(2011, 12, 12) #son tarihten 3 gün sonrasını aldık :)

rfm_ = df.groupby('Customer ID').agg({'InvoiceDate': lambda date: (thisday-date.max()).days,
                                     'Invoice': lambda num: len(num),
                                     'TotalPrice': lambda TotalPrice: TotalPrice.sum()})

rfm_.columns = ['Recency', 'Frequency', 'Monetary']

rfm_.head()
rfm_ = rfm_[(rfm_["Monetary"]) > 0 & (rfm_["Frequency"] > 0)]

#############################################################
#               RFM SKOR HESAPLAMA İŞEMİ                    #
#############################################################
#qcut ile çeyrekliğe göre  küçükten büyüğe doğru büyüyor
rfm_["Recency_Score"] = pd.qcut(rfm_['Recency'], 5, labels=[5, 4, 3, 2, 1])# 1 gün önce geldiyse 5 puan
rfm_["Frequency_Score"] = pd.qcut(rfm_['Frequency'], 5, labels=[1, 2, 3, 4, 5])
rfm_["Monetary_Score"] = pd.qcut(rfm_['Monetary'], 5, labels=[1, 2, 3, 4, 5])

#string tipine  çevirdim ve birleştirip RFMSCORE sutünuna yerleştirdim.
rfm_["RFMSCORE"] = (rfm_['Recency_Score'].astype(str)+rfm_['Frequency_Score'].astype(str)+rfm_['Monetary_Score'].astype(str))

#En iyi müşteriler gösterilmektedir.
rfm_[rfm_["RFMSCORE"] == "555"].head()

##En kötü müşteriler gösterilmektedir.
rfm_[rfm_["RFMSCORE"] == "111"].head()

# RFM isimlendirmesi regex->herhangi bi text içerisinde yakalama işlemi,feature türetmek içinde bizim
#segment isimlendirilmesi yaptık
segment_map = { #sözlük oluşturduk
    r'[1-2][1-2]': 'Hibernating',
    r'[1-2][3-4]': 'At_Risk',
    r'[1-2]5': 'Cant_Loose',
    r'3[1-2]': 'About_to_Sleep',
    r'33': 'Need_Attention',
    r'[3-4][4-5]': 'Loyal_Customers',
    r'41': 'Promising',
    r'51': 'New_Customers',
    r'[4-5][2-3]': 'Potential_Loyalists',
    r'5[4-5]': 'Champions'
}

rfm_['Segment'] = rfm_['Recency_Score'].astype(str) + rfm_['Frequency_Score'].astype(str)


rfm_['Segment'] = rfm_['Segment'].replace(segment_map, regex=True)
#bunun keylerine göre arama yap yakaladığını value değerler ile değiştir dedik ;)
rfm_.head()



#1- Öbek sayınızı (K) seçtikten sonra rastgele K adet merkez seçilir.
#2- Her veri noktasıyla merkez arasındaki uzaklık hesaplandıktan sonra en yakın öbeğe atanır.
#3- Daha sonra öbeklerde bulunan verilerin ortalamasına göre yeni merkezler belirlenir ve tekrardan noktalar yakın olduğu öbeklere atanır.
#4- Bu işlem öbek merkezlerinde değişiklik olmayana kadar devam e