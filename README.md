# Whittier Saw Mill Runaround

Source: https://github.com/jamesplotts/wittiersawmillrunaround
Download: https://www.nexusmods.com/railroader/mods/2322 (or the GitHub releases)

A small track mod for Railroader 0.6 (Maintenance of Way). It adds a runaround track beside the Whittier Saw Mill lead, so a log train can pull down the lead, run its engine around the cars and shove them into the mill tracks, without turning on the wye.

- The upper switch is on the lead about 60 m above the first mill spur switch. The lower switch is below the last spur switch, about 20 m above the unloading spot at the end of the lead. The runaround is about 295 m long switch to switch, with roughly 230 m of clear track for cars.
- It runs 4.5 m (track centers) from the lead on the side away from the mill, following the lead's bend. The curves through the switches are about 155 m radius, gentler than the mill's own spur switches. Everything is level, at the lead's height.
- No existing track is moved or split. Both switches are on existing nodes of the lead, so cars already on the lead aren't disturbed.
- The new track crosses the mill's dirt road just above the lower switch, where the lead already crosses it.

## With Chilly's East Whittier Sawmill

[Chilly's East Whittier Sawmill](https://www.nexusmods.com/railroader/mods/1967) moves the mill lead's switches and adds a track down its south-west side, right where the plain runaround runs. When it's installed, this mod uses a second layout that goes around all of its switches instead:

- The upper switch is on the lead at N2qd, about 85 m above where the plain layout leaves it. Chilly moves the first spur switch to within 27 m of N5r2, too close to turn out there.
- It runs 4.5 m (track centers) south-west of the left-hand-most track, past every switch on the lead and Chilly's new left-hand track.
- The lower switch is on Chilly's left-hand track, 50 m below N3dmxsgyp. That segment (S3dmxdn86) is split in two at the new switch; the curve moves by under 10 cm.
- About 360 m switch to switch. The tightest curve is the lead's own bend (about 96 m radius, which the runaround follows); the turnouts are about 170 m and 355 m radius.
- Chilly's track dips below N3dmxsgyp, so the runaround drops about 36 cm over its last 35 m to meet it level at the lower switch.
- Chilly's sawmill road crosses the runaround and Chilly's left-hand track near the lower switch with its surface a few centimetres above the rails. The mod lowers that road point (`wh-sawmill-road`, point `n`) by 17 cm so both tracks clear it.

No setting is needed: the mod loads after Chilly's and checks whether Chilly's track is in the map.

## Install

Copy this folder (`Info.json`, `Data/`, `Scripts/`) to `Documents\Railroader\Mods\WittierSawmillRunaround\`, then enable it under **Mods** on the main menu. It's a data mod, so it doesn't need "Allow Unsafe DLL Mods".

## How it works

`Scripts/Data.rl` looks for Chilly's sawmill track in the map and merges `Data/MapChilly.json` if it's there, `Data/Map.json` if not. `Info.json` loads the mod after Chilly's (`load.after`), which the game ignores when Chilly's isn't installed. The new nodes and segments use `jamesplotts/wsr/...` ids so they can't clash with other mods. `tools/design.py` computes the plain layout from the base map (`python3 tools/design.py [spacing]`), `tools/design_chilly.py` the Chilly layout from the base map plus BMR's East Whittier Yard and Chilly's sawmill as installed (`python3 tools/design_chilly.py [spacing] [split]`), and `tools/frogcheck.py [chilly]` checks that the game will build the switches with their frogs and stands. They use the Bézier helpers in the Sylva Tie-In repo's `tools/track.py`.
