import pypyodbc
import cv2
import base64
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

cap = cv2.VideoCapture(0)
ret, frame = cap.read()

# Resmi JPEG formatında bir stringe dönüştürme
if ret:
    _, buffer = cv2.imencode('.jpg', frame)
    jpg_as_text = base64.b64encode(buffer).decode()
    print("Resim Base64 formatında string ifadesi: ", jpg_as_text)
else:
    print("Resim çekilemedi.")

# Veritabanı bağlantısı
conn = pypyodbc.connect(
    'Driver={SQL Server};'
   'Server=DESKTOP-N8AOMNL;'
   'Database=FaceDedection;'
   'Trusted_Connection=yes;')

imlec = conn.cursor()


insert_query = "INSERT INTO Face_Images (Faceimages) VALUES (?)"
params = (jpg_as_text,)  # Parametreleri bir tuple içinde iletiyoruz


imlec.execute(insert_query, params)
imlec.commit()
imlec.execute('SELECT (Faceimages) FROM Face_Images')

rows = imlec.fetchall()
for row in rows:
    base64_data = row[0]  # Base64 kodunu al
    decoded_data = base64.b64decode(base64_data)
    image = Image.open(BytesIO(decoded_data))
    plt.imshow(image)
    plt.axis('off')  
    plt.show()

conn.close()
cap.release()



