import json, zipfile
from tkinter.filedialog import askopenfilename

sb3to2translations = [
    ["motion_movesteps", "forward:"],
    ["motion_turnright", "turnRight:"],
    ["motion_turnleft", "turnLeft:"],
    ["motion_pointindirection", "heading:"],
    ["motion_pointtowards", "pointTowards:"],
    ["motion_gotoxy", "gotoX:y:"],
    ["motion_goto", "gotoSpriteOrMouse:"],
    ["motion_glidesecstoxy", "glideSecs:toX:y:elapsed:from:"],
    ["motion_changexby", "changeXposBy:"],
    ["motion_setx", "xpos:"],
    ["motion_changeyby", "changeYposBy:"],
    ["motion_sety", "ypos:"],
    ["motion_ifonedgebounce", "bounceOffEdge"],
    ["motion_setrotationstyle", "setRotationStyle"],
    ["control_wait", "wait:elapsed:from:"],
    ["control_repeat", "doRepeat"],
    ["control_if", "doIf"],
    ["control_if_else", "doIfElse"],
    ["control_stop", "stopScripts"],
    ["control_wait_until", "doWaitUntil"],
    ["control_repeat_until", "doUntil"],
    ["control_forever", "doForever"],
    ["control_start_as_clone", "whenCloned"],
    ["control_create_clone_of", "createCloneOf"],
    ["control_delete_this_clone", "deleteClone"],
    ["event_whenflagclicked", "whenGreenFlag"],
    ["event_whenkeypressed", "whenKeyPressed"],
    ["event_whenthisspriteclicked", "whenClicked"],
    ["event_whenbackdropswitchesto", "whenSceneStarts"],
    ["event_whengreaterthan", "whenSensorGreaterThan"],
    ["event_whenbroadcastreceived", "whenIReceive"],
    ["event_broadcast", "broadcast:"],
    ["event_broadcastandwait", "doBroadcastAndWait"],
    ["operator_equals", "="],
    ["operator_lt", "<"],
    ["operator_gt", ">"],
    ["looks_sayforsecs", "say:duration:elapsed:from:"],
    ["looks_say", "say:"],
    ["looks_thinkforsecs", "think:duration:elapsed:from:"],
    ["looks_think", "think:"],
    ["looks_show", "show"],
    ["looks_hide", "hide"],
    ["looks_switchcostumeto", "lookLike:"],
    ["looks_nextcostume", "nextCostume"],
    ["looks_switchbackdropto", "startScene"],
    ["looks_changeeffectby", "changeGraphicEffect:by:"],
    ["looks_seteffectto", "setGraphicEffect:to:"],
    ["looks_cleargraphiceffects", "filterReset"],
    ["looks_changesizeby", "changeSizeBy:"],
    ["looks_setsizeto", "setSizeTo:"],
    ["looks_gotofrontback", "comeToFront"],
    ["looks_goforwardbackwardlayers", "goBackByLayers:"],
    ["looks_costumenumbername", "costumeIndex"],
    ["looks_backdropnumbername", "sceneName"],
    ["looks_size", "scale"],
    ["sound_play", "playSound:"],
    ["sound_playuntildone", "doPlaySoundAndWait"],
    ["sound_stopallsounds", "stopAllSounds"],
    ["sound_changevolumeby", "changeVolumeBy:"],
    ["sound_setvolumeto", "setVolumeTo:"],
    ["sound_volume", "volume"],
    ["music_playDrumForBeats", "playDrum"],
    ["music_restForBeats", "rest:elapsed:from:"],
    ["music_playNoteForBeats", "noteOn:duration:elapsed:from:"],
    ["music_setInstrument", "instrument:"],
    ["music_changeTempo", "changeTempoBy:"],
    ["music_setTempo", "setTempoTo:"],
    ["music_getTempo", "tempo"],
    ["pen_clear", "clearPenTrails"],
    ["pen_stamp", "stampCostume"],
    ["pen_penDown", "putPenDown"],
    ["pen_penUp", "putPenUp"],
    ["pen_setPenColorToColor", "penColor:"],
    ["pen_changePenHueBy", "changePenHueBy:"],
    ["pen_setPenHueToNumber", "setPenHueTo:"],
    ["pen_changePenShadeBy", "changePenShadeBy:"],
    ["pen_setPenShadeToNumber", "setPenShadeTo:"],
    ["pen_changePenSizeBy", "changePenSizeBy:"],
    ["pen_setPenSizeTo", "penSize:"],
    ["sensing_answer", "answer"],
    ["sensing_resettimer", "timerReset"],
    ["sensing_touchingobject", "touching:"],
    ["sensing_touchingcolor", "touchingColor:"],
    ["sensing_mousex", "mouseX"],
    ["sensing_coloristouchingcolor", "color:sees:"],
    ["sensing_mousey", "mouseY"],
    ["sensing_loudness", "soundLevel"],
    ["sensing_keypressed", "keyPressed:"],
    ["sensing_mousedown", "mousePressed"],
    ["sensing_current", "timeAndDate"],
    ["sensing_dayssince2000", "timestamp"],
    ["sensing_username", "getUserName"],
    ["sensing_timer", "timer"],
    ["sensing_askandwait", "doAsk"],
    ["videoSensing_videoToggle", "setVideoState"],
    ["videoSensing_setVideoTransparency", "setVideoTransparency"],
    ["videoSensing_videoOn", "senseVideoMotion"],
    ["all around", "normal"]
] #TODO: add remaining blocks, rotation styles, etc.

sb3sounds = []
sb3soundsmd5 = []
sb3costumes = []
sb3costumesmd5 = []
scriptcount = 0
spritecount = 0

def getSoundID(aID):
    return sb3sounds.index(aID)

def getSoundIDmd5(md5):
    return sb3soundsmd5.index(md5)

def getCostumeID(aID):
    return sb3costumes.index(aID)

def getCostumeIDmd5(md5):
    return sb3costumesmd5.index(md5)

def t3to2(c):
    try:
        return [e[1] for e in sb3to2translations if e[0] == c][0]
    except:
        print("oof, couldn't find " + c)
        return ""

nofieldblocks = [
    "comeToFront",
    "goBackByLayers:",
    "costumeIndex",
    "sceneName"
]

def get2command(b):
    c = t3to2(b.opcode)
    f = [b.fields[f0][0] for f0 in b.fields]
    i = []
    for i0 in b.inputs:
        if type(i0) == str and i0[0] == '#':
            i.append(int(b.inputs[i0].replace("#", ""), 16))
        else:
            i.append(b.inputs[i0])
    tmpoutthing = []
    if not c == "":
        tmpoutthing.append(c)
    if not c in nofieldblocks:
        for f0 in f:
            tmpoutthing.append(f0)
    for i0 in i:
        tmpoutthing.append(i0)
    return tmpoutthing

def get2commandTop(b):
    c = t3to2(b.opcode)
    i = [b.inputs[i0] for i0 in b.inputs]
    f = [b.fields[f0][0] for f0 in b.fields]
    tmpoutthing = [c]
    if not c in nofieldblocks:
        for f0 in f:
            tmpoutthing.append(f0)
    for i0 in i:
        tmpoutthing.append(i0)
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

def getIndexStuff(i, b):
    for ib in i:
        if type(i[ib][1]) == str and i[ib][1] in b:
            cB = b[i[ib][1]]
            curBlock = sb3Block(cB["opcode"], cB["next"], cB["inputs"], cB["fields"], cB["shadow"], b)
            tmpstack = [get2command(curBlock)]
            while not curBlock.next == None:
                cB = b[curBlock.next]
                curBlock = sb3Block(cB["opcode"], cB["next"], cB["inputs"], cB["fields"], cB["shadow"], b)
                tmpstack.append(get2command(curBlock))
            if len(tmpstack) == 1 and not "substack" in ib.lower():
                if type(tmpstack[0]) == list and len(tmpstack[0]) == 1: #TODO: find different condition to check for (I don't wanna create a list with blocks that need this)
                    i[ib] = tmpstack[0][0]
                else:
                    i[ib] = tmpstack[0]
            else:
                i[ib] = tmpstack
        else:
            i[ib] = i[ib][1][1]
    return i

class sb3Block:
    def __init__(self, o, n, i, f, s, b):
        self.opcode = o
        self.next = n
        self.inputs = getIndexStuff(i, b)
        self.fields = f
        self.shadow = s

class sb3TopBlock:
    def __init__(self, o, n, i, f, s, x, y, b):
        self.opcode = o
        self.next = n
        self.inputs = getIndexStuff(i, b)
        self.fields = f
        self.shadow = s
        self.x = x
        self.y = y
        self.children = []

    def getv2(self):
        sb2tb = [get2commandTop(self)]
        for c in self.children:
            sb2tb.append(get2command(c))
        sb2 = [self.x, self.y, sb2tb]
        return sb2

class sb3Project:
    def __init__(self):
        self.stages = []

def convert3to2json(p):
    s = p.stages[0]
    sb2 = {
        "objName": s.name,
        "sounds": [
            {
                "soundName": snd.name,
                "soundID": getSoundID(snd.assetID),
                "md5": snd.md5ext,
                "sampleCount": snd.sampleCount,
                "rate": snd.rate,
                "format": snd.format
            } for snd in s.sounds
        ],
        "costumes": [
            {
                "costumeName": c.name,
                "baseLayerID": getCostumeID(c.assetID),
                "baseLayerMD5": c.md5ext,
                "bitmapResolution": c.bitmapResolution,
                "rotationCenterX": c.rotationCenterX,
                "rotationCenterY": c.rotationCenterY
            } for c in s.costumes
        ],
        "currentCostumeIndex": s.currentCostume,
        "penLayerMD5": "TODO",
        "penLayerID": s.layerOrder,
        "tempoBMP": s.tempo,
        "videoAlpha": s.videoTransparency/100,
        "children": [
            {
                "objName": o.name,
                "scripts": [b.getv2() for b in o.blocks],
                "sounds": [
                    {
                        "soundName": snd.name,
                        "soundID": getSoundID(snd.assetID),
                        "md5": snd.md5ext,
                        "sampleCount": snd.sampleCount,
                        "rate": snd.rate,
                        "format": snd.format
                    } for snd in o.sounds
                ],
                "costumes": [
                    {
                        "costumeName": c.name,
                        "baseLayerID": getCostumeID(c.assetID),
                        "baseLayerMD5": c.md5ext,
                        "bitmapResolution": c.bitmapResolution,
                        "rotationCenterX": c.rotationCenterX,
                        "rotationCenterY": c.rotationCenterY
                    } for c in o.costumes
                ],
                "currentCostumeIndex": o.currentCostume,
                "scratchX": o.x,
                "scratchY": o.y,
                "scale": o.size/100,
                "direction": o.direction,
                "rotationStyle": t3to2(o.rotationStyle),
                "isDraggable": o.draggable,
                "indexInLibrary": o.layerOrder,
                "visible": o.visible,
                "spriteInfo": {}
            } for o in s.children
        ],
        "info": {
            "userAgent": "Scratch 2.0 Offline Editor",
            "flashVersion": "WIN 31,0,0,108",
            "swfVersion": "v461",
            "videoOn": False, #TODO: figure out what this is
            "scriptCount": scriptcount,
            "spriteCount": spritecount
        }
    }
    return json.dumps(sb2, indent=4, sort_keys=True)

curStage = None
sb3fn = askopenfilename(title="Select 3.0 Project...", filetypes=[("Scratch 3.0 Project", "*.sb3")])
sb3 = zipfile.ZipFile(sb3fn, "r")
sb3json = json.loads(sb3.read("project.json"))
#sb3json = json.loads(open(askopenfilename(title="Select 3.0 Project...", filetypes=[("Scratch 3.0 Project", "*.json")]), "r").read())
project = sb3Project()
for t in sb3json["targets"]:
    curObject = None
    if t["isStage"]:
        curObject = sb3Stage(t["name"], t["currentCostume"], t["volume"], t["layerOrder"], t["tempo"], t["videoTransparency"], t["videoState"], t["textToSpeechLanguage"])
    else:
        curObject = sb3Object(t["name"], t["currentCostume"], t["volume"], t["layerOrder"], t["visible"], t["x"], t["y"], t["size"], t["direction"], t["draggable"], t["rotationStyle"])
    blocks = t["blocks"]
    for b in [blocks[nb] for nb in blocks if blocks[nb]["topLevel"]]:
        scriptcount += 1
        curTopBlock = sb3TopBlock(b["opcode"], b["next"], b["inputs"], b["fields"], b["shadow"], b["x"], b["y"], blocks)
        curBlock = curTopBlock
        while not curBlock.next == None:
            cB = blocks[curBlock.next]
            curBlock = sb3Block(cB["opcode"], cB["next"], cB["inputs"], cB["fields"], cB["shadow"], blocks)
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
        spritecount += 1
project.stages.append(curStage)

sb2json = convert3to2json(project)
open("project.json", "w").write(sb2json)
with zipfile.ZipFile("test_out.sb2", "w") as sb2: #zipfile.ZipFile(sb3fn.replace(".sb3", "_out.sb2"), "w") as sb2:
    sb2.comment = sb3.comment
    sb2.writestr("project.json", sb2json)
    for sf in sb3soundsmd5:
        sb2.writestr(f"{getSoundIDmd5(sf)}.{sf.split('.')[len(sf.split('.'))-1]}", sb3.read(sf))
    for c in sb3costumesmd5:
        sb2.writestr(f"{getCostumeIDmd5(c)}.{c.split('.')[len(c.split('.'))-1]}", sb3.read(c))
