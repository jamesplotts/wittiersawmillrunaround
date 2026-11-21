import json
import log

// Chilly's East Whittier Sawmill (chilly/east-whitter-sawmill) moves the mill lead's switches
// and adds a track down its south-west side, so it gets a layout of its own. Info.json loads
// this mod after Chilly's, so if Chilly's is on, its track is already in the map here.
func modifyMap(map) {
    var found = { "chilly": false }
    map.modify((data) => {
        let nodes = data["graph"]?["nodes"]
        let segments = data["graph"]?["segments"]
        if nodes?["N3dmxsgyp"] != null && nodes?["N3dmx11e5"] != null && segments?["S3dmxdn86"] != null {
            found["chilly"] = true
        }
    })
    if found["chilly"] {
        log.info("Whittier Saw Mill Runaround: Chilly's East Whittier Sawmill found, using its layout")
        map.merge(json.load("Data/MapChilly.json"))
    } else {
        map.merge(json.load("Data/Map.json"))
    }
}
