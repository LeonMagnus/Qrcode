import zbar
from threading import Thread
from PIL import Image
import cv2
import numpy
import requests


class post2(Thread):
    def __init__(self,datas):
        Thread.__init__(self)
        self.data=datas
    def run(self):
        URL="http://192.168.200.112:5000/upd"
        #URL="http://127.0.0.1:8080/upd" 
        try:
            req=requests.post(URL,self.data)
        except Exception as e:
            print "rro" 
        #print req.status_code

class images(Thread):
    def __init__(self,image,ok):
        Thread.__init__(self)
        self.image = image
        self.ok=ok

    def run(self):
        for decoded in self.image:
            if self.ok :
                self.ok=False
                data = decoded.data.split(' ')
                datas={'fname':data[0], 'lname':data[1]}
                thread=post2(datas)
                thread.start()
                thread.join()
                print(data[0])
                print(data[1])


def main():


    aff=0
    ok=False
   #choisir ta cam pour filme
    capture = cv2.VideoCapture(0)

    while True:
        # pour quite le porgramme apuis sur q
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # metre limage de la video sur frame
        ret, frame = capture.read()


        # couvrire limage au grayscale.
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Uses PIL to convert the grayscale image into a ndary array that ZBar can understand.
        image = Image.fromarray(gray)
        width, height = image.size
        zbar_image = zbar.Image(width, height, 'Y800', image.tobytes())

        #scanner le zbar image
        scanner = zbar.ImageScanner()
        n=scanner.scan(zbar_image)

        if n>aff:
            aff+=1
            ok=True
        elif n<aff:
            aff-=1
        # scan le qr code (afiche la couleur ver sur les alentoure du qr code)
        for decoded in zbar_image:
            #desin le rectoncle pour affiche le dessin
            p = numpy.array(decoded.location)
            cv2.line(frame,(p[0][0],p[0][1]),(p[1][0],p[1][1]),(0, 255, 0), 2, 8, 0)
            cv2.line(frame,(p[1][0],p[1][1]),(p[2][0],p[2][1]),(0, 255, 0), 2, 8, 0)
            cv2.line(frame,(p[2][0],p[2][1]),(p[3][0],p[3][1]),(0, 255, 0), 2, 8, 0)
            cv2.line(frame,(p[3][0],p[3][1]),(p[0][0],p[0][1]),(0, 255, 0), 2, 8, 0)

        #envoie le ficher au serveur avec le threds + print sur la console
        if ok :
            thread2=images(zbar_image,ok)
            thread2.start()
            thread2.join()
            ok=False
      #for decoded in zbar_image:
          #  if ok :
           #     ok=False
            #    data = decoded.data.split(' ')
             #   datas={'fname':data[0], 'lname':data[1]}
              #  thread=post2(datas)
               # thread.start()
             #   thread.join()
              #  print(data[0])
               # print(data[1])
        # affiche la video on coure
        cv2.imshow('Current', frame)

if __name__ == "__main__":
    main()
