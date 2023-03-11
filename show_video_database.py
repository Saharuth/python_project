import mysql.connector
import cv2
import numpy as np
import base64

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="347+445+b",
  database="test"
)

resolution = {
    "96X96" : [96,96],
    "QQVGA" : [160,120],
    "QCIF"  : [176,144],
    "HQVGA" : [240,176],
    "240x240"   : [240,240],
    "QVGA"  : [320,240],
    "CIF"   : [400,296],
    "HVGA"  : [480,320],
    "VGA"   : [640,480],
    "SVGA"  : [800,600],
    "XGA"   : [1024,768],
    "HD"    : [1280,720],
    "SXGA"  : [1280,1024],
    "UXGA"  : [1600,1200],
    "FHD"   : [1920,1080],
    "P_HD"  : [720,1280],
    "P_3MP" : [864,1536],
    "QXGA"  : [2048,1536],
    "QHD"   : [2560,1440],
    "WQXGA" : [2560,1600],
    "P_FHD" : [1080,1920],
    "QSXGA" : [2560,1920]
}

mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM picturedata")
myresult = mycursor.fetchall()

res = myresult[0][4]
xy = resolution[res]
cam = myresult[0][5]
seq_pic = 0
picture_show = ""

def aggregation(db, node):
    global seq_pic
    cursor = db.cursor()
    cursor.execute("SELECT * FROM picturedata")
    data = cursor.fetchall()
    data_total = ""
    # sql = "UPDATE picturedata SET number = 'END' WHERE id = '"+ data[0][3] + "'" 
    # cursor.execute(sql)
    # db.commit()
    idpic = int(data[seq_pic][6])
    total_pkt = int(data[seq_pic][3])
    count = 0
    for x in range(total_pkt):
        if int(data[x+seq_pic][6]) == idpic:
            data_total = data_total + data[x+seq_pic][2]
            count = count + 1
    # seq_pic = seq_pic + total_pkt
    if (idpic+1)%30 == 0 or idpic == 255:
        seq_pic = 0
    if count == total_pkt:
        seq_pic = seq_pic + total_pkt
        return data_total
    else:
        return "0"

while(True):
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="347+445+b",
            database="test"
        )

        picture = aggregation(mydb, 1)
        if picture != "0":
            picture_show = picture

        picdecode = base64.standard_b64decode(picture_show)
        img = np.frombuffer(picdecode, dtype=np.uint8)
        frame = cv2.imdecode(img, flags=cv2.IMREAD_COLOR)

        # Display the resulting frame   
        cv2.imshow('frame',frame)
        # Press Q on keyboard to stop recording
        if cv2.waitKey(500) & 0xFF == ord('q'):
            break
    except Exception as e:
        print(e)
    # Break the loop 

cv2.destroyAllWindows()
