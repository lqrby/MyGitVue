'''
version: V2.0
Author: 学海无涯任我游
Date: 2020-12-25 16:36:28
LastEditors: 学海无涯任我游
LastEditTime: 2020-12-25 16:39:47
'''
#  -*- coding:utf-8 -*-

import turtle
q = turtle.Pen()
turtle.bgcolor("black")
sides = 7
colors =["red","orange","yellow","green","cyan","blue","blue","purple"]
for x in range(360):
    q.pencolor(colors[x%sides])
    q.forward(x*3/sides+x)
    q.left(360/sides+1)
    q.width(x*sides/200)