# -*- coding: utf-8 -*-
"""
Created on Sun Jun 26 05:34:56 2016

@author: lupur
"""

# STANJA:
# 0 - pocetno stanje
# 1 - biranje boja
# 11 - bela
# 12 - crvena
# 13 - zelena
# 14 - plava
# 15 - zuta
# 2 - crtanje
# 3 - biranje oblika
    # 31 - linija
    # 3 - krug 
    # 23 - pravougaonik
    # 24 - 
    # 25
def pocetnoStanje(brojPrstiju, stanje):
        if(brojPrstiju==1 ):
            stanje = 1     
        elif(brojPrstiju==2 ):
            stanje = 2    
        elif(brojPrstiju==3):
            stanje = 3                
        return stanje

def prvoStanje(brojPrstiju, boja, stanje) :
    
    if(brojPrstiju == 1) :
        boja = [255,255,255]
        print("BELA BOJA")
    elif(brojPrstiju==2) :
        print("CRVENA BOJA")
        boja = [0,0,255]
    elif (brojPrstiju==3) :
        boja = [0,255,0]
        print("ZELENA BOJA")
    elif (brojPrstiju==4) :
        boja = [255,0,0]
        print("PLAVA BOJA")
    elif (brojPrstiju==5) :
        boja = [0,255,255]
        print("ZUTA BOJA")
    else: 
        stanje = 0
        print("VRACANJE U STANJE 0")
    return stanje, boja
    

#ODABIR OBLIKA 
# 1 - LINIJA, 2- KVADRAT, 3-KRUG, 4- TROUGAO
def treceStanje(brojPrstiju, oblik, stanje, pun) :
    if(brojPrstiju==1):
        oblik = 1
        print("LINIJA")
    elif(brojPrstiju==2):
        oblik = 2
        print("KVADRAT")
    elif(brojPrstiju==3):
        oblik = 3
        print("KRUG")
    elif(brojPrstiju==4):
        pun = pun* -1
        if(pun<0):
            print("PUN")
        else:  
            print("PRAZAN")
    elif(brojPrstiju==5):
        stanje = 30
        print("POCINJEM CRTANJE OBJEKTA")
    else: 
        stanje = 0
        print("VRACANJE U STANJE 0")
    return stanje, oblik, pun
#def drugoStanje(trenutniBroj, )    
    
    