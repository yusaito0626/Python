# -*- coding: utf-8 -*-
"""
Created on Sat Jun 25 11:07:12 2022

@author: yusai
"""



class Ring:
    def __init__(self,size=100):
        self.__arr = []
        self.__size = size
        self.__idx = -1
        self.__currentSz = 0
        
    def add(self,item):
        self.__idx += 1
        if(self.__idx == self.__size):
            self.__idx = 0
        if(self.__currentSz < self.__size):
            self.__arr.append(item)
            self.__currentSz += 1
        else:
            self.__arr[self.__idx] = item
                
        
    def relative(self,i):
        idx = self.__idx + i
        if(idx >= self.__currentSz):
            idx -= self.__currentSz
        elif(idx < 0):
            idx += self.__currentSz
            if(idx > self.__currentSz):
                return None
        if(idx >= self.__currentSz or idx < 0):
            return None
        else:
            return self.__arr[idx]
    def peek(self):
        return self.__arr[self.__idx]
    
    def item(self,i):
        if(i >= self.__currentSz or i < 0):
            return None
        else:
            return self.__arr[i]
    def items(self):
        return self.__arr
        
    def getSz(self):
        return self.__size
    
    def getCurrentSz(self):
        return self.__currentSz
    
    def current(self):
        return self.__idx