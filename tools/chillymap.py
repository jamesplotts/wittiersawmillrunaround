# The map as the game builds it with Chilly's East Whittier Sawmill: the base map, BMR's East
# Whittier Yard (Chilly requires it) and Chilly's sawmill, merged in load order (JSON merge patch).
import json,copy,os
MODS=os.path.expanduser('~/.local/share/Steam/steamapps/compatdata/1683150/pfx/drive_c/users/steamuser/Documents/Railroader/Mods/')
BASE=os.path.expanduser('~/.local/share/Steam/steamapps/common/Railroader/Railroader_Data/StreamingAssets/AssetPacksCore/nc-bryson-terrain/Data/Map.json')
def merge(t,p):
    for k,v in p.items():
        if v is None: t.pop(k,None)
        elif isinstance(v,dict) and isinstance(t.get(k),dict): merge(t[k],v)
        else: t[k]=copy.deepcopy(v)
def load(chilly=True,extra=()):
    m=json.load(open(BASE))
    if chilly:
        for d in ('bmr-east-whittier-yard','chilly-east-whitter-sawmill'):
            merge(m,json.load(open(MODS+d+'/Data/Map.json')))
    for f in extra: merge(m,json.load(open(f)))
    return m
