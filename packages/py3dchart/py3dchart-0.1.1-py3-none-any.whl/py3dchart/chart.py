from tkinter import *
import numpy

__version__ = '0.1.1'
__author__ = 'WangLvyuan'

class threeDChart:

    def pieData(data2):
        rate = []
        s = sum(data2)
        for x in data2:
            rate.append('{:.4f}'.format(x/s))
        rate = numpy.array(rate, dtype = numpy.float64)
        return rate
    
    # the pie apart
    def pieGernerate(self, pie_data_as_array):
        rate = threeDChart.pieData(pie_data_as_array)
        root = Tk()
        coord = 20, 20, 220, 220
        shadow = 30, 30, 230, 230
        center = 100, 100, 140, 140
        centerShadow = 110, 110, 150, 150
        cv = Canvas(root, bg='white')
    
        # the 3D shadow, will not move
        cv.create_oval(shadow, fill="white")
        startPoint: float = 0
        for x in rate:
            degree: float = float('{:.2f}'.format(x*360))
            cv.create_arc(coord, start=startPoint, extent=degree, fill="white")
            startPoint += degree
    
        cv.create_oval(center, fill="white")
        cv.create_arc(centerShadow, style="arc", start=71, extent=135)
    
        cv.pack()
        root.mainloop()
		
if __name__ == '__main__':
	print("hello")