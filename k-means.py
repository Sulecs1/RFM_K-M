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
import seaborn as sns
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

#tüm sütunları ve satırların görüntülenmesi
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

#virgülden sonra gösterilecek olan sayı miktarı
pd.set_option('display.float_format', lambda x: '%.0f' % x)

data = pd.read_excel(r"C:\Users\Suleakcay\PycharmProjects\pythonProject3\HAFTA3\online_retail_II.xlsx", sheet_name="Year 2010-2011")
df = data.copy()
df.head()
df.shape #(541910, 8)

#en çok sipariş edilen ürünlerin sıralaması
df.groupby("Description").agg({"Quantity": "sum"}).sort_values("Quantity", ascending=False).head()





