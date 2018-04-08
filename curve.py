import matplotlib.pyplot as plt
import numpy as np
import math
import numpy as np
from scipy.interpolate import interp1d
from matplotlib.offsetbox import AnchoredText

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

# define your values
Force = [0,4400,5670,6600,7040,8320,8800,9200,9240]
Elongation = [0,1,2,4,5,8,10,15,18]
GLength = 75
Radius = 6.65
LinearLimit = 1


#area calculation
Area = math.pi*Radius*Radius


#stress strain calculated as per above values
Stress = [ x*9.8/Area for x in Force ]
Strain = [ x/GLength for x  in Elongation ]

#True Stress calculation
Stress_True = [ x * (1+y) for y,x in zip(Strain,Stress)]
#True Strain calculation
Strain_True = [math.log(1+x) for x in Strain]


#values created which are needed for interpolation
Strain_values_linear = np.linspace(Strain[0], Strain[LinearLimit], num=41, endpoint=True)
Strain_values_eng = np.linspace(Strain[LinearLimit], Strain[-1], num=41, endpoint=True)
Strain_values_true = np.linspace(Strain_True[LinearLimit], Strain_True[-1], num=41, endpoint=True)

#interpolation defined
f1 = interp1d(Strain, Stress, fill_value='extrapolate')
f2 = interp1d(Strain, Stress, kind=3, fill_value='extrapolate')
f3 = interp1d(Strain_True, Stress_True, kind=3)

#plot
ax.plot(Strain,Stress, 'o')
ax.plot(Strain_values_linear, f1(Strain_values_linear),'b-')
ax.plot(Strain_values_eng, f2(Strain_values_eng),'g-')
ax.plot(Strain_values_true, f3(Strain_values_true),'r-')

#set label
ax.set_xlabel('Strain')
ax.set_ylabel('Stress  (MPa)')

#define ElasticLimit
ElasticLimit = Stress[LinearLimit] 
#define Modulus
Slope = Stress[LinearLimit]/Strain[LinearLimit]
Modulus = Slope/math.pow(10,3)
#define UTS
uts = max(Stress)
#define Failure Stress
failure_stress = max(Stress)

#plot UTS Line
plt.axhline(y=uts, ls=':', c='cyan')
#plot Ductility Line
plt.axvline(x=Strain[-1], ls=':', c='purple')

#plot offset Line
xA = [Strain[0],Strain[LinearLimit]]
yA = [Stress[0],Stress[LinearLimit]]
Strain_values_offset = [x +.002*Strain[-1] for x in xA]
f4 = interp1d(Strain_values_offset, yA, fill_value='extrapolate')
Strain_values_offset.append(Strain[LinearLimit+1])
ax.plot(Strain_values_offset,f4(Strain_values_offset),':',color='orange')


#find offset yield value              
val=Strain[LinearLimit]
step = (Strain[LinearLimit+1]-Strain[LinearLimit])/50
sign = f4(val)-f2(val)
while(1):
    if((f4(val)-f2(val))*sign < 0):
         break    
    val = val+ step
YieldPoint = f4(val-step)

#plot offset horizontal line
plt.axhline(y=YieldPoint, ls=':', c='black')


#plt legend
plt.legend(['Actual Values', 'Linear Region ', 'Engineering Stress Strain','True Stress Strain','UTS','Max Strain','Offset Line','Yield Point'], loc='best')
#add anchor
anchored_text = AnchoredText("Young's Modulus = " +"%.5f" % Modulus + " GPa\n" +
                             "Elastic Limit = " + "%.5f" % ElasticLimit + " MPa\n" +
                             "Yield Stress = "+ "%.5f" % YieldPoint + " MPa\n"+
                             "UTS = "+ "%.5f" % uts +" MPa\n"+
                             "Failure Stress = " + "%.5f" % failure_stress +" MPa\n"+
                             "Max Strain = "+ "%.5f" % Strain[8], loc='right')
ax.add_artist(anchored_text)

#set limits
ax.set_xlim(xmin=0)
ax.set_ylim(ymin=0)

#display graph
plt.show()

#print(Force)
#print(Elongation)
#print(Stress)
#print(Strain)
#print(Stress_True)
#print(Strain_True)
#print(Area)
#
