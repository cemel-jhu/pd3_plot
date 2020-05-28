def cross(a, b):
    return [a[1]*b[2] - a[2]*b[1],a[2]*b[0] - a[0]*b[2],a[0]*b[1] - a[1]*b[0]]

target = open('frank_read.data', 'w')

target.truncate()

print "Writing to file ..."

Dimx=1.0*4.016e+3  #1x1x3 micron
Dimy=Dimx
Dimz=3*Dimx
rho=1.0e13         #dislocation density
rholength=Dimx*Dimy*Dimz*2.49*2.49e-20*rho #total dislocation length

from random import uniform, randint
lmin=800
lmax=2400
#random.randint(lmin/50,lmax/50)
#random.uniform(lmin,lmax)
l0=0.0
segnum=0
length=[]

while l0<rholength-lmax:
    length.append(uniform(lmin,lmax))
    l0=l0+length[segnum]    
    segnum=segnum+1
    

length.append(rholength-l0)
#x_ax=[-0.70710678118654746172,0.70710678118654746172,0.0000]
#y_ax=[0.40824829,0.40824829,-0.81649658]
#z_ax=[0.57735026918962584208,0.57735026918962584208,0.57735026918962584208]

x_ax=[1.0000,0.0000,0.0000]
y_ax=[0.0000,1.0000,0.0000]
z_ax=[0.0000,0.0000,1.0000]

b=[[-0.70710678118654746172, 0.70710678118654746172, 0.0000],[0.70710678118654746172, 0.70710678118654746172, 0.0000],[-0.70710678118654746172, 0.0000, 0.70710678118654746172],[0.70710678118654746172, 0.0000, 0.70710678118654746172],[0.0000, -0.70710678118654746172, 0.70710678118654746172],[0.0000, 0.70710678118654746172, 0.70710678118654746172]] # 6 Burgers vectors

n=[[0.57735026918962584208, 0.57735026918962584208, 0.57735026918962584208],[0.57735026918962584208, 0.57735026918962584208, -0.57735026918962584208],[0.57735026918962584208, -0.57735026918962584208, 0.57735026918962584208],[-0.57735026918962584208, 0.57735026918962584208, 0.57735026918962584208]] #4 slip normals

target.write("dataFileVersion =   5")
target.write("\n")
target.write("Dimensions = [")
target.write("\n")
target.write(str(Dimx))
target.write("\n")
target.write(str(Dimy))
target.write("\n")
target.write(str(Dimz))
target.write("\n")
target.write("]")
target.write("\n")
target.write("XAxis = [")
target.write("\n")
target.write(str(x_ax[0]))
target.write("\n")
target.write(str(x_ax[1]))
target.write("\n")
target.write(str(x_ax[2]))
target.write("\n")
target.write("]")
target.write("\n")
target.write("YAxis = [")
target.write("\n")
target.write(str(y_ax[0]))
target.write("\n")
target.write(str(y_ax[1]))
target.write("\n")
target.write(str(y_ax[2]))
target.write("\n")
target.write("]")
target.write("\n")


target.write("nodeCount = ")
target.write(str(2*segnum))
target.write("\n")
target.write("GeometryType =   1")
target.write("\n")
target.write("nodalData =")
target.write("\n")
target.write("#  Primary lines: node_tag, x, y, z, num_arms, constraint")
target.write("\n")
target.write("#  Secondary lines: arm_tag, burgx, burgy, burgz, nx, ny, nz")
target.write("\n")
 
from math import cos, sin, pi, sqrt
ll0=0
for num in range(0,segnum+1):     
#should be less than 1.000E+6 with current .ctrl file
    x0=uniform(-Dimx/2+length[num]/2,Dimx/2-length[num]/2)
    y0=uniform(-Dimy/2+length[num]/2,Dimy/2-length[num]/2)
    z0=uniform(-Dimz/2+length[num]/2,Dimz/2-length[num]/2)
    theta=uniform(0,2*pi)
    i=randint(0,5)
    if i == 0:
        j = randint(0,1)
    elif i == 1:
        j = 2+randint(0,1)
    elif i == 2:
        j = 2*randint(0,1)
    elif i == 3:
        j = 1+2*randint(0,1)        
    elif i == 4:
        j = 3*randint(0,1)
    elif i == 5:
        j = 1+randint(0,1)
    c=cross(b[i],n[j])

    x1=x0+length[num]*(cos(theta)*c[0]+sin(theta)*b[i][0])/2
    x2=x0-length[num]*(cos(theta)*c[0]+sin(theta)*b[i][0])/2
    y1=y0+length[num]*(cos(theta)*c[1]+sin(theta)*b[i][1])/2
    y2=y0-length[num]*(cos(theta)*c[1]+sin(theta)*b[i][1])/2
    z1=z0+length[num]*(cos(theta)*c[2]+sin(theta)*b[i][2])/2
    z2=z0-length[num]*(cos(theta)*c[2]+sin(theta)*b[i][2])/2
    ll0 = ll0 + sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2)+(z1-z2)*(z1-z2))
    target.write("0,")
    target.write(str(2*num).ljust(8))
    target.write(str())
    target.write("		")
    target.write(str(x1))
    target.write("		")
    target.write(str(y1))
    target.write("		")
    target.write(str(z1))
    target.write("		")
    target.write("1		7")
    target.write("\n")
    target.write("0.0000")
    target.write("      ")
    target.write("0.0000")
    target.write("      ")
    target.write("0.0000")
    target.write("\n")
    target.write("0,")
    target.write(str(2*num+1).ljust(8))
    target.write(str(b[i][0]))
    target.write("      ")
    target.write(str(b[i][1]))
    target.write("      ")
    target.write(str(b[i][2]))
    target.write("\n")
    target.write(str(n[j][0]))
    target.write("      ")
    target.write(str(n[j][1]))
    target.write("      ")
    target.write(str(n[j][2]))
    target.write("\n")
    target.write("0,")
    target.write(str(2*num+1).ljust(8))
    target.write(str())
    target.write("		")
    target.write(str(x2))
    target.write("		")
    target.write(str(y2))
    target.write("		")
    target.write(str(z2))
    target.write("		")
    target.write("1		7")
    target.write("\n")
    target.write("0.0000")
    target.write("      ")
    target.write("0.0000")
    target.write("      ")
    target.write("0.0000")
    target.write("\n")
    target.write("0,")
    target.write(str(2*num).ljust(8))
    target.write(str(-b[i][0]))
    target.write("      ")
    target.write(str(-b[i][1]))
    target.write("      ")
    target.write(str(-b[i][2]))
    target.write("\n")
    target.write(str(n[j][0]))
    target.write("      ")
    target.write(str(n[j][1]))
    target.write("      ")
    target.write(str(n[j][2]))
    target.write("\n")

print "Writing done."
print ll0, rholength
target.close()

target = open('geo.vtk', 'w')

target.truncate()

print "Writing to geometry file ..."

target.write("# vtk DataFile Version 3.0\n")
target.write("# Simulation cell (DXA version 1.3.0)\n")
target.write("ASCII\n")
target.write("DATASET STRUCTURED_GRID\n")
target.write("DIMENSIONS 2 2 2\n")
target.write("POINTS 8 float\n\n")
target.write(str(-Dimx/2*x_ax[0]-Dimy/2*y_ax[0]-Dimz/2*z_ax[0]).ljust(8))
target.write("		")
target.write(str(-Dimx/2*x_ax[1]-Dimy/2*y_ax[1]-Dimz/2*z_ax[1]).ljust(8))
target.write("		")
target.write(str(-Dimx/2*x_ax[2]-Dimy/2*y_ax[2]-Dimz/2*z_ax[2]).ljust(8))
target.write("\n")
target.write(str(+Dimx/2*x_ax[0]-Dimy/2*y_ax[0]-Dimz/2*z_ax[0]).ljust(8))
target.write("		")
target.write(str(+Dimx/2*x_ax[1]-Dimy/2*y_ax[1]-Dimz/2*z_ax[1]).ljust(8))
target.write("		")
target.write(str(+Dimx/2*x_ax[2]-Dimy/2*y_ax[2]-Dimz/2*z_ax[2]).ljust(8))
target.write("\n")
target.write(str(-Dimx/2*x_ax[0]+Dimy/2*y_ax[0]-Dimz/2*z_ax[0]).ljust(8))
target.write("		")
target.write(str(-Dimx/2*x_ax[1]+Dimy/2*y_ax[1]-Dimz/2*z_ax[1]).ljust(8))
target.write("		")
target.write(str(-Dimx/2*x_ax[2]+Dimy/2*y_ax[2]-Dimz/2*z_ax[2]).ljust(8))
target.write("\n")
target.write(str(+Dimx/2*x_ax[0]+Dimy/2*y_ax[0]-Dimz/2*z_ax[0]).ljust(8))
target.write("		")
target.write(str(+Dimx/2*x_ax[1]+Dimy/2*y_ax[1]-Dimz/2*z_ax[1]).ljust(8))
target.write("		")
target.write(str(+Dimx/2*x_ax[2]+Dimy/2*y_ax[2]-Dimz/2*z_ax[2]).ljust(8))
target.write("\n")
target.write(str(-Dimx/2*x_ax[0]-Dimy/2*y_ax[0]+Dimz/2*z_ax[0]).ljust(8))
target.write("		")
target.write(str(-Dimx/2*x_ax[1]-Dimy/2*y_ax[1]+Dimz/2*z_ax[1]).ljust(8))
target.write("		")
target.write(str(-Dimx/2*x_ax[2]-Dimy/2*y_ax[2]+Dimz/2*z_ax[2]).ljust(8))
target.write("\n")
target.write(str(Dimx/2*x_ax[0]-Dimy/2*y_ax[0]+Dimz/2*z_ax[0]).ljust(8))
target.write("		")
target.write(str(Dimx/2*x_ax[1]-Dimy/2*y_ax[1]+Dimz/2*z_ax[1]).ljust(8))
target.write("		")
target.write(str(Dimx/2*x_ax[2]-Dimy/2*y_ax[2]+Dimz/2*z_ax[2]).ljust(8))
target.write("\n")
target.write(str(-Dimx/2*x_ax[0]+Dimy/2*y_ax[0]+Dimz/2*z_ax[0]).ljust(8))
target.write("		")
target.write(str(-Dimx/2*x_ax[1]+Dimy/2*y_ax[1]+Dimz/2*z_ax[1]).ljust(8))
target.write("		")
target.write(str(-Dimx/2*x_ax[2]+Dimy/2*y_ax[2]+Dimz/2*z_ax[2]).ljust(8))
target.write("\n")
target.write(str(Dimx/2*x_ax[0]+Dimy/2*y_ax[0]+Dimz/2*z_ax[0]).ljust(8))
target.write("		")
target.write(str(Dimx/2*x_ax[1]+Dimy/2*y_ax[1]+Dimz/2*z_ax[1]).ljust(8))
target.write("		")
target.write(str(Dimx/2*x_ax[2]+Dimy/2*y_ax[2]+Dimz/2*z_ax[2]).ljust(8))
target.write("\n")
print "Writing done."
target.close()
