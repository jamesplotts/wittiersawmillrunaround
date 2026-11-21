# The runaround for Chilly's East Whittier Sawmill (Nexus 1967). Chilly moves the mill lead's
# switches and adds a track down the south-west side, so this layout replaces the plain one:
# it leaves the lead at N2qd (Chilly moves Ndk9 to within 27 m of N5r2, too close to turn out
# there), runs D metres south-west of the left-hand-most track past every switch (Ndk9, Nzrr,
# Ni3o, N638, Ntky0hii3, N3dmx11e5) and joins Chilly's left
# track S3dmxdn86 at a new switch node X, SPLIT metres below N3dmxsgyp. S3dmxdn86 is split there.
#   python3 tools/design_chilly.py [D] [SPLIT]
import sys,json,math,os
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,'/home/jamesp/railroadermods/sylvatie/tools'); sys.path.insert(0,HERE)
from track import bez,length
from chillymap import load
m=load(True); N=m['graph']['nodes']; S=m['graph']['segments']
D=float(sys.argv[1]) if len(sys.argv)>1 else 4.5
SPLIT=float(sys.argv[2]) if len(sys.argv)>2 else 50.0
UP='N2qd'
MID=['N5r2','Ndk9','Nzrr','Ni3o','N638','Ntky0hii3','N3dmx11e5']
P='jamesplotts/wsr/c'
SPLITSEG='S3dmxdn86'; X=P+'x'
def head(n):   # heading pointing down the lead (south-east)
    h=N[n]['rotation'][1]%360
    return h if 90<h<270 else (h+180)%360
def off(n):
    p=N[n]['position']; h=math.radians(head(n)); rx,rz=math.cos(h),-math.sin(h)   # right of travel = south-west
    return {'position':[round(p[0]+rx*D,3),round(p[1],3),round(p[2]+rz*D,3)],'rotation':[0.0,round(head(n),4),0.0]}
# the split node on Chilly's left track
seg=S[SPLITSEG]; A,B=seg['a'],seg['b']
orig=bez(N[A],N[B],2000)
acc=0;i=0
while acc<SPLIT: acc+=math.dist(orig[i],orig[i+1]); i+=1
p=orig[i]; q0,q1=orig[i-5],orig[i+5]   # A is up the lead, so q0->q1 points south-east
dx,dy,dz=[q1[k]-q0[k] for k in range(3)]
hd=math.degrees(math.atan2(dx,dz))%360; pitch=-math.degrees(math.asin(dy/math.sqrt(dx*dx+dy*dy+dz*dz)))
xnode={'position':[round(p[0],3),round(p[1],3),round(p[2],3)],'rotation':[round(pitch,4),round(hd,4),0.0]}
nodes={P+'%d'%i:off(n) for i,n in enumerate(MID)}
nodes[X]=xnode
chain=[UP]+[P+'%d'%i for i in range(len(MID))]+[X]
segs={P+'s%d'%i:{'a':chain[i],'b':chain[i+1]} for i in range(len(chain)-1)}
attrs={k:v for k,v in seg.items() if k not in ('a','b')}
split={SPLITSEG:None, P+'d0':dict(a=A,b=X,**attrs), P+'d1':dict(a=X,b=B,**attrs)}
allN=dict(N); allN.update(nodes)
# Chilly's left track dips below N3dmxsgyp and X is near the bottom of the dip. Lower the last
# runaround node until both legs out of X are level where the frog falls (about 31 m out),
# otherwise the game won't build the switch.
def y_at(a,b,d):
    pts=bez(allN[a],allN[b],400); acc=0
    for i in range(len(pts)-1):
        acc+=math.dist(pts[i],pts[i+1])
        if acc>=d: return pts[i+1][1]
LAST=P+'%d'%(len(MID)-1)
lo,hi=allN[X]['position'][1],allN[LAST]['position'][1]
for _ in range(40):
    mid=(lo+hi)/2; nodes[LAST]['position'][1]=mid
    if y_at(X,LAST,31)>y_at(X,A,31): hi=mid
    else: lo=mid
nodes[LAST]['position'][1]=round(mid,3)
print(f"{LAST} lowered to y {mid:.3f} (lead beside it {N[MID[-1]]['position'][1]:.3f})")
def radius(pts):
    r=1e9
    for i in range(1,len(pts)-1):
        a,b,c=[(p[0],p[2]) for p in pts[i-1:i+2]]
        A_=math.dist(a,b);B_=math.dist(b,c);C=math.dist(a,c)
        area=abs((b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]))/2
        if area>1e-9: r=min(r,A_*B_*C/(4*area))
    return r
# the split must not move Chilly's track
new=bez(allN[A],allN[X],400)+bez(allN[X],allN[B],400)
dev=max(min(math.dist(q,r) for r in orig[::2]) for q in new[::4])
print(f"split {SPLITSEG} {SPLIT:.0f} m below {A}: max deviation from Chilly's curve {100*dev:.1f} cm")
near={k:bez(N[s['a']],N[s['b']],100) for k,s in S.items() if s['a'] in N and s['b'] in N
      and math.dist([N[s['a']]['position'][0],N[s['a']]['position'][2]],[12320,5100])<250}
ends=[N[UP]['position'],xnode['position']]
total=0
for k,s in segs.items():
    pts=bez(allN[s['a']],allN[s['b']],200); L=length(pts); total+=L
    inner=[q for q in pts if all(math.dist([q[0],q[2]],[e[0],e[2]])>30 for e in ends)]
    txt=f"{k}: {s['a']}->{s['b']} {L:.1f} m, min radius {radius(pts):.0f} m"
    if inner:
        c=min((min(math.dist([q[0],q[2]],[r[0],r[2]]) for q in inner[::4] for r in v[::2]),sk) for sk,v in near.items() if sk!=SPLITSEG)
        txt+=f", nearest other track {c[0]:.2f} m ({c[1]})"
    print(txt)
print(f"runaround {total:.1f} m switch to switch")
# Chilly's sawmill road crosses the runaround and Chilly's left track at its control point "n",
# about 7 cm above the rails, so the road surface buries them. Lower that point so both clear it.
ROADDROP=0.17
rn=m['objects']['wh-sawmill-road']['params']['points']['n']
road={'wh-sawmill-road':{'params':{'points':{'n':{'position':[rn['position'][0],round(rn['position'][1]-ROADDROP,6),rn['position'][2]]}}}}}
json.dump({'graph':{'nodes':nodes,'segments':{**segs,**split}},'objects':road},open(os.path.join(HERE,'..','Data','MapChilly.json'),'w'),indent=2)
