# Designs the runaround on the southwest side of the Whittier Saw Mill lead: a switch at N5r2
# (above the spur switches) and one at Ntky0n5l7 (below them, above the unloading spot),
# with the new track D metres off the lead, following its dogleg.
import sys,json,math
sys.path.insert(0,'/home/jamesp/railroadermods/sylvatie/tools')
from track import *
D=float(sys.argv[1]) if len(sys.argv)>1 else 4.5
UP,LO='N5r2','Ntky0n5l7'
MID=['Ndk9','Nzrr','Ni3o','N638','Ntky0hii3','Ntky0khft']   # lead nodes the new track runs beside
P='jamesplotts/wsr/'
def head(n):   # heading pointing down the lead (south-east)
    h=N[n]['rotation'][1]%360
    return h if 90<h<270 else (h+180)%360
def off(n):
    p=N[n]['position']; h=math.radians(head(n)); rx,rz=math.cos(h),-math.sin(h)   # right of travel = south-west
    return {'position':[round(p[0]+rx*D,3),p[1],round(p[2]+rz*D,3)],'rotation':[0.0,round(head(n),4),0.0]}
nodes={P+'%d'%i:off(n) for i,n in enumerate(MID)}
chain=[UP]+list(nodes)+[LO]
segs={P+'s%d'%i:{'a':chain[i],'b':chain[i+1]} for i in range(len(chain)-1)}
allN=dict(N); allN.update(nodes)
def radius(pts):
    r=1e9
    for i in range(1,len(pts)-1):
        a,b,c=[(p[0],p[2]) for p in pts[i-1:i+2]]
        A=math.dist(a,b);B=math.dist(b,c);C=math.dist(a,c)
        area=abs((b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]))/2
        if area>1e-9: r=min(r,A*B*C/(4*area))
    return r
lead=[p for s in ['S5ej','S5ky','Sbn4','Sju3','Stky0fgyb','Stky0gupa','Stky0llr8'] for p in bez(N[S[s]['a']],N[S[s]['b']],200)]
total=0
for k,s in segs.items():
    pts=bez(allN[s['a']],allN[s['b']],200); L=length(pts); total+=L
    sp=[min(math.dist([q[0],q[2]],[r[0],r[2]]) for r in lead) for q in pts[20:-20]]
    print(f"{k}: {s['a']}->{s['b']} {L:.1f} m, min radius {radius(pts):.0f} m, spacing to lead {min(sp):.2f}-{max(sp):.2f}")
print(f"runaround {total:.1f} m")
# reference: radius of the existing spur turnouts
for s in ['Sq42','S81g','Sxiy','S5ky','Sbn4','Stky0gupa']: print('  existing',s,f"{radius(bez(N[S[s]['a']],N[S[s]['b']],200)):.0f} m")
json.dump({'graph':{'nodes':nodes,'segments':segs}},open('Data/Map.json','w'),indent=2)
