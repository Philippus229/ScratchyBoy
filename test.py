import json, zipfile
from tkinter.filedialog import askopenfilename

sb3to2commands = [
    ["event_whenflagclicked", "whenGreenFlag"],
    ["motion_gotoxy", "gotoX:y:"],
    ["pen_penDown", "putPenDown"],
    ["pen_penUp", "putPenUp"],
    ["control_wait", "wait:elapsed:from:"]
] #TODO: add remaining commands

sb3to2rotStyles = [
    ["all around", "normal"],
] #TODO: add remaining rotation styles

sb3sounds = []
sb3soundsmd5 = []
sb3costumes = []
sb3costumesmd5 = []
spritecount = 0

def getSoundID(aID):
    return sb3sounds.index(aID)

def getSoundIDmd5(md5):
    return sb3soundsmd5.index(md5)

def getCostumeID(aID):
    return sb3costumes.index(aID)

def getCostumeIDmd5(md5):
    return sb3costumesmd5.index(md5)

def c3to2(c):
    return [e[1] for e in sb3to2commands if e[0] == c][0]

def get2rotStyle(rS):
    return [e[1] for e in sb3to2rotStyles if e[0] == rS][0]

def get2command(c, i, f):
    c = c3to2(c)
    s = [i[i0][1][1] for i0 in i]
    tmpoutthing = []
    tmpoutthing.append(c)
    for s0 in s:
        tmpoutthing.append(s0)
    return tmpoutthing
    
class sb3Costume:
    def __init__(self, aID, n, bR, md5, dF, rCX, rCY):
        self.assetID = aID
        self.name = n
        self.bitmapResolution = bR
        self.md5ext = md5
        self.dataFormat = dF
        self.rotationCenterX = rCX
        self.rotationCenterY = rCY
        sb3costumes.append(aID)
        sb3costumesmd5.append(md5)

class sb3Sound:
    def __init__(self, aID, n, dF, f, r, sC, md5):
        self.assetID = aID
        self.name = n
        self.dataFormat = dF
        self.format = f
        self.rate = r
        self.sampleCount = sC
        self.md5ext = md5
        sb3sounds.append(aID)
        sb3soundsmd5.append(md5)

class sb3Object:
    def __init__(self, n, cC, v, lO, vi, x, y, s, d, iD, rS):
        self.name = n
        self.variables = []
        self.lists = []
        self.broadcasts = []
        self.blocks = []
        self.comments = []
        self.currentCostume = cC
        self.costumes = []
        self.sounds = []
        self.volume = v
        self.layerOrder = lO
        self.visible = vi
        self.x = x
        self.y = y
        self.size = s
        self.direction = d
        self.draggable = iD
        self.rotationStyle = rS
        spritecount += 1

class sb3Stage:
    def __init__(self, n, cC, v, lO, t, vT, vS, tTSL):
        self.name = n
        self.variables = []
        self.lists = []
        self.broadcasts = []
        self.blocks = []
        self.comments = []
        self.currentCostume = cC
        self.costumes = []
        self.sounds = []
        self.volume = v
        self.layerOrder = lO
        self.tempo = t
        self.videoTransparency = vT
        self.videoState = vS
        self.textToSpeechLanguage = tTSL
        self.children = []

class sb3Block:
    def __init__(self, o, n, i, f, s):
        self.opcode = o
        self.next = n
        self.inputs = i
        self.fields = f
        self.shadow = s

class sb3TopBlock:
    def __init__(self, o, n, i, f, s, x, y):
        self.opcode = o
        self.next = n
        self.inputs = i
        self.fields = f
        self.shadow = s
        self.x = x
        self.y = y
        self.children = [] #temporary until I find a better solution

class sb3Project:
    def __init__(self):
        self.stages = []

def convert3to2json(p):
    sb2 = "{\n"
    for s in p.stages:
        sb2 += f"    \"objName\": \"{s.name}\",\n"
        sb2 += "    \"sounds\": [{\n"
        for snd in s.sounds:
            if not snd == s.sounds[0]:
                sb2 += "        },\n        {\n"
            sb2 += f"            \"soundName\": \"{snd.name}\",\n"
            sb2 += f"            \"soundID\": {getSoundID(snd.assetID)},\n"
            sb2 += f"            \"md5\": \"{snd.md5ext}\",\n"
            sb2 += f"            \"sampleCount\": {snd.sampleCount},\n"
            sb2 += f"            \"rate\": {snd.rate},\n"
            sb2 += f"            \"format\": \"{snd.format}\"\n"
        sb2 += "        }],\n    \"costumes\": [{\n"
        for c in s.costumes:
            if not c == s.costumes[0]:
                sb2 += "        },\n        {\n"
            sb2 += f"            \"costumeName\": \"{c.name}\",\n"
            sb2 += f"            \"baseLayerID\": {getCostumeID(c.assetID)},\n"
            sb2 += f"            \"baseLayerMD5\": \"{c.md5ext}\",\n"
            sb2 += f"            \"bitmapResolution\": {c.bitmapResolution},\n"
            sb2 += f"            \"rotationCenterX\": {c.rotationCenterX},\n"
            sb2 += f"            \"rotationCenterY\": {c.rotationCenterY}\n"
        sb2 += "        }],\n"
        sb2 += f"    \"currentCostumeIndex\": {s.currentCostume},\n"
        sb2 += f"    \"penLayerMD5\": \"TODO_find_pen_layer_md5\",\n" #TODO
        sb2 += f"    \"penLayerID\": {s.layerOrder},\n"
        sb2 += f"    \"tempoBPM\": {s.tempo},\n"
        sb2 += f"    \"videoAlpha\": {s.videoTransparency/100},\n"
        sb2 += "    \"children\": [{\n"
        for o in s.children:
            if not o == s.children[0]:
                sb2 += "        },\n        {\n"
            sb2 += f"            \"objName\": \"{o.name}\",\n"
            sb2 += f"            \"scripts\": [\n"
            for b in o.blocks:
                sb2 += f"                    [{b.x},\n"
                sb2 += f"                    {b.y},\n"
                sb2 += f"                    [{get2command(b.opcode, b.inputs, b.fields)}"
                for cB in b.children:
                    sb2 += ","
                    sb2 += f"\n                        {get2command(cB.opcode, cB.inputs, cB.fields)}"
                sb2 += "\n                    ]]\n"
            sb2 += "                ],\n"
            sb2 += "            \"sounds\": [{\n"
            for snd in o.sounds:
                if not snd == o.sounds[0]:
                    sb2 += "                },\n                {\n"
                sb2 += f"                    \"soundName\": \"{snd.name}\",\n"
                sb2 += f"                    \"soundID\": {getSoundID(snd.assetID)},\n"
                sb2 += f"                    \"md5\": \"{snd.md5ext}\",\n"
                sb2 += f"                    \"sampleCount\": {snd.sampleCount},\n"
                sb2 += f"                    \"rate\": {snd.rate},\n"
                sb2 += f"                    \"format\": \"{snd.format}\"\n"
            sb2 += "                }],\n            \"costumes\": [{\n"
            for c in o.costumes:
                if not c == o.costumes[0]:
                    sb2 += "                },\n                {\n"
                sb2 += f"                    \"costumeName\": \"{c.name}\",\n"
                sb2 += f"                    \"baseLayerID\": {getCostumeID(c.assetID)},\n"
                sb2 += f"                    \"baseLayerMD5\": \"{c.md5ext}\",\n"
                sb2 += f"                    \"bitmapResolution\": {c.bitmapResolution},\n"
                sb2 += f"                    \"rotationCenterX\": {c.rotationCenterX},\n"
                sb2 += f"                    \"rotationCenterY\": {c.rotationCenterY}\n"
            sb2 += "                }],\n"
            sb2 += f"            \"currentCostumeIndex\": {o.currentCostume},\n"
            sb2 += f"            \"scratchX\": {o.x},\n"
            sb2 += f"            \"scratchY\": {o.y},\n"
            sb2 += f"            \"scale\": {o.size/100},\n"
            sb2 += f"            \"direction\": {o.direction},\n"
            sb2 += f"            \"rotationStyle\": \"{get2rotStyle(o.rotationStyle)}\",\n"
            sb2 += f"            \"isDraggable\": {o.draggable},\n"
            sb2 += f"            \"indexInLibrary\": {o.layerOrder},\n"
            sb2 += f"            \"visible\": {o.visible},\n"
            sb2 += "            \"spriteInfo\": {}\n" #TODO: figure out what this is
            sb2 += "        }],\n"
        sb2 += "    \"info\": {\n"
        sb2 += "        \"userAgent\": \"Scratch 2.0 Offline Editor\",\n"
        sb2 += "        \"swfVersion\": \"v461\",\n"
        sb2 += "        \"flashVersion\": \"WIN 31,0,0,108\",\n"
        sb2 += f"        \"scriptCount\": {1},\n" #TODO: get actual script count
        sb2 += f"        \"videoOn\": {False},\n" #TODO: figure out what this is
        sb2 += f"        \"spriteCount\": {spritecount}\n"
        sb2 += "    }\n}"
    return sb2.replace("'", "\"").replace("False", "false").replace("True", "true")

curStage = None
sb3fn = askopenfilename(title="Select 3.0 Project...", filetypes=[("Scratch 3.0 Project", "*.sb3")])
sb3 = zipfile.ZipFile(sb3fn, "r")
sb3json = json.loads(sb3.read("project.json"))
project = sb3Project()
for t in sb3json["targets"]:
    print("")
    curObject = None
    if t["isStage"]:
        curObject = sb3Stage(t["name"], t["currentCostume"], t["volume"], t["layerOrder"], t["tempo"], t["videoTransparency"], t["videoState"], t["textToSpeechLanguage"])
    else:
        curObject = sb3Object(t["name"], t["currentCostume"], t["volume"], t["layerOrder"], t["visible"], t["x"], t["y"], t["size"], t["direction"], t["draggable"], t["rotationStyle"])
    blocks = t["blocks"]
    for b in [blocks[nb] for nb in blocks if blocks[nb]["topLevel"]]:
        curTopBlock = sb3TopBlock(b["opcode"], b["next"], b["inputs"], b["fields"], b["shadow"], b["x"], b["y"])
        #TODO: fix inputs, fields
        curBlock = curTopBlock
        while not curBlock.next == None:
            cB = blocks[curBlock.next]
            curBlock = sb3Block(cB["opcode"], cB["next"], cB["inputs"], cB["fields"], cB["shadow"])
            #TODO: fix inputs, fields
            curTopBlock.children.append(curBlock)
        curObject.blocks.append(curTopBlock)
    for c in t["costumes"]:
        curCostume = sb3Costume(c["assetId"], c["name"], c["bitmapResolution"], c["md5ext"], c["dataFormat"], c["rotationCenterX"], c["rotationCenterY"])
        curObject.costumes.append(curCostume)
    for s in t["sounds"]:
        curSound = sb3Sound(s["assetId"], s["name"], s["dataFormat"], s["format"], s["rate"], s["sampleCount"], s["md5ext"])
        curObject.sounds.append(curSound)
    if t["isStage"]:
        if not curStage == None:
            project.stages.append(curStage)
        curStage = curObject
    else:
        curStage.children.append(curObject)
project.stages.append(curStage)
#open("project.json", "w").write(convert3to2json(project))
sb2json = convert3to2json(project)
with zipfile.ZipFile("test_out.sb2", "w") as sb2: #zipfile.ZipFile(sb3fn.replace(".sb3", "_out.sb2"), "w") as sb2:
    sb2.comment = sb3.comment
    sb2.writestr("project.json", sb2json)
    for sf in sb3soundsmd5:
        sb2.writestr(f"{getSoundIDmd5(sf)}.{sf.split('.')[len(sf.split('.'))-1]}", sb3.read(sf))
    for c in sb3costumesmd5:
        sb2.writestr(f"{getCostumeIDmd5(c)}.{c.split('.')[len(c.split('.'))-1]}", sb3.read(c))
'''for s in project.stages:
    print(s.name)
    print("  blocks:")
    for b in s.blocks:
        print("    " + b.opcode)
        for cB in b.children:
            print("      " + cB.opcode)
    print("  costumes:")
    for c in s.costumes:
        print("    " + c.name)
    print("  sounds:")
    for snd in s.sounds:
        print("    " + snd.name)
    print("  objects:")
    for o in s.children:
        print("    " + o.name)
        print("      blocks:")
        for b in o.blocks:
            print("        " + b.opcode)
            for cB in b.children:
                print("          " + cB.opcode)
        print("      costumes:")
        for c in o.costumes:
            print("        " + c.name)
        print("      sounds:")
        for snd in o.sounds:
            print("        " + snd.name)
'''
