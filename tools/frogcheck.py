# Checks the new switches the way the game's SwitchGeometry does: the inner rails of the two
# legs must cross (the frog) within 2 cm in 3D, or the game draws plain track with no stand.
import sys,json,math
sys.path.insert(0,'/home/jamesp/railroadermods/sylvatie/tools')
from track import *
mod=json.load(open('Data/Map.json'))['graph']
for k,v in mod['nodes'].items(): N[k]=v
for SW,LEG,NEW in [('N5r2','Ndk9','jamesplotts/wsr/0'),('Ntky0n5l7','Ntky0khft','jamesplotts/wsr/5')]:
 print('switch',SW)
 def curve(a,b,n=400):
     p=bez(N[a],N[b],n)
     return p if a==SW else p[::-1]
 A=curve(SW,LEG); B=curve(SW,NEW)
 G=1.435/2
 def rails(P):
     L=[];R=[]
     for i in range(len(P)):
         j=min(i+1,len(P)-1); k=max(j-1,0)
         dx,dz=P[j][0]-P[k][0],P[j][2]-P[k][2]; l=math.hypot(dx,dz)
         # right-hand normal in Unity (x right, z forward): right of forward (dx,dz) is (dz,-dx)
         rx,rz=dz/l,-dx/l
         L.append((P[i][0]-rx*G,P[i][1],P[i][2]-rz*G)); R.append((P[i][0]+rx*G,P[i][1],P[i][2]+rz*G))
     return L,R
 AL,AR=rails(A); BL,BR=rails(B)
 def cross(P,Q):
     for i in range(1,len(P)):
         for j in range(1,len(Q)):
             p0,p1,q0,q1=P[i-1],P[i],Q[j-1],Q[j]
             d=(p1[0]-p0[0])*(q1[2]-q0[2])-(p1[2]-p0[2])*(q1[0]-q0[0])
             if abs(d)<1e-12: continue
             t=((q0[0]-p0[0])*(q1[2]-q0[2])-(q0[2]-p0[2])*(q1[0]-q0[0]))/d
             u=((q0[0]-p0[0])*(p1[2]-p0[2])-(q0[2]-p0[2])*(p1[0]-p0[0]))/d
             if 0<t<=1 and 0<u<=1 and i>2:
                 ya=p0[1]+t*(p1[1]-p0[1]); yb=q0[1]+u*(q1[1]-q0[1])
                 return i, ya, yb
     return None
 for name,(P,Q) in {'A.left x B.right':(AL,BR),'A.right x B.left':(AR,BL)}.items():
     r=cross(P,Q)
     if r: i,ya,yb=r; print(name, f"at ~{length(A[:i+1]):.1f} m from points: main y {ya:.3f}, tie y {yb:.3f}, diff {100*(yb-ya):.1f} cm")
     else: print(name,'none')
 # separation along
 for d in [5,10,20,30,40]:
     i=min(range(len(A)),key=lambda i:abs(length(A[:i+1])-d))
     q=min(B,key=lambda q:math.dist([q[0],q[2]],[A[i][0],A[i][2]]))
     print(d,'m: sep',round(math.dist([q[0],q[2]],[A[i][0],A[i][2]]),3),'dy',round(q[1]-A[i][1],3))
