from tkinter import *
import numpy
import math

__version__ = '0.2.1'
__author__ = 'WangLvyuan'

class chart3d:
    fontSize = 12
    x1 = 20
    y1 = 20
    x2 = 220
    y2 = 220

    def fontSize(self, num):
         chart3d.fontSize = num
         return

    def x1(self, num):
         chart3d.x1 = num
         return
    
    def x2(self, num):
         chart3d.x2 = num
         return
    
    def y1(self, num):
         chart3d.y1 = num
         return
    
    def y2(self, num):
         chart3d.y2 = num
         return

    def pieData(data2):
        rate = []
        s = sum(data2)
        for x in data2:
            rate.append('{:.4f}'.format(x/s))
        rate = numpy.array(rate, dtype = numpy.float64)
        return rate
    
    def locationCal(degree):
        rad = math.radians(degree)
        xLocation1 = round(round(math.cos(-rad),2) * (chart3d.x2-chart3d.x1)/4 + (chart3d.x2+chart3d.x1)/2)
        yLocation1 = round(round(math.sin(-rad),2) * (chart3d.x2-chart3d.x1)/4 + (chart3d.y2+chart3d.y1)/2)
        xLocation2 = round(round(math.cos(-rad),2) * (chart3d.x2-chart3d.x1)/2-10 + (chart3d.x2+chart3d.x1)/2)
        yLocation2 = round(round(math.sin(-rad),2) * (chart3d.x2-chart3d.x1)/2-10 + (chart3d.y2+chart3d.y1)/2)
        return [xLocation1, yLocation1, xLocation2, yLocation2]
    
    # the pie apart
    def drawPie(self, pie_data_as_array, pie_lable_as_llist):
        rate = chart3d.pieData(pie_data_as_array)
        root = Tk()
        coord = chart3d.x1, chart3d.y1, chart3d.x2, chart3d.y2
        shadow = chart3d.x1 + 10, chart3d.y1 + 10, chart3d.x2 + 10, chart3d.y2 + 10
        center = chart3d.x1 + 80, chart3d.y1 + 80, chart3d.x2 - 80, chart3d.y2 - 80
        centerShadow = chart3d.x1 + 90, chart3d.y1 + 90, chart3d.x2 - 70, chart3d.y2 - 70
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
            cv.create_text(location[2], location[3], text=y, font=("Arial", chart3d.fontSize))
            location = []
            startPoint += degree
    
        #generate center hole
        cv.create_oval(center, fill="white")
        cv.create_arc(centerShadow, style="arc", start=71, extent=135)
    
        #generate label
        # for x in label:
             

        cv.pack()
        root.mainloop()

def main():
     print('test main')
		
if __name__ == '__main__':
	main()
