from tkinter import *
import numpy
import math

__version__ = '0.2.2'
__author__ = 'WangLvyuan'

class chart3d:
    
    fontSize1 = 12
    xx1 = 20
    yy1 = 20
    xx2 = 220
    yy2 = 220

    def fontSize(self, num):
         chart3d.fontSize1 = num
         return

    def x1(self, num):
         chart3d.xx1 = num
         return
    
    def x2(self, num):
         chart3d.xx2 = num
         return
    
    def y1(self, num):
         chart3d.yy1 = num
         return
    
    def y2(self, num):
         chart3d.yy2 = num
         return

# the pie apart
    def drawPie(self, pie_data_as_array, pie_lable_as_llist):
        rate = chart3d.pieData(pie_data_as_array)
        root = Tk()
        coord = chart3d.xx1, chart3d.yy1, chart3d.xx2, chart3d.yy2
        shadow = chart3d.xx1 + 10, chart3d.yy1 + 10, chart3d.xx2 + 10, chart3d.yy2 + 10
        center = chart3d.xx1 + 80, chart3d.yy1 + 80, chart3d.xx2 - 80, chart3d.yy2 - 80
        centerShadow = chart3d.xx1 + 90, chart3d.yy1 + 90, chart3d.xx2 - 70, chart3d.yy2 - 70
        cv = Canvas(root, bg='white')
        cv.pack(fill = 'both',expand ='yes')
    
        # the 3D shadow, will not move
        cv.create_oval(shadow, fill="white")

        #generate pie
        startPoint: float = 0
        for x,y in zip(rate, pie_lable_as_llist):
            degree: float = float('{:.2f}'.format(x*360))
            print(chart3d.locationCal(startPoint + degree/2)) 
            location = chart3d.locationCal(startPoint + degree/2)#data type: int in list
            cv.create_arc(coord, start=startPoint, extent=degree, fill="white")
            cv.create_text(location[0], location[1], text=str(round((x*100),1)) + '%')
            cv.create_text(location[2], location[3], text=y, font=("Arial", chart3d.fontSize1))
            location = []
            startPoint += degree
    
        #generate center hole
        cv.create_oval(center, fill="white")
        cv.create_arc(centerShadow, style="arc", start=71, extent=135)

        cv.pack()
        root.mainloop()

    def pieData(data2):
        rate = []
        s = sum(data2)
        for x in data2:
            rate.append('{:.4f}'.format(x/s))
        rate = numpy.array(rate, dtype = numpy.float64)
        return rate
    
    def locationCal(degree):
        rad = math.radians(degree)
        xLocation1 = round(round(math.cos(-rad),2) * (chart3d.xx2-chart3d.xx1)/4 + (chart3d.xx2+chart3d.xx1)/2)
        yLocation1 = round(round(math.sin(-rad),2) * (chart3d.xx2-chart3d.xx1)/4 + (chart3d.yy2+chart3d.yy1)/2)
        xLocation2 = round(round(math.cos(-rad),2) * (chart3d.xx2-chart3d.xx1)/2-10 + (chart3d.xx2+chart3d.xx1)/2)
        yLocation2 = round(round(math.sin(-rad),2) * (chart3d.xx2-chart3d.xx1)/2-10 + (chart3d.yy2+chart3d.yy1)/2)
        return [xLocation1, yLocation1, xLocation2, yLocation2]

def main():
     print('test main')
		
if __name__ == '__main__':
	main()
