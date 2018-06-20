import zbar

from PIL import Image
import cv2
import numpy
import requests

def main():
    aff=0
    ok=False
    URL="http://192.168.200.112:5000/upd"
    def post(fname, lname):
        data={'fname':fname, 'lname': lname}
        req=requests.post(URL,data)
       # print req.status_code
   #choisir la cam avec la quelle filme
    capture = cv2.VideoCapture(0)

    while True:
        # quite le programme avec q.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Breaks down the video into frames
        ret, frame = capture.read()


        # Converts image to grayscale.
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Uses PIL to convert the grayscale image into a ndary array that ZBar can understand.
        image = Image.fromarray(gray)
        width, height = image.size
        zbar_image = zbar.Image(width, height, 'Y800', image.tobytes())

        # Scans the zbar image.
        scanner = zbar.ImageScanner()
        n=scanner.scan(zbar_image)

        if n>aff:
            aff+=1
            ok=True
        elif n<aff:
            aff-=1
        # Prints data from image.
        for decoded in zbar_image:
            #desin le rectoncle pour affiche le dessin
            p = numpy.array(decoded.location)
            cv2.line(frame,(p[0][0],p[0][1]),(p[1][0],p[1][1]),(0, 255, 0), 2, 8, 0)
            cv2.line(frame,(p[1][0],p[1][1]),(p[2][0],p[2][1]),(0, 255, 0), 2, 8, 0)
            cv2.line(frame,(p[2][0],p[2][1]),(p[3][0],p[3][1]),(0, 255, 0), 2, 8, 0)
            cv2.line(frame,(p[3][0],p[3][1]),(p[0][0],p[0][1]),(0, 255, 0), 2, 8, 0)


        for decoded in zbar_image:
            if ok :
                ok=False
                data = decoded.data.split(' ')
                post(data[0],data[1])
                print(data[0])
                print(data[1])
        
        # Displays the current frame
        cv2.imshow('Current', frame)

if __name__ == "__main__":
    main()
