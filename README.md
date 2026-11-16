# Whittier Saw Mill Runaround

A small track mod for Railroader 0.6 (Maintenance of Way). It adds a runaround track beside the Whittier Saw Mill lead, so a log train can pull down the lead, run its engine around the cars and shove them into the mill tracks, without turning on the wye.

- The upper switch is on the lead about 60 m above the first mill spur switch. The lower switch is below the last spur switch, about 20 m above the unloading spot at the end of the lead. The runaround is about 295 m long switch to switch, with roughly 230 m of clear track for cars.
- It runs 4.5 m (track centers) from the lead on the side away from the mill, following the lead's bend. The curves through the switches are about 155 m radius, gentler than the mill's own spur switches. Everything is level, at the lead's height.
- No existing track is moved or split. Both switches are on existing nodes of the lead, so cars already on the lead aren't disturbed.
- The new track crosses the mill's dirt road just above the lower switch, where the lead already crosses it.

## Install

Copy this folder (`Info.json`, `Data/`, `Scripts/`) to `Documents\Railroader\Mods\WittierSawmillRunaround\`, then enable it under **Mods** on the main menu. It's a data mod, so it doesn't need "Allow Unsafe DLL Mods".

## How it works

`Scripts/Data.rl` merges `Data/Map.json` into the base map when it loads. The new nodes and segments use `jamesplotts/wsr/...` ids so they can't clash with other mods. `tools/design.py` computes the track from the base map (`python3 tools/design.py [spacing]`) and `tools/frogcheck.py` checks that the game will build both switches with their frogs and stands. They use the Bézier helpers in the Sylva Tie-In repo's `tools/track.py`.
