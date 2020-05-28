def cross(a, b):
    return [a[1]*b[2] - a[2]*b[1],a[2]*b[0] - a[0]*b[2],a[0]*b[1] - a[1]*b[0]]
def num_vec_prod(a,b,c,x,y,z):
    return [a*x[0]+b*x[1]+c*x[2],a*y[0]+b*y[1]+c*y[2],a*z[0]+b*z[1]+c*z[2]]

from numpy import linalg as LA

target = open('frank_read.data', 'w')

target.truncate()

print "Writing to file ..."

Lx=.7*4.016e+3
Ly=.7*4.016e+3
Lz=1*4.016e+3
Lwall=0.2*4.016e+3
Dimx=Lx  #4x3x3 micron
Dimy=Ly
Dimz=Lz
rholength_wall=(Lx*Ly-(Lx-Lwall)*(Ly-Lwall))*Lz*2.49*2.49e-20*1e+15
rholength_interior=(Dimx*Dimy-Lx*Ly+(Lx-Lwall)*(Ly-Lwall))*Lz*2.49*2.49e-20*4.0e+13
     
from random import uniform, randint
lmin=800
lmax=1500
lmin_fr=3500
lmax_fr=4500
#random.randint(lmin/50,lmax/50)
#random.uniform(lmin,lmax)
l0=0.0
segnum=0
length_interior_short=[]
length_interior_long=[]

while l0<rholength_interior*.5-lmax-lmin:
    length_interior_short.append(uniform(lmin,lmax))
    l0=l0+length_interior_short[segnum]
    length_interior_long.append(uniform(lmin,lmax))
    l0=l0+length_interior_long[segnum]
    segnum=segnum+1

length_interior_short.append(.5*(rholength_interior*.5-l0))
length_interior_long.append(.5*(rholength_interior*.5-l0))

l0=0.0
segnum_fr=0
length_fr=[]
while l0<rholength_interior-lmax_fr:
    length_fr.append(uniform(lmin_fr,lmax_fr))
    l0=l0+length_fr[segnum_fr]    
    segnum_fr=segnum_fr+1

length_fr.append(rholength_interior-l0)

lmin_long=650
lmax_long=800
lmin_short=300
lmax_short=400
#random.randint(lmin/50,lmax/50)
#random.uniform(lmin,lmax)
l0=0.0
segnum_wall=0
length_wall_long=[]
length_wall_short=[]

while l0<rholength_wall*.5-lmax_long-lmax_short:
    length_wall_short.append(uniform(lmin_short,lmax_short))
    l0=l0+length_wall_short[segnum_wall]
    length_wall_long.append(length_wall_short[segnum_wall]*uniform(1,3))
    l0=l0+length_wall_long[segnum_wall]
    segnum_wall=segnum_wall+1

length_wall_short.append((rholength_wall*0.5-l0)*lmax_short/(lmax_short+lmax_long))
length_wall_long.append((rholength_wall*0.5-l0)*lmax_long/(lmax_short+lmax_long))

#x_ax=[0.70710678118654746172,-0.70710678118654746172,0.0000]
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
target.write(str(4*segnum+4*segnum_wall+8+3*segnum_fr))
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
    x0=uniform(-Dimx/2,Dimx/2)
    y0=uniform(-Dimy/2,Dimy/2)
    z0=uniform(-Dimz/2,Dimz/2)

    theta=uniform(0,2*pi)
    i=randint(0,5)
    if i == 0:
        j = randint(0,1)
        j1 = 1-j
    elif i == 1:
        j = 2+randint(0,1)
        j1 = 5-j
    elif i == 2:
        j = 2*randint(0,1)
        j1 = 2-j
    elif i == 3:
        j = 1+2*randint(0,1)
        j1 = 4-j
    elif i == 4:
        j = 3*randint(0,1)
        j1 = 3-j
    elif i == 5:
        j = 1+randint(0,1)
        j1 = 3-j

    c0=cross(b[i],n[j])
    c=c0/LA.norm(c0)
    c0=cross(b[i],n[j1])
    c1=c0/LA.norm(c0)
    
    x1=x0*x_ax[0]+y0*y_ax[0]+z0*z_ax[0]+length_interior_short[num]/2*(c[0]*cos(theta)+b[i][0]*sin(theta))-length_interior_long[num]/2*(c1[0]*cos(theta)+b[i][0]*sin(theta))
    x2=x0*x_ax[0]+y0*y_ax[0]+z0*z_ax[0]-length_interior_short[num]/2*(c[0]*cos(theta)+b[i][0]*sin(theta))-length_interior_long[num]/2*(c1[0]*cos(theta)+b[i][0]*sin(theta))
    y1=x0*x_ax[1]+y0*y_ax[1]+z0*z_ax[1]+length_interior_short[num]/2*(c[1]*cos(theta)+b[i][1]*sin(theta))-length_interior_long[num]/2*(c1[1]*cos(theta)+b[i][1]*sin(theta))
    y2=x0*x_ax[1]+y0*y_ax[1]+z0*z_ax[1]-length_interior_short[num]/2*(c[1]*cos(theta)+b[i][1]*sin(theta))-length_interior_long[num]/2*(c1[1]*cos(theta)+b[i][1]*sin(theta))
    z1=x0*x_ax[2]+y0*y_ax[2]+z0*z_ax[2]+length_interior_short[num]/2*(c[2]*cos(theta)+b[i][2]*sin(theta))-length_interior_long[num]/2*(c1[2]*cos(theta)+b[i][2]*sin(theta))
    z2=x0*x_ax[2]+y0*y_ax[2]+z0*z_ax[2]-length_interior_short[num]/2*(c[2]*cos(theta)+b[i][2]*sin(theta))-length_interior_long[num]/2*(c1[2]*cos(theta)+b[i][2]*sin(theta))

    x3=x0*x_ax[0]+y0*y_ax[0]+z0*z_ax[0]+length_interior_short[num]/2*(c[0]*cos(theta)+b[i][0]*sin(theta))+length_interior_long[num]/2*(c1[0]*cos(theta)+b[i][0]*sin(theta))
    x4=x0*x_ax[0]+y0*y_ax[0]+z0*z_ax[0]-length_interior_short[num]/2*(c[0]*cos(theta)+b[i][0]*sin(theta))+length_interior_long[num]/2*(c1[0]*cos(theta)+b[i][0]*sin(theta))
    y3=x0*x_ax[1]+y0*y_ax[1]+z0*z_ax[1]+length_interior_short[num]/2*(c[1]*cos(theta)+b[i][1]*sin(theta))+length_interior_long[num]/2*(c1[1]*cos(theta)+b[i][1]*sin(theta))
    y4=x0*x_ax[1]+y0*y_ax[1]+z0*z_ax[1]-length_interior_short[num]/2*(c[1]*cos(theta)+b[i][1]*sin(theta))+length_interior_long[num]/2*(c1[1]*cos(theta)+b[i][1]*sin(theta))
    z3=x0*x_ax[2]+y0*y_ax[2]+z0*z_ax[2]+length_interior_short[num]/2*(c[2]*cos(theta)+b[i][2]*sin(theta))+length_interior_long[num]/2*(c1[2]*cos(theta)+b[i][2]*sin(theta))
    z4=x0*x_ax[2]+y0*y_ax[2]+z0*z_ax[2]-length_interior_short[num]/2*(c[2]*cos(theta)+b[i][2]*sin(theta))+length_interior_long[num]/2*(c1[2]*cos(theta)+b[i][2]*sin(theta))

    ll0 = ll0 + 2*sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2)+(z1-z2)*(z1-z2))+2*sqrt((x1-x3)*(x1-x3)+(y1-y3)*(y1-y3)+(z1-z3)*(z1-z3))
    local_1 = num_vec_prod(x1,y1,z1,x_ax,y_ax,z_ax)
    local_2 = num_vec_prod(x2,y2,z2,x_ax,y_ax,z_ax)
    local_3 = num_vec_prod(x3,y3,z3,x_ax,y_ax,z_ax)
    local_4 = num_vec_prod(x4,y4,z4,x_ax,y_ax,z_ax)

    if min(local_1[0],local_2[0],local_3[0],local_4[0]) < -Dimx/2:
        dx=-Dimx/2-min(local_1[0],local_2[0],local_3[0],local_4[0])
        x0=x0+1.01*dx
    elif max(local_1[0],local_2[0],local_3[0],local_4[0]) > Dimx/2:
        dx=max(local_1[0],local_2[0],local_3[0],local_4[0])-Dimx/2
        x0=x0-1.01*dx
    if min(local_1[1],local_2[1],local_3[1],local_4[1]) < -Dimy/2:
        dy=-Dimy/2-min(local_1[1],local_2[1],local_3[1],local_4[1])
        y0=y0+1.01*dy
    elif max(local_1[1],local_2[1],local_3[1],local_4[1]) > Dimy/2:
        dy=max(local_1[1],local_2[1],local_3[1],local_4[1])-Dimy/2
        y0=y0-1.01*dy
    if min(local_1[2],local_2[2],local_3[2],local_4[2]) < -Dimz/2:
        dz=-Dimz/2-min(local_1[2],local_2[2],local_3[2],local_4[2])
        z0=z0+1.01*dz
    elif max(local_1[2],local_2[2],local_3[2],local_4[2]) > Dimz/2:
        dz=max(local_1[2],local_2[2],local_3[2],local_4[2])-Dimz/2
        z0=z0-1.01*dz

    x1=x0*x_ax[0]+y0*y_ax[0]+z0*z_ax[0]+length_interior_short[num]/2*(c[0]*cos(theta)+b[i][0]*sin(theta))-length_interior_long[num]/2*(c1[0]*cos(theta)+b[i][0]*sin(theta))
    x2=x0*x_ax[0]+y0*y_ax[0]+z0*z_ax[0]-length_interior_short[num]/2*(c[0]*cos(theta)+b[i][0]*sin(theta))-length_interior_long[num]/2*(c1[0]*cos(theta)+b[i][0]*sin(theta))
    y1=x0*x_ax[1]+y0*y_ax[1]+z0*z_ax[1]+length_interior_short[num]/2*(c[1]*cos(theta)+b[i][1]*sin(theta))-length_interior_long[num]/2*(c1[1]*cos(theta)+b[i][1]*sin(theta))
    y2=x0*x_ax[1]+y0*y_ax[1]+z0*z_ax[1]-length_interior_short[num]/2*(c[1]*cos(theta)+b[i][1]*sin(theta))-length_interior_long[num]/2*(c1[1]*cos(theta)+b[i][1]*sin(theta))
    z1=x0*x_ax[2]+y0*y_ax[2]+z0*z_ax[2]+length_interior_short[num]/2*(c[2]*cos(theta)+b[i][2]*sin(theta))-length_interior_long[num]/2*(c1[2]*cos(theta)+b[i][2]*sin(theta))
    z2=x0*x_ax[2]+y0*y_ax[2]+z0*z_ax[2]-length_interior_short[num]/2*(c[2]*cos(theta)+b[i][2]*sin(theta))-length_interior_long[num]/2*(c1[2]*cos(theta)+b[i][2]*sin(theta))

    x3=x0*x_ax[0]+y0*y_ax[0]+z0*z_ax[0]+length_interior_short[num]/2*(c[0]*cos(theta)+b[i][0]*sin(theta))+length_interior_long[num]/2*(c1[0]*cos(theta)+b[i][0]*sin(theta))
    x4=x0*x_ax[0]+y0*y_ax[0]+z0*z_ax[0]-length_interior_short[num]/2*(c[0]*cos(theta)+b[i][0]*sin(theta))+length_interior_long[num]/2*(c1[0]*cos(theta)+b[i][0]*sin(theta))
    y3=x0*x_ax[1]+y0*y_ax[1]+z0*z_ax[1]+length_interior_short[num]/2*(c[1]*cos(theta)+b[i][1]*sin(theta))+length_interior_long[num]/2*(c1[1]*cos(theta)+b[i][1]*sin(theta))
    y4=x0*x_ax[1]+y0*y_ax[1]+z0*z_ax[1]-length_interior_short[num]/2*(c[1]*cos(theta)+b[i][1]*sin(theta))+length_interior_long[num]/2*(c1[1]*cos(theta)+b[i][1]*sin(theta))
    z3=x0*x_ax[2]+y0*y_ax[2]+z0*z_ax[2]+length_interior_short[num]/2*(c[2]*cos(theta)+b[i][2]*sin(theta))+length_interior_long[num]/2*(c1[2]*cos(theta)+b[i][2]*sin(theta))
    z4=x0*x_ax[2]+y0*y_ax[2]+z0*z_ax[2]-length_interior_short[num]/2*(c[2]*cos(theta)+b[i][2]*sin(theta))+length_interior_long[num]/2*(c1[2]*cos(theta)+b[i][2]*sin(theta))
    
    target.write("0,")
    target.write(str(4*num).ljust(8)) #1
    target.write(str())
    target.write("		")
    target.write(str(x1))
    target.write("		")
    target.write(str(y1))
    target.write("		")
    target.write(str(z1))
    target.write("		")
    target.write("2		0")
    target.write("\n")
    target.write("0.0000")
    target.write("      ")
    target.write("0.0000")
    target.write("      ")
    target.write("0.0000")
    target.write("\n")
    target.write("0,")
    target.write(str(4*num+1).ljust(8)) #2
    target.write(str(b[i][0]))
    target.write("      ")
    target.write(str(b[i][1]))
    target.write("      ")
    target.write(str(b[i][2]))
    target.write("\n")
    target.write(str(n[j1][0]))
    target.write("      ")
    target.write(str(n[j1][1]))
    target.write("      ")
    target.write(str(n[j1][2]))
    target.write("\n")
    target.write("0,")
    target.write(str(4*num+2).ljust(8)) #3
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

    target.write("0,")
    target.write(str(4*num+1).ljust(8)) #2
    target.write(str())
    target.write("		")
    target.write(str(x2))
    target.write("		")
    target.write(str(y2))
    target.write("		")
    target.write(str(z2))
    target.write("		")
    target.write("2		0")
    target.write("\n")
    target.write("0.0000")
    target.write("      ")
    target.write("0.0000")
    target.write("      ")
    target.write("0.0000")
    target.write("\n")
    target.write("0,")
    target.write(str(4*num+3).ljust(8))     #4
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
    target.write(str(4*num).ljust(8))  #1
    target.write(str(-b[i][0]))
    target.write("      ")
    target.write(str(-b[i][1]))
    target.write("      ")
    target.write(str(-b[i][2]))
    target.write("\n")
    target.write(str(n[j1][0]))
    target.write("      ")
    target.write(str(n[j1][1]))
    target.write("      ")
    target.write(str(n[j1][2]))
    target.write("\n")

    target.write("0,")
    target.write(str(4*num+2).ljust(8))  #3
    target.write(str())
    target.write("		")
    target.write(str(x3))
    target.write("		")
    target.write(str(y3))
    target.write("		")
    target.write(str(z3))
    target.write("		")
    target.write("2		0")
    target.write("\n")
    target.write("0.0000")
    target.write("      ")
    target.write("0.0000")
    target.write("      ")
    target.write("0.0000")
    target.write("\n")
    target.write("0,")
    target.write(str(4*num).ljust(8))  #1
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
    target.write(str(4*num+3).ljust(8))  #4
    target.write(str(-b[i][0]))
    target.write("      ")
    target.write(str(-b[i][1]))
    target.write("      ")
    target.write(str(-b[i][2]))
    target.write("\n")
    target.write(str(n[j1][0]))
    target.write("      ")
    target.write(str(n[j1][1]))
    target.write("      ")
    target.write(str(n[j1][2]))
    target.write("\n")

    target.write("0,")
    target.write(str(4*num+3).ljust(8))
    target.write(str())
    target.write("		")
    target.write(str(x4))
    target.write("		")
    target.write(str(y4))
    target.write("		")
    target.write(str(z4))
    target.write("		")
    target.write("2		0")
    target.write("\n")
    target.write("0.0000")
    target.write("      ")
    target.write("0.0000")
    target.write("      ")
    target.write("0.0000")
    target.write("\n")
    target.write("0,")
    target.write(str(4*num+2).ljust(8))
    target.write(str(b[i][0]))
    target.write("      ")
    target.write(str(b[i][1]))
    target.write("      ")
    target.write(str(b[i][2]))
    target.write("\n")
    target.write(str(n[j1][0]))
    target.write("      ")
    target.write(str(n[j1][1]))
    target.write("      ")
    target.write(str(n[j1][2]))
    target.write("\n")
    target.write("0,")
    target.write(str(4*num+1).ljust(8))
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
   
print "Writing interior done."
print segnum, ll0, rholength_interior


ll0=0
for num in range(0,segnum_wall+1):
    i=randint(0,5)
    if i == 0:
        j = randint(0,1)
        j1 = 1-j
    elif i == 1:
        j = 2+randint(0,1)
        j1 = 5-j
    elif i == 2:
        j = 2*randint(0,1)
        j1 = 2-j
    elif i == 3:
        j = 1+2*randint(0,1)
        j1 = 4-j
    elif i == 4:
        j = 3*randint(0,1)
        j1 = 3-j
    elif i == 5:
        j = 1+randint(0,1)
        j1 = 3-j
    i0=randint(0,3) 
    if i0 == 0:
        c_long0=cross([-x_ax[0], -x_ax[1], -x_ax[2]],n[j])
        c_short0=cross(c_long0,n[j1])
        c_long=c_long0/LA.norm(c_long0)
        c_short=c_short0/LA.norm(c_short0)
        x0=uniform(-Lwall/2,Lwall/2)
        y0=uniform(-Ly/2,Ly/2)
        z0=uniform(-Lz/2,Lz/2)
    elif i0 == 1:
        c_long0=cross(x_ax,n[j])
        c_short0=cross(c_long0,n[j1])
        c_long=c_long0/LA.norm(c_long0)
        c_short=c_short0/LA.norm(c_short0)
        x0=uniform(-Lwall/2,Lwall/2)
        y0=uniform(-Ly/2,Ly/2)
        z0=uniform(-Lz/2,Lz/2)
    elif i0 == 2:
        c_long0=cross([-y_ax[0], -y_ax[1], -y_ax[2]],n[j])
        c_short0=cross(c_long0,n[j1])
        c_long=c_long0/LA.norm(c_long0)
        c_short=c_short0/LA.norm(c_short0)
        x0=uniform(-Lx/2,Lx/2)
        y0=uniform(-Lwall/2,Lwall/2)
        z0=uniform(-Lz/2,Lz/2)
    elif i0 == 3:
        c_long0=cross(y_ax,n[j])
        c_short0=cross(c_long0,n[j1])
        c_long=c_long0/LA.norm(c_long0)
        c_short=c_short0/LA.norm(c_short0)
        x0=uniform(-Lx/2,Lx/2)
        y0=uniform(-Lwall/2,Lwall/2)
        z0=uniform(-Lz/2,Lz/2)
    # elif i0 == 4:
    #     c_long0=cross([-z_ax[0], -z_ax[1], -z_ax[2]],n[j])
    #     c_short0=cross(c_long0,n[j1])
    #     c_long=c_long0/LA.norm(c_long0)
    #     c_short=c_short0/LA.norm(c_short0)
    #     x0=uniform(-Lx/2+length_wall_long[num]/2,Lx/2-length_wall_long[num]/2)
    #     y0=uniform(-Ly/2+length_wall_long[num]/2,Ly/2-length_wall_long[num]/2)
    #     z0=uniform(-Lz/2+length_wall_short[num]/2,-Lz/2+Lwall-length_wall_short[num]/2)
    # elif i0 == 5:
    #     c_long0=cross(z_ax,n[j])
    #     c_short0=cross(c_long0,n[j1])
    #     c_long=c_long0/LA.norm(c_long0)
    #     c_short=c_short0/LA.norm(c_short0)
    #     x0=uniform(-Lx/2+length_wall_long[num]/2,Lx/2-length_wall_long[num]/2)
    #     y0=uniform(-Ly/2+length_wall_long[num]/2,Ly/2-length_wall_long[num]/2)
    #     z0=uniform(Lz/2-Lwall+length_wall_short[num]/2,Lz/2-length_wall_short[num]/2)

    b_sgn=2*randint(0,1)-1
    x1=x0*x_ax[0]+y0*y_ax[0]+z0*z_ax[0]+length_wall_short[num]/2*c_short[0]-length_wall_long[num]/2*c_long[0]
    x2=x0*x_ax[0]+y0*y_ax[0]+z0*z_ax[0]-length_wall_short[num]/2*c_short[0]-length_wall_long[num]/2*c_long[0]
    y1=x0*x_ax[1]+y0*y_ax[1]+z0*z_ax[1]+length_wall_short[num]/2*c_short[1]-length_wall_long[num]/2*c_long[1]
    y2=x0*x_ax[1]+y0*y_ax[1]+z0*z_ax[1]-length_wall_short[num]/2*c_short[1]-length_wall_long[num]/2*c_long[1]
    z1=x0*x_ax[2]+y0*y_ax[2]+z0*z_ax[2]+length_wall_short[num]/2*c_short[2]-length_wall_long[num]/2*c_long[2]
    z2=x0*x_ax[2]+y0*y_ax[2]+z0*z_ax[2]-length_wall_short[num]/2*c_short[2]-length_wall_long[num]/2*c_long[2]
    
    x3=x0*x_ax[0]+y0*y_ax[0]+z0*z_ax[0]+length_wall_short[num]/2*c_short[0]+length_wall_long[num]/2*c_long[0]
    x4=x0*x_ax[0]+y0*y_ax[0]+z0*z_ax[0]-length_wall_short[num]/2*c_short[0]+length_wall_long[num]/2*c_long[0]
    y3=x0*x_ax[1]+y0*y_ax[1]+z0*z_ax[1]+length_wall_short[num]/2*c_short[1]+length_wall_long[num]/2*c_long[1]
    y4=x0*x_ax[1]+y0*y_ax[1]+z0*z_ax[1]-length_wall_short[num]/2*c_short[1]+length_wall_long[num]/2*c_long[1]
    z3=x0*x_ax[2]+y0*y_ax[2]+z0*z_ax[2]+length_wall_short[num]/2*c_short[2]+length_wall_long[num]/2*c_long[2]
    z4=x0*x_ax[2]+y0*y_ax[2]+z0*z_ax[2]-length_wall_short[num]/2*c_short[2]+length_wall_long[num]/2*c_long[2]
    ll0 = ll0 + 2*sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2)+(z1-z2)*(z1-z2)) + 2*sqrt((x3-x1)*(x3-x1)+(y3-y1)*(y3-y1)+(z3-z1)*(z3-z1))

    local_1 = num_vec_prod(x1,y1,z1,x_ax,y_ax,z_ax)
    local_2 = num_vec_prod(x2,y2,z2,x_ax,y_ax,z_ax)
    local_3 = num_vec_prod(x3,y3,z3,x_ax,y_ax,z_ax)
    local_4 = num_vec_prod(x4,y4,z4,x_ax,y_ax,z_ax)

    if i0 == 0 or i0 == 1:
        if i0==0:
            if min(local_1[0],local_2[0],local_3[0],local_4[0]) < -Lwall/2:
                dx=-Lwall/2-min(local_1[0],local_2[0],local_3[0],local_4[0])
                x0=x0+1.03*dx
            elif max(local_1[0],local_2[0],local_3[0],local_4[0]) > Lwall/2:
                dx=max(local_1[0],local_2[0],local_3[0],local_4[0])-Lwall/2
                x0=x0-1.03*dx
        elif i0==0:
            if min(local_1[0],local_2[0],local_3[0],local_4[0]) < -Lwall/2:
                dx=-Lwall/2-min(local_1[0],local_2[0],local_3[0],local_4[0])
                x0=x0+1.03*dx
            elif max(local_1[0],local_2[0],local_3[0],local_4[0]) > Lwall/2:
                dx=max(local_1[0],local_2[0],local_3[0],local_4[0])-Lwall/2
                x0=x0-1.03*dx

    elif i0 == 2 or i0 == 3:
        if i0==2:
            if min(local_1[1],local_2[1],local_3[1],local_4[1]) < -Lwall/2:
                dy=-Lwall/2-min(local_1[1],local_2[1],local_3[1],local_4[1])
                y0=y0+1.03*dy
            elif max(local_1[1],local_2[1],local_3[1],local_4[1]) > Lwall/2:
                dy=max(local_1[1],local_2[1],local_3[1],local_4[1])-Lwall/2
                y0=y0-1.03*dy
        elif i0==3:
            if min(local_1[1],local_2[1],local_3[1],local_4[1]) < -Lwall/2:
                dy=-Lwall/2-min(local_1[1],local_2[1],local_3[1],local_4[1])
                y0=y0+1.03*dy
            elif max(local_1[1],local_2[1],local_3[1],local_4[1]) > Lwall/2:
                dy=max(local_1[1],local_2[1],local_3[1],local_4[1])-Lwall/2
                y0=y0-1.03*dy
                

    x1=x0*x_ax[0]+y0*y_ax[0]+z0*z_ax[0]+length_wall_short[num]/2*c_short[0]-length_wall_long[num]/2*c_long[0]
    x2=x0*x_ax[0]+y0*y_ax[0]+z0*z_ax[0]-length_wall_short[num]/2*c_short[0]-length_wall_long[num]/2*c_long[0]
    y1=x0*x_ax[1]+y0*y_ax[1]+z0*z_ax[1]+length_wall_short[num]/2*c_short[1]-length_wall_long[num]/2*c_long[1]
    y2=x0*x_ax[1]+y0*y_ax[1]+z0*z_ax[1]-length_wall_short[num]/2*c_short[1]-length_wall_long[num]/2*c_long[1]
    z1=x0*x_ax[2]+y0*y_ax[2]+z0*z_ax[2]+length_wall_short[num]/2*c_short[2]-length_wall_long[num]/2*c_long[2]
    z2=x0*x_ax[2]+y0*y_ax[2]+z0*z_ax[2]-length_wall_short[num]/2*c_short[2]-length_wall_long[num]/2*c_long[2]
    
    x3=x0*x_ax[0]+y0*y_ax[0]+z0*z_ax[0]+length_wall_short[num]/2*c_short[0]+length_wall_long[num]/2*c_long[0]
    x4=x0*x_ax[0]+y0*y_ax[0]+z0*z_ax[0]-length_wall_short[num]/2*c_short[0]+length_wall_long[num]/2*c_long[0]
    y3=x0*x_ax[1]+y0*y_ax[1]+z0*z_ax[1]+length_wall_short[num]/2*c_short[1]+length_wall_long[num]/2*c_long[1]
    y4=x0*x_ax[1]+y0*y_ax[1]+z0*z_ax[1]-length_wall_short[num]/2*c_short[1]+length_wall_long[num]/2*c_long[1]
    z3=x0*x_ax[2]+y0*y_ax[2]+z0*z_ax[2]+length_wall_short[num]/2*c_short[2]+length_wall_long[num]/2*c_long[2]
    z4=x0*x_ax[2]+y0*y_ax[2]+z0*z_ax[2]-length_wall_short[num]/2*c_short[2]+length_wall_long[num]/2*c_long[2]
  
    target.write("0,")
    target.write(str(4*segnum+4+4*num).ljust(8)) #1
    target.write(str())
    target.write("		")
    target.write(str(x1))
    target.write("		")
    target.write(str(y1))
    target.write("		")
    target.write(str(z1))
    target.write("		")
    target.write("2		0")
    target.write("\n")
    target.write("0.0000")
    target.write("      ")
    target.write("0.0000")
    target.write("      ")
    target.write("0.0000")
    target.write("\n")
    target.write("0,")
    target.write(str(4*segnum+4+4*num+1).ljust(8)) #2
    target.write(str(b_sgn*b[i][0]))
    target.write("      ")
    target.write(str(b_sgn*b[i][1]))
    target.write("      ")
    target.write(str(b_sgn*b[i][2]))
    target.write("\n")
    target.write(str(n[j1][0]))
    target.write("      ")
    target.write(str(n[j1][1]))
    target.write("      ")
    target.write(str(n[j1][2]))
    target.write("\n")
    target.write("0,")
    target.write(str(4*segnum+4+4*num+2).ljust(8)) #3
    target.write(str(-b_sgn*b[i][0]))
    target.write("      ")
    target.write(str(-b_sgn*b[i][1]))
    target.write("      ")
    target.write(str(-b_sgn*b[i][2]))
    target.write("\n")
    target.write(str(n[j][0]))
    target.write("      ")
    target.write(str(n[j][1]))
    target.write("      ")
    target.write(str(n[j][2]))
    target.write("\n")

    target.write("0,")
    target.write(str(4*segnum+4+4*num+1).ljust(8)) #2
    target.write(str())
    target.write("		")
    target.write(str(x2))
    target.write("		")
    target.write(str(y2))
    target.write("		")
    target.write(str(z2))
    target.write("		")
    target.write("2		0")
    target.write("\n")
    target.write("0.0000")
    target.write("      ")
    target.write("0.0000")
    target.write("      ")
    target.write("0.0000")
    target.write("\n")
    target.write("0,")
    target.write(str(4*segnum+4+4*num+3).ljust(8))     #4
    target.write(str(b_sgn*b[i][0]))
    target.write("      ")
    target.write(str(b_sgn*b[i][1]))
    target.write("      ")
    target.write(str(b_sgn*b[i][2]))
    target.write("\n")
    target.write(str(n[j][0]))
    target.write("      ")
    target.write(str(n[j][1]))
    target.write("      ")
    target.write(str(n[j][2]))
    target.write("\n")
    target.write("0,")
    target.write(str(4*segnum+4+4*num).ljust(8))  #1
    target.write(str(-b_sgn*b[i][0]))
    target.write("      ")
    target.write(str(-b_sgn*b[i][1]))
    target.write("      ")
    target.write(str(-b_sgn*b[i][2]))
    target.write("\n")
    target.write(str(n[j1][0]))
    target.write("      ")
    target.write(str(n[j1][1]))
    target.write("      ")
    target.write(str(n[j1][2]))
    target.write("\n")

    target.write("0,")
    target.write(str(4*segnum+4+4*num+2).ljust(8))  #3
    target.write(str())
    target.write("		")
    target.write(str(x3))
    target.write("		")
    target.write(str(y3))
    target.write("		")
    target.write(str(z3))
    target.write("		")
    target.write("2		0")
    target.write("\n")
    target.write("0.0000")
    target.write("      ")
    target.write("0.0000")
    target.write("      ")
    target.write("0.0000")
    target.write("\n")
    target.write("0,")
    target.write(str(4*segnum+4+4*num).ljust(8))  #1
    target.write(str(b_sgn*b[i][0]))
    target.write("      ")
    target.write(str(b_sgn*b[i][1]))
    target.write("      ")
    target.write(str(b_sgn*b[i][2]))
    target.write("\n")
    target.write(str(n[j][0]))
    target.write("      ")
    target.write(str(n[j][1]))
    target.write("      ")
    target.write(str(n[j][2]))
    target.write("\n")
    target.write("0,")
    target.write(str(4*segnum+4+4*num+3).ljust(8))  #4
    target.write(str(-b_sgn*b[i][0]))
    target.write("      ")
    target.write(str(-b_sgn*b[i][1]))
    target.write("      ")
    target.write(str(-b_sgn*b[i][2]))
    target.write("\n")
    target.write(str(n[j1][0]))
    target.write("      ")
    target.write(str(n[j1][1]))
    target.write("      ")
    target.write(str(n[j1][2]))
    target.write("\n")

    target.write("0,")
    target.write(str(4*segnum+4+4*num+3).ljust(8))
    target.write(str())
    target.write("		")
    target.write(str(x4))
    target.write("		")
    target.write(str(y4))
    target.write("		")
    target.write(str(z4))
    target.write("		")
    target.write("2		0")
    target.write("\n")
    target.write("0.0000")
    target.write("      ")
    target.write("0.0000")
    target.write("      ")
    target.write("0.0000")
    target.write("\n")
    target.write("0,")
    target.write(str(4*segnum+4+4*num+2).ljust(8))
    target.write(str(b_sgn*b[i][0]))
    target.write("      ")
    target.write(str(b_sgn*b[i][1]))
    target.write("      ")
    target.write(str(b_sgn*b[i][2]))
    target.write("\n")
    target.write(str(n[j1][0]))
    target.write("      ")
    target.write(str(n[j1][1]))
    target.write("      ")
    target.write(str(n[j1][2]))
    target.write("\n")
    target.write("0,")
    target.write(str(4*segnum+4+4*num+1).ljust(8))
    target.write(str(-b_sgn*b[i][0]))
    target.write("      ")
    target.write(str(-b_sgn*b[i][1]))
    target.write("      ")
    target.write(str(-b_sgn*b[i][2]))
    target.write("\n")
    target.write(str(n[j][0]))
    target.write("      ")
    target.write(str(n[j][1]))
    target.write("      ")
    target.write(str(n[j][2]))
    target.write("\n")
print "Writing wall done."
print ll0, rholength_wall

ll0=0
for num in range(0,segnum_fr+1):     
#should be less than 1.000E+6 with current .ctrl file
    x0=uniform(-Dimx/2+length_fr[num]/2,Dimx/2-length_fr[num]/2)
    y0=uniform(-Dimy/2+length_fr[num]/2,Dimy/2-length_fr[num]/2)
    z0=uniform(-Dimz/2+length_fr[num]/2,Dimz/2-length_fr[num]/2)
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

    x1=x0+length_fr[num]*c[0]/2
    x2=x0-length_fr[num]*c[0]/2
    y1=y0+length_fr[num]*c[1]/2
    y2=y0-length_fr[num]*c[1]/2
    z1=z0+length_fr[num]*c[2]/2
    z2=z0-length_fr[num]*c[2]/2
    ll0 = ll0 + sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2)+(z1-z2)*(z1-z2))
    target.write("0,")
    target.write(str(4*segnum+4*segnum_wall+8+3*num).ljust(8))
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
    target.write(str(4*segnum+4*segnum_wall+8+3*num+1).ljust(8))
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
    target.write(str(4*segnum+4*segnum_wall+8+3*num+1).ljust(8))
    target.write(str())
    target.write("		")
    target.write(str(x1/2+x2/2))
    target.write("		")
    target.write(str(y2/2+y1/2))
    target.write("		")
    target.write(str(z2/2+z1/2))
    target.write("		")
    target.write("2		7")
    target.write("\n")
    target.write("0.0000")
    target.write("      ")
    target.write("0.0000")
    target.write("      ")
    target.write("0.0000")
    target.write("\n")
    target.write("0,")
    target.write(str(4*segnum+4*segnum_wall+8+3*num).ljust(8))
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
    target.write("0,")
    target.write(str(4*segnum+4*segnum_wall+8+3*num+2).ljust(8))
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
    target.write(str(4*segnum+4*segnum_wall+8+3*num+2).ljust(8))
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
    target.write(str(4*segnum+4*segnum_wall+8+3*num+1).ljust(8))
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

print "Writing FR done."
print ll0, rholength_interior

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
