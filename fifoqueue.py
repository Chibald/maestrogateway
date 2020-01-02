class PileFifo(object):
    def __init__(self,maxpile=None):
        self.pile=[]
        self.maxpile = maxpile

    def empile(self,element,idx=0):
        if (self.maxpile!=None) and (len(self.pile)==self.maxpile):
            raise ValueError ("erreur: tentative d'empiler dans une pile pleine")
        self.pile.insert(idx,element)
 
    def depile(self,idx=-1):
        if len(self.pile)==0:
            raise ValueError ("erreur: tentative de depiler une pile vide")
        if idx<-len(self.pile) or idx>=len(self.pile):
            raise ValueError ("erreur: element de pile à depiler n'existe pas")
        return self.pile.pop(idx)
 
    def element(self,idx=-1):
        if idx<-len(self.pile) or idx>=len(self.pile):
            raise ValueError ("erreur: element de pile à lire n'existe pas")
        return self.pile[idx]
 
    def copiepile(self,imin=0,imax=None):
        if imax==None:
            imax=len(self.pile)
        if imin<0 or imax>len(self.pile) or imin>=imax:
            raise ValueError ("erreur: mauvais indice(s) pour l'extraction par copiepile")
        return list(self.pile[imin:imax])
 
    def pilevide(self):
        return len(self.pile)==0
 
    def pilepleine(self):
        return self.maxpile!=None and len(self.pile)==self.maxpile
 
    def taille(self):
        return len(self.pile)