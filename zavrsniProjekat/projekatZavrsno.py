import cv2
import numpy as np
import math
import automat 


stanje = 0
cap = cv2.VideoCapture(0)
brojPonavljanja = 0
trenutniBroj = -1
pesnica = cv2.imread('pesnica.png',0)
kaziprst = cv2.imread('kaziprst.png',0)

granicaPonavljanja = 15

oblik = 0
#VELICINE LINIJE:
koorX1 = 20
koorY1 = 0

pun = 1
def promeniPun(pun):
    pun = -1 * pun



stanje0 = cv2.imread('stanje0.png', 0)
stanje2 = cv2.imread('stanje1.png', 0)
stanje1 = cv2.imread('stanje2.png', 0)
stanje4 = cv2.imread('stanje2.png', 0)
stanje3 = cv2.imread('stanje3.png', 0)
stanje30 = cv2.imread('stanje30.png', 0)

boja = [255,255,255]
bojaCrvena = [0, 0, 255]
bojaZelena = [0, 255, 0]
bojaPlava = [255, 0, 0]
bojaZuta = [255,0,255]

bojaPozadine = [255, 255, 255]

crtanje = np.zeros((300,300,3), np.uint8)


image, contours, hierarchy = cv2.findContours(pesnica.copy(), \
           cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

max_area = -1
for i in range(len(contours)):
    cnt=contours[i]
    area = cv2.contourArea(cnt)
    if(area>max_area):
        max_area=area
        ci=i
pesnica=contours[ci]
    
image, contours, hierarchy = cv2.findContours(kaziprst.copy(), \
           cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
           
max_area = -1
for i in range(len(contours)):
    cnt=contours[i]
    area = cv2.contourArea(cnt)
    if(area>max_area):
        max_area=area
        ci=i
kaziprst=contours[ci]


while(cap.isOpened()):
    
    #uzimanje slike sa kamere
    ret, img = cap.read()
    img = cv2.flip(img,1)
    #uokvirivanje regiona sa slike na kom ce se vrsiti prepoznavanje
    cv2.rectangle(img,(350,350),(50,50),(0,255,0),0)
    crop_img = img[50:350, 50:350]
    grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(grey, (35, 35), 0)
    
    #parametri cv2.threshold:
    # 1. fotografija koju obradjujemo, 2. prag thresholda, 
    # 3. vrednost koju dobija piksel ukoliko potpada u threshold
    # 4. stil tresholda 
                                  
    _, thresh1 = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

   
    image, contours, hierarchy = cv2.findContours(thresh1.copy(), \
           cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    #Trazimo najvecu konturu CNT
    max_area = -1
    for i in range(len(contours)):
        cnt=contours[i]
        area = cv2.contourArea(cnt)
        if(area>max_area):
            max_area=area
            ci=i
    cnt=contours[ci]

    #Uokvirimo najvecu konturu pravougaonikom
    x,y,w,h = cv2.boundingRect(cnt)
    cv2.rectangle(crop_img,(x,y),(x+w,y+h),(0,0,255),0)
    
    #hull aproksimira konturu u konveksan poligon    
    hull = cv2.convexHull(cnt)
    drawing = np.zeros(crop_img.shape,np.uint8)
    cv2.drawContours(drawing,[cnt],0,(0,255,0),0)
    cv2.drawContours(drawing,[hull],0,(0,0,255),0)
    
    #kada je parametar FALSE dobijamo temena HULL poligona
    hull = cv2.convexHull(cnt,returnPoints = False)
    
    #nadjemo defekte, tj delove na konturi koji su nekoveksni
    defects = cv2.convexityDefects(cnt,hull)
    count_defects = 0

    #moment slike daje informacije kao sto su centar mase, povrsina itd.
    moments = cv2.moments(cnt)
    #koordinate centra konture     
    centroid_x = int(moments['m10']/moments['m00'])
    centroid_y = int(moments['m01']/moments['m00'])
    cv2.circle(drawing,(centroid_x,centroid_y),2,[255,255,255],-1)    
    #cv2.drawContours(thresh1, contours, -1, (0,255,0), 3)
   
    for i in range(defects.shape[0]):
        
        #s-pocetak defekta
        #e-kraj defekta
        #f-najdalja tacka defekta
        #d-udaljenost izmedju f i konveksnog mnogougla
        s,e,f,d = defects[i,0]
        start = tuple(cnt[s][0])
        end = tuple(cnt[e][0])
        far = tuple(cnt[f][0])
        a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
        b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
        c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
        angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
        cv2.line(crop_img,start,end,[0,255,0],2)

        if angle <= 90:
             count_defects += 1
             cv2.circle(crop_img,far,5,[0,0,255],-1)
                 
        
        
    #SADA KADA SMO NASLI BROJ PRONADJENIH PRSTIJU SLEDI IMPLEMENTACIJA FUNKCIJA APLIKACIJE
        
        
    #PRVO NA OSNOVU BROJA DEFEKATA ODREDJUJEMO KOJI JE PRST PODIGNUT I KOLIKO DUGO JE ISTI PRST PODIGNUT
    if count_defects == 1:
        if( cv2.matchShapes(cnt,pesnica,1,0.0) < cv2.matchShapes(cnt,kaziprst,1,0.0)):
            if(trenutniBroj != 0):
                brojPonavljanja = 1
                trenutniBroj = 0
            else: brojPonavljanja = brojPonavljanja + 1
            cv2.putText(img,"0", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)

        else:
             if(trenutniBroj != count_defects):
                brojPonavljanja = 1
                trenutniBroj = count_defects
             else: brojPonavljanja = brojPonavljanja + 1
             cv2.putText(img,"1", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        
    elif count_defects == 2:
         if(trenutniBroj != count_defects):
            brojPonavljanja = 1
            trenutniBroj = count_defects
         else: brojPonavljanja = brojPonavljanja + 1
         cv2.putText(img, "2", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
    elif count_defects == 3:
         if(trenutniBroj != count_defects):
            brojPonavljanja = 1
            trenutniBroj = count_defects
         else: brojPonavljanja = brojPonavljanja + 1
         cv2.putText(img,"3", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
    elif count_defects == 4:
         if(trenutniBroj != count_defects):
            brojPonavljanja = 1
            trenutniBroj = count_defects
         else: brojPonavljanja = brojPonavljanja + 1        
         cv2.putText(img,"4", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
    
    else:
         if(trenutniBroj != count_defects):
            brojPonavljanja = 1
            trenutniBroj = count_defects
         else: brojPonavljanja = brojPonavljanja + 1
         cv2.putText(img,"5", (50,50),\
                    cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
 
    stanjeString = str(stanje)
    string = " STANJE: " + stanjeString
    cv2.putText(img,string, (150,150), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)


    #RAD SA AUTOMATOM STANJA

    if(brojPonavljanja == granicaPonavljanja and stanje == 0):
        if(trenutniBroj==4):
            cv2.imwrite( "sacuvanaSlika.jpg", crtanje );
            print("SLIKA SACUVANA")
        elif(trenutniBroj==5):
            break
        else:
            stanje = automat.pocetnoStanje(trenutniBroj, stanje)
            brojPonavljanja = 0
        

        
    if (stanje == 1 and brojPonavljanja == granicaPonavljanja):
        stanje, boja = automat.prvoStanje(trenutniBroj, boja, stanje)
        brojPonavljanja = 0
        
    if(stanje == 2 ):
        koorX = 1000
        koorY = 1000
        for i in range(x,x+w):
            #for j in range(y,y+h):
            pripada = cv2.pointPolygonTest(cnt, (i,y), False) 
            if (pripada==0):
            #if(koorY > j):
                koorX = i
                koorY = y
                break
        if(trenutniBroj==1):    
            print("CRTAM")
            cv2.circle(img, (koorX+50,koorY+50),5,boja,-1)
            cv2.circle(crtanje, (koorX,koorY),5, boja,-1)
        if(trenutniBroj==5 and brojPonavljanja==granicaPonavljanja):
             crtanje = np.zeros((300,300,3), np.uint8)
        if(trenutniBroj == 0 and brojPonavljanja == granicaPonavljanja):
             stanje = 0
             
             
             
    if(stanje == 3 and brojPonavljanja==granicaPonavljanja) :
        stanje, oblik, pun = automat.treceStanje(trenutniBroj, oblik, stanje,pun)
    
    kopijaDrawinga = crtanje.copy()

    if(stanje == 30):
        koorX = 1000
        koorY = 1000
        
        for i in range(x,x+w):
            #for j in range(y,y+h):
            pripada = cv2.pointPolygonTest(cnt, (i,y), False) 
            if (pripada==0):
            #if(koorY > j):
                koorX = i
                koorY = y
                break     
        if(trenutniBroj==0 and brojPonavljanja==granicaPonavljanja):
                stanje = 3
                brojPonavljanja=0
        if(trenutniBroj==2 and brojPonavljanja==granicaPonavljanja):
            crtanje = kopijaDrawinga
            stanje = 3
            brojPonavljanja=0
        elif(trenutniBroj==3):
            koorX1=koorX1+3
        elif(trenutniBroj==4):
            if(koorX1>5):
                koorX1 = koorX1-3
        if(oblik==1):
            cv2.line(img,(koorX+50,koorY+50),(50+koorX+koorX1,50+koorY+koorY1),boja,5)
            cv2.line(kopijaDrawinga,(koorX,koorY),(koorX+koorX1,koorY+koorY1),boja,5)
        if(oblik==2):
            cv2.rectangle(img,(koorX+50,koorY+50),(50+koorX+koorX1,50+koorY+koorX1),boja, pun*3)
            cv2.rectangle(kopijaDrawinga,(koorX,koorY),(koorX+koorX1,koorY+koorX1),boja,pun*3)
        if(oblik==3):
            cv2.circle(img,(koorX+50,koorY+50), koorX1, boja, pun*3)
            cv2.circle(kopijaDrawinga,(koorX,koorY),koorX1,boja,pun*3)

                    
    cv2.imshow('Original', img)
    all_img = np.hstack((drawing, crop_img))
    cv2.imshow('Konture', all_img)
    cv2.imshow('Thresholded', thresh1)

    if(stanje==30):
        cv2.imshow("CRTANJE", kopijaDrawinga)
        
    else:    
        cv2.imshow("CRTANJE", crtanje)
    
    


    if(stanje==0):
        cv2.imshow('STANJE', stanje0)
    elif(stanje==1):
        cv2.imshow('STANJE', stanje1)
    elif(stanje==2):
        cv2.imshow('STANJE', stanje2)
    elif(stanje==3):
        cv2.imshow('STANJE', stanje3)
    elif(stanje==4):
        cv2.imshow('STANJE', stanje4)
    elif(stanje==30):
        cv2.imshow('STANJE', stanje30)



           
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    

cap.release()
cv2.destroyAllWindows()













