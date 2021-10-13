import uhal
import math
import numpy as np
import matplotlib.pyplot as plt
import csv

manager = uhal.ConnectionManager("file://arty7_connection.xml")
hw = manager.getDevice("arty7")

N = 512

list = []
for i in range(N):
	list.append( i*2 + 1 )

y_input = []
x = np.linspace(0, 6.28, N)

for i in x:
	y_input.append( int(100 + 100*np.sin(i)) )

plt.plot(x, y_input)
plt.show()

hw.getNode("data_input").writeBlock(y_input)

reading = hw.getNode("data_processed").readBlock(N)

hw.dispatch()

sine_filtered = reading.value()

with open("./sinewave.dat", "w") as f:
    for i in y_input:
       f.write(str(i)+"\n")
    for i in sine_filtered:
       f.write(str(i)+"\n")

plt.plot(x, y_input)
plt.plot(x, sine_filtered)
plt.show()





#Here triangular wave
x = np.linspace(0, 6, N)
y_input = []
for i in x:
        if ( i < 3):
	   y_input.append( int(100*i) )
        else:
	   y_input.append(  int(-100*i + 600) )

hw.getNode("data_input").writeBlock(y_input)
reading = hw.getNode("data_processed").readBlock(N)
hw.dispatch()

triangular_filtered = reading.value()

with open("./triangular.dat", "w") as f:
    for i in y_input:
       f.write(str(i)+"\n")
    for i in triangular_filtered:
       f.write(str(i)+"\n")

plt.plot(x, y_input)
plt.plot(x, triangular_filtered)
plt.show()





#Here square wave
x = np.linspace(0, 2, N)
y_input = []

for i in x:
        if ((i < 0.5)|(i > 1.5)):
	   y_input.append( 0 )
        else:
	   y_input.append( 100 )


hw.getNode("data_input").writeBlock(y_input)
reading = hw.getNode("data_processed").readBlock(N)
hw.dispatch()

square_filtered = reading.value()

with open("./square.dat", "w") as f:
    for i in y_input:
       f.write(str(i)+"\n")
    for i in square_filtered:
       f.write(str(i)+"\n")

plt.plot(x, y_input)
plt.plot(x, square_filtered)
plt.show()


#Here train of square waves
x = np.linspace(0, 50, N)
y_input = []

for i in x:
	if (i < 5):
		y_input.append( 0 )
        elif ((i <= 10)&(i > 5)):
		y_input.append( 10 )
        elif ((i <= 15)&(i > 10)):
		y_input.append( 0 )
        elif ((i <= 20)&(i > 15)):
		y_input.append( 10 )
        elif ((i <= 25)&(i > 20)):
	   y_input.append( 0 )
        elif ((i <= 30)&(i > 25)):
	   y_input.append( 10 )
        elif ((i <= 35)&(i > 30)):
	   y_input.append( 0 )
        elif ((i <= 40)&(i > 35)):
	   y_input.append( 10 )
        elif ((i <= 45)&(i > 40)):
	   y_input.append( 0 )
        elif ((i <= 50)&(i > 45)):
	   y_input.append( 10 )



hw.getNode("data_input").writeBlock(y_input)
reading = hw.getNode("data_processed").readBlock(N)
hw.dispatch()

squares_filtered = reading.value()

with open("./squares.dat", "w") as f:
    for i in y_input:
       f.write(str(i)+"\n")
    for i in squares_filtered:
       f.write(str(i)+"\n")

plt.plot(x, y_input)
plt.plot(x, squares_filtered)
plt.show()






