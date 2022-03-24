import maya.cmds as cmds

#Constants
#Objects
GROUP = "grp"
GUIDE = "guide"
JAW = "jaw"
JOINT = "jnt"

#Sides
LEFT = "L"
RIGHT = "R"
CENTER = "C"
UPPER = "upper"
LOWER = "lower"


def addOffset(destinationObject, suffix = "OFF"):
    offsetGroup = cmds.createNode("transform", name = "{}_{}".format(destinationObject, suffix))
    cmds.select(cl=True)
    destinationPosition = cmds.xform(destinationObject, q = True, m = True, ws = True)
    cmds.xform(offsetGroup, m = destinationPosition, ws = True)
    cmds.select(cl=True)
    destinationParent = cmds.listRelatives(destinationObject, parent = True)
    if destinationParent:
        cmds.parent(offsetGroup, destinationParent)
        cmds.select(cl=True)
    cmds.parent(destinationObject, offsetGroup)

    cmds.select(cl=True)
    return offsetGroup

def CreateGuides(count = 5):
    jawGuideGroup = cmds.createNode("transform", name = "{}_{}_{}_{}".format(CENTER,JAW,GUIDE,GROUP))
    locatorGroup = cmds.createNode("transform", name="{}_lip_{}_{}".format(CENTER, GUIDE, GROUP), parent = jawGuideGroup)
    lipsLocatorGroup = cmds.createNode("transform", name="{}_lipMinor_{}_{}".format(CENTER, GUIDE, GROUP),parent = locatorGroup)

    for part in [UPPER, LOWER]:

        part_mult = 1 if part == UPPER else -1
        mid_data = (0, part_mult,0)

        mid_loc = cmds.spaceLocator(name = "{}_{}_{}_lip_{}".format(CENTER, JAW,part ,GUIDE))[0]
        cmds.parent(mid_loc, lipsLocatorGroup)

        for side in [LEFT, RIGHT]:
            for x in range(count):
                mult = x+1 if side == LEFT else -(x+1)
                locatorData = (mult, part_mult, 0)
                locator = cmds.spaceLocator(name = "{}_{}_{}_lip_{:02d}_{}".format(side,JAW,part,x+1, GUIDE))[0]
                cmds.parent(locator, lipsLocatorGroup)

                #set side locator position
                cmds.setAttr("{}.t".format(locator), *locatorData)

            # set center locator position
        cmds.setAttr("{}.t".format(mid_loc),*mid_data)

        # Set the corner locator position
    leftCornerLocator = cmds.spaceLocator(name = "{}_{}_corner_lip_{}".format(LEFT,JAW, GUIDE))[0]
    rightCornerLocator = cmds.spaceLocator(name = "{}_{}_corner_lip_{}".format(RIGHT,JAW, GUIDE))[0]

    cmds.parent(leftCornerLocator, lipsLocatorGroup)
    cmds.parent(rightCornerLocator, lipsLocatorGroup)

    cmds.setAttr("{}.t".format(leftCornerLocator), *(count + 1, 0, 0))
    cmds.setAttr("{}.t".format(rightCornerLocator), *(-(count + 1), 0, 0))

    cmds.select(cl = True)

    #create jaw base
    jawBaseGuideGrp = cmds.createNode("transform", name = "{}_{}_base_{}_{}".format(CENTER, JAW,GUIDE, GROUP),
                                      parent = jawGuideGroup)
    jawGuide = cmds.spaceLocator(name = "{}_{}_{}".format(CENTER, JAW, GUIDE))[0]
    jawInverseGuide = cmds.spaceLocator(name = "{}_{}_Inverse_{}".format(CENTER, JAW, GUIDE))[0]

    cmds.setAttr("{}.t".format(jawGuide), *(0, -1, -count))
    cmds.setAttr("{}.t".format(jawInverseGuide), *(0, 1, -count))

    cmds.parent(jawGuide, jawBaseGuideGrp)
    cmds.parent(jawInverseGuide, jawBaseGuideGrp)

    cmds.select(cl=True)


def GetLipGuides():
    lipMinorGrp = "{}_lipMinor_{}_{}".format(CENTER, GUIDE, GROUP)
    return [loc for loc in cmds.listRelatives(lipMinorGrp) if cmds.objExists(lipMinorGrp)]
def GetBaseGuides():
    baseGuideGrp = "{}_{}_base_{}_{}".format(CENTER, JAW,GUIDE, GROUP)
    return [loc for loc in cmds.listRelatives(baseGuideGrp) if cmds.objExists(baseGuideGrp)]

def CreateHeirarchy():
    mainGroup = cmds.createNode("transform", name = "{}_{}_rig_{}".format(CENTER, JAW, GROUP))
    lipGroup = cmds.createNode("transform", name="{}_{}_lip_{}".format(CENTER, JAW, GROUP), parent = mainGroup)
    baseGroup = cmds.createNode("transform", name="{}_{}_base_{}".format(CENTER, JAW, GROUP), parent = mainGroup)

    lipMinorGroup = cmds.createNode("transform", name="{}_{}_lip_minor_{}".format(CENTER, JAW, GROUP), parent=lipGroup)
    lipBroadGroup = cmds.createNode("transform", name="{}_{}_lip_broad_{}".format(CENTER, JAW, GROUP), parent=lipGroup)

    cmds.select(cl = True)



def CreateMinorJoints():
    minorJoints = list()

    for guide in GetLipGuides():
        pos = cmds.xform(guide, q = True, m = True, ws =True)
        joints = cmds.joint(name = guide.replace(GUIDE,JOINT))
        cmds.setAttr("{}.radius".format(joints), 0.5)
        cmds.xform(joints, m = pos, ws = True)

        #parent joints
        cmds.parent(joints,"{}_{}_lip_minor_{}".format(CENTER, JAW, GROUP) )
        minorJoints.append(joints)

        cmds.select(cl = True)

    return minorJoints

def CreateBroadJoints():
    upperJoint = cmds.joint(name = "{}_{}_broadUpper_{}".format(CENTER, JAW , JOINT))
    cmds.select(cl = True)
    lowerJoint = cmds.joint(name="{}_{}_broadLower_{}".format(CENTER, JAW, JOINT))
    cmds.select(cl=True)
    leftJoint = cmds.joint(name="{}_{}_broadCorner_{}".format(LEFT, JAW, JOINT))
    cmds.select(cl=True)
    rightJoint = cmds.joint(name="{}_{}_broadCorner_{}".format(RIGHT, JAW, JOINT))

    cmds.parent([upperJoint, lowerJoint, leftJoint, rightJoint], "{}_{}_lip_broad_{}".format(CENTER, JAW, GROUP))

    #get Guide Position
    upperPos = cmds.xform("{}_{}_upper_lip_{}".format(CENTER, JAW, GUIDE), q = True, m = True, ws = True)
    lowerPos = cmds.xform("{}_{}_lower_lip_{}".format(CENTER, JAW, GUIDE), q=True,m = True, ws=True)
    leftPos = cmds.xform("{}_{}_corner_lip_{}".format(LEFT, JAW, GUIDE), q=True,m = True, ws=True)
    rightPos = cmds.xform("{}_{}_corner_lip_{}".format(RIGHT, JAW, GUIDE), q=True,m = True, ws=True)

    #set guides positions
    cmds.xform(upperJoint, m = upperPos)
    cmds.xform(lowerJoint, m=lowerPos)
    cmds.xform(leftJoint, m=leftPos)
    cmds.xform(rightJoint, m=rightPos)

    #set scale to 1
    cmds.scale(1,1,1, [upperJoint,lowerJoint,leftJoint,rightJoint])

    cmds.select(cl = True)

def CreateJawBase():
    jawJoint = cmds.joint(name = "{}_{}_{}".format(CENTER,JAW,JOINT))
    jawInverseJoint = cmds.joint(name = "{}_inverse_{}_{}".format(CENTER, JAW, JOINT))

    jawPos = cmds.xform(GetBaseGuides()[0], q = True, m = True, ws = True)
    jawInversePos = cmds.xform(GetBaseGuides()[1], q = True, m = True, ws = True)

    cmds.xform(jawJoint, m = jawPos, ws = True)
    cmds.xform(jawInverseJoint, m = jawInversePos, ws = True)

    cmds.parent(jawJoint, "{}_{}_base_{}".format(CENTER, JAW, GROUP))
    cmds.parent(jawInverseJoint, "{}_{}_base_{}".format(CENTER, JAW, GROUP))

    cmds.select(cl = True)

    addOffset(jawJoint, suffix="OFF")
    addOffset(jawInverseJoint, suffix="OFF")

    addOffset(jawJoint, suffix="AUTO")
    addOffset(jawInverseJoint, suffix="AUTO")

    cmds.select(cl=True)

def buildJoints():
    CreateHeirarchy()
    CreateMinorJoints()
    CreateBroadJoints()
    CreateJawBase()
    CreateSeal("lower")
    CreateSeal("upper")
    ConstraintBroadJoints()
    CreateJawAttr()
    CreateConstraints()
    CreateInitialValues("upper")
    CreateInitialValues("lower")
    CreatOffsetFollow()
    CreateSealAttr("upper")
    CreateSealAttr("lower")
    CreateJawPin()


def ConstraintBroadJoints():
    jawJoint = "{}_{}_{}".format(CENTER, JAW, JOINT)
    inverseJawJoint =  "{}_inverse_{}_{}".format(CENTER, JAW, JOINT)

    broadUpper = "{}_{}_broadUpper_{}".format(CENTER, JAW, JOINT)
    broadlower = "{}_{}_broadLower_{}".format(CENTER, JAW, JOINT)
    broadLeft = "{}_{}_broadCorner_{}".format(LEFT, JAW, JOINT)
    broadRight = "{}_{}_broadCorner_{}".format(RIGHT, JAW, JOINT)

    #add offset to broad joints
    upperOffset = addOffset(broadUpper)
    lowerOffset = addOffset(broadlower)
    leftOffset = addOffset(broadLeft)
    rightOffset = addOffset(broadRight)


    #adding constraint to upper and lower
    cmds.parentConstraint(jawJoint, lowerOffset, mo = True)
    cmds.parentConstraint(inverseJawJoint, upperOffset, mo=True)

    #adding constraint to corners
    cmds.parentConstraint(upperOffset,lowerOffset, leftOffset, mo = True)
    cmds.parentConstraint(upperOffset,lowerOffset, rightOffset, mo=True)

    cmds.select(cl = True)

def GetLipParts():
    upperToken = "jaw_upper"
    lowerToken = "jaw_lower"
    cornerToken = "jaw_corner"

    cUpper = "{}_{}_broadUpper_{}".format(CENTER, JAW, JOINT)
    cLower = "{}_{}_broadLower_{}".format(CENTER, JAW, JOINT)
    lCorner = "{}_{}_broadCorner_{}".format(LEFT, JAW, JOINT)
    rCorner = "{}_{}_broadCorner_{}".format(RIGHT, JAW, JOINT)

    lipJoints = cmds.listRelatives("{}_{}_lip_{}".format(CENTER, JAW,GROUP), allDescendents =True)

    lookUp = {"C_upper" :{}, "C_lower" :{},
              "L_upper" :{}, "L_lower" :{},
              "R_upper": {}, "R_lower": {},
              "L_corner" :{}, "R_corner" :{}}

    for joint in lipJoints:

        if cmds.objectType(joint) != "joint":
            continue
        if joint.startswith("C") and upperToken in joint:
            lookUp["C_upper"][joint] = [cUpper]
        if joint.startswith("C") and lowerToken in joint:
            lookUp["C_lower"][joint] = [cLower]
        if joint.startswith("L") and upperToken in joint:
            lookUp["L_upper"][joint] = [cUpper,lCorner]
        if joint.startswith("L") and lowerToken in joint:
            lookUp["L_lower"][joint] = [cLower,lCorner]

        if joint.startswith("R") and upperToken in joint:
            lookUp["R_upper"][joint] = [cUpper,rCorner]
        if joint.startswith("R") and lowerToken in joint:
            lookUp["R_lower"][joint] = [cLower,rCorner]

        if joint.startswith("L") and cornerToken in joint:
            lookUp["L_corner"][joint] = [lCorner]
        if joint.startswith("R") and cornerToken in joint:
            lookUp["R_corner"][joint] = [rCorner]

    return lookUp

def LipParts(part):
    lipParts = [reversed(sorted(GetLipParts()["L_{}".format(part)].keys())), GetLipParts()["C_{}".format(part)].keys(),
                sorted(GetLipParts()["R_{}".format(part)].keys())]

    return [joint for joint in lipParts for joint in joint]


def CreateSeal(part):
    sealName = "{}_seal_{}".format(CENTER, GROUP)
    sealParent = sealName if cmds.objExists(sealName) else cmds.createNode("transform", name =sealName, parent =
                                                                           "{}_{}_rig_{}".format(CENTER, JAW, GROUP))


    partGrp = cmds.createNode("transform", name = sealName.replace("seal", "seal_{}".format(part)), parent = sealParent)

    lCorner = "{}_{}_broadCorner_{}".format(LEFT, JAW, JOINT)
    rCorner = "{}_{}_broadCorner_{}".format(RIGHT, JAW, JOINT)

    value = len(LipParts(part))

    for index, joint in enumerate(LipParts(part)):
        node = cmds.createNode("transform", name = joint.replace("jnt", "{}_SEAL".format(part)), parent = partGrp)
        pos = cmds.xform(joint, q = True, m = True, ws = True)
        cmds.xform(node, m = pos, ws = True)

        constraint = cmds.parentConstraint(lCorner, rCorner, node, mo = True)[0]
        cmds.setAttr("{}.interpType".format(constraint), 2)

        rCornerValue = float(index)/ float(value-1)
        lCornerValue = 1 - rCornerValue

        lCornerAttr = "{}.{}W0".format(constraint, lCorner)
        rCornerAttr = "{}.{}W1".format(constraint, rCorner)

        cmds.setAttr(lCornerAttr, lCornerValue)
        cmds.setAttr(rCornerAttr, rCornerValue)

    cmds.select()


def CreateJawAttr():
    node = cmds.createNode("transform", name = "jaw_attributes", parent = "{}_{}_rig_{}".format(CENTER, JAW, GROUP))
    cmds.addAttr(node, ln = sorted(GetLipParts()["C_upper"].keys())[0], min = 0, max = 1, dv = 0)
    cmds.setAttr("{}.{}".format(node, sorted(GetLipParts()["C_upper"].keys())[0]), lock = 1)

    for upper in sorted(GetLipParts()["L_upper"].keys()):
        cmds.addAttr(node, ln = upper, min = 0, max = 1, dv = 0)

    cmds.addAttr(node, ln = sorted(GetLipParts()["L_corner"].keys())[0], min = 0, max = 1, dv = 0)
    cmds.setAttr("{}.{}".format(node, sorted(GetLipParts()["L_corner"].keys())[0]), lock=1)

    for lower in reversed(sorted(GetLipParts()["L_lower"].keys())):
        cmds.addAttr(node, ln=lower, min=0, max=1, dv=0)

def CreateConstraints():
    for value in GetLipParts().values():
        for lipJoint, broadJoint, in value.items():
            sealToken = "upper_SEAL" if "upper" in lipJoint else "lower_SEAL"
            lipSeal = lipJoint.replace(JOINT,sealToken)

            if not cmds.objExists(lipSeal):
                constraint = cmds.parentConstraint(broadJoint, lipJoint, mo=True)[0]
                cmds.setAttr("{}.interpType".format(constraint), 2)
                continue
            constraint = cmds.parentConstraint(broadJoint, lipSeal, lipJoint, mo = True)[0]
            cmds.setAttr("{}.interpType".format(constraint), 2)

            if len(broadJoint) == 1:
                sealAttr = "{}_parentConstraint1.{}W1".format(lipJoint, lipSeal)
                rev = cmds.createNode("reverse", name = lipJoint.replace(JOINT, "REV"))
                cmds.connectAttr(sealAttr, "{}.inputX".format(rev))
                cmds.connectAttr("{}.outputX".format(rev), "{}_parentConstraint1.{}W0".format(lipJoint, broadJoint[0]))
                cmds.setAttr(sealAttr, 0)

            if len(broadJoint) == 2:
                sealAttr = "{}_parentConstraint1.{}W2".format(lipJoint, lipSeal)
                cmds.setAttr(sealAttr, 0)

                sealRev = cmds.createNode("reverse", name = lipJoint.replace("jnt", "seal_REV"))
                jawAttrRev = cmds.createNode("reverse", name=lipJoint.replace("jnt", "jaw_attr_REV"))
                sealMult = cmds.createNode("multiplyDivide", name=lipJoint.replace("jnt", "seal_MULT"))

                cmds.connectAttr(sealAttr, "{}.inputX".format(sealRev))
                cmds.connectAttr("{}.outputX".format(sealRev), "{}.input2X".format(sealMult))
                cmds.connectAttr("{}.outputX".format(sealRev), "{}.input2Y".format(sealMult))

                cmds.connectAttr("jaw_attributes.{}".format(lipJoint.replace(lipJoint[0], "L")), "{}.input1Y".format(sealMult))
                cmds.connectAttr("jaw_attributes.{}".format(lipJoint.replace(lipJoint[0], "L")), "{}.inputX".format(jawAttrRev))

                cmds.connectAttr("{}.outputX".format(jawAttrRev), "{}.input1X".format(sealMult))

                cmds.connectAttr("{}.outputX".format(sealMult), "{}_parentConstraint1.{}W0".format(lipJoint, broadJoint[0]))
                cmds.connectAttr("{}.outputY".format(sealMult), "{}_parentConstraint1.{}W1".format(lipJoint, broadJoint[1]))


def CreateInitialValues(part, smoothvalue = 1.3):
    jawAttr = [part for part in LipParts(part) if not part.startswith("C") and not part.startswith("R")]
    value = len(jawAttr)

    for index, attrName in enumerate(jawAttr[::-1]):
        attr = "jaw_attributes.{}".format(attrName)

        linearValue = float(index)/float(value - 1)
        divValue = linearValue/smoothvalue
        final = divValue*linearValue
        cmds.setAttr(attr, final)


def CreatOffsetFollow():
    jawAttr = "jaw_attributes"

    jawJoint = "{}_{}_{}".format(CENTER, JAW, JOINT)
    jawAutoJoint = "{}_{}_{}_AUTO".format(CENTER, JAW, JOINT)

    #add follow attribues
    cmds.addAttr(jawAttr, ln = "follow_ty", min = -10, max = 10, dv = 0)
    cmds.addAttr(jawAttr, ln="follow_tz", min=-10, max=10, dv=0)
    cmds.addAttr(jawAttr, ln="{}_seal".format("L"), min=0, max=10, dv=0)
    cmds.addAttr(jawAttr, ln="{}_seal".format("R"), min=0, max=10, dv=0)
    cmds.addAttr(jawAttr, ln="{}_seal_delay".format("L"), min=0, max=10, dv=0)
    cmds.addAttr(jawAttr, ln="{}_seal_delay".format("R"), min=0, max=10, dv=0)

    unit = cmds.createNode("unitConversion", name = "{}_{}_follow_UNIT".format(CENTER,JAW))

    remapY = cmds.createNode("remapValue", name = "{}_{}_followY_REMAP".format(CENTER, JAW))
    cmds.setAttr("{}.inputMax".format(remapY), 1)

    remapZ = cmds.createNode("remapValue", name="{}_{}_followZ_REMAP".format(CENTER, JAW))
    cmds.setAttr("{}.inputMax".format(remapZ), 1)

    multY = cmds.createNode("multDoubleLinear", name = "{}_{}_followY_MULT".format(CENTER, JAW))
    cmds.setAttr("{}.input2".format(multY), -1)

    cmds.connectAttr("{}.rx".format(jawJoint), "{}.input".format(unit))
    cmds.connectAttr("{}.output".format(unit), "{}.inputValue".format(remapY))
    cmds.connectAttr("{}.output".format(unit), "{}.inputValue".format(remapZ))

    cmds.connectAttr("{}.follow_ty".format(jawAttr), "{}.input1".format(multY))
    cmds.connectAttr("{}.follow_tz".format(jawAttr), "{}.inputMax".format(remapZ))
    cmds.connectAttr("{}.output".format(multY), "{}.inputMax".format(remapY))

    cmds.connectAttr("{}.outValue".format(remapY), "{}.ty".format(jawAutoJoint))
    cmds.connectAttr("{}.outValue".format(remapZ), "{}.tz".format(jawAutoJoint))


def CreateSealAttr(part):
    sealToken = "seal_{}".format(part)

    jawAttr = "jaw_attributes"

    lipJoints = LipParts(part)
    value = len(lipJoints)
    sealDriver = cmds.createNode("lightInfo", name = "C_{}_DRV".format(sealToken))

    triggers = {"L" :list(), "R" : list()}
    for side in "LR":
        delaySubName = "{}_{}_delay_SUB".format(side, sealToken)
        delaySub = cmds.createNode("plusMinusAverage", name = delaySubName)
        cmds.setAttr("{}.operation".format(delaySub), 2)
        cmds.setAttr("{}.input1D[0]".format(delaySub), 10)

        cmds.connectAttr("{}.{}_seal_delay".format(jawAttr, side), "{}.input1D[1]".format(delaySub))

        lerp = 1/float(value-1)
        delayDivName = "{}_{}_delay_DIV".format(side,sealToken)
        delayDiv = cmds.createNode("multDoubleLinear", name = delayDivName)
        cmds.setAttr("{}.input2".format(delayDiv), lerp)
        cmds.connectAttr("{}.output1D".format(delaySub), "{}.input1".format(delayDiv))

        multTriggers = list()
        subTriggers = list()
        triggers[side].append(multTriggers)
        triggers[side].append(subTriggers)

        for index in range(value):
            indexName = "jaw_{:02d}".format(index)

            delayMultName = "{}_{}_{}_delay_MULT".format(indexName, side, sealToken)
            delayMult = cmds.createNode("multDoubleLinear", name = delayMultName)
            cmds.setAttr("{}.input1".format(delayMult), index)
            cmds.connectAttr("{}.output".format(delayDiv), "{}.input2".format(delayMult))

            multTriggers.append(delayMult)

            delaySubName = "{}_{}_{}_delay_MULT".format(indexName, side, sealToken)
            delaySub = cmds.createNode("plusMinusAverage", name=delaySubName)
            cmds.connectAttr("{}.output".format(delayMult), "{}.input1D[0]".format(delaySub))
            cmds.connectAttr("{}.{}_seal_delay".format(jawAttr, side), "{}.input1D[1]".format(delaySub))

            subTriggers.append(delaySub)

    constTargets = list()

    for jnt in lipJoints:
        attrs = cmds.listAttr("{}_parentConstraint1".format(jnt), ud =True)
        for attr in attrs:
            if "SEAL" in attr:
                constTargets.append("{}_parentConstraint1.{}".format(jnt,attr))

    for leftIndex, constTarget in enumerate(constTargets):
        rightIndex = value - leftIndex -1
        indexName = "{}_{}".format(sealToken, leftIndex)

        lMultTrigger, lSubTrigger = triggers["L"][0][leftIndex], triggers["L"][1][leftIndex]
        rMultTrigger, rSubTrigger = triggers["R"][0][rightIndex], triggers["R"][1][rightIndex]

        #left
        lRemapName = "L_{}_{}_REMAP".format(sealToken, indexName)
        lRemap = cmds.createNode("remapValue", name = lRemapName)
        cmds.setAttr("{}.outputMax".format(lRemap),1)
        cmds.setAttr("{}.value[0].value_Interp".format(lRemap), 2)

        cmds.connectAttr("{}.output".format(lMultTrigger), "{}.inputMin".format(lRemap))
        cmds.connectAttr("{}.output1D".format(lSubTrigger), "{}.inputMax".format(lRemap))

        cmds.connectAttr("{}.L_seal".format(jawAttr), "{}.inputValue".format(lRemap))

        #right
        rSubName = "R_{}_offset_{}_SUB".format(sealToken, indexName)
        rSub = cmds.createNode("plusMinusAverage", name = rSubName)
        cmds.setAttr("{}.input1D[0]".format(rSub), 1)
        cmds.setAttr("{}.operation".format(rSub), 2)

        cmds.connectAttr("{}.outValue".format(lRemap), "{}.input1D[1]".format(rSub))

        rRemapName = "R_{}_{}_REMAP".format(sealToken, indexName)
        rRemap = cmds.createNode("remapValue", name=rRemapName)
        cmds.setAttr("{}.outputMax".format(rRemap), 1)
        cmds.setAttr("{}.value[0].value_Interp".format(rRemap), 2)

        cmds.connectAttr("{}.output".format(rMultTrigger), "{}.inputMin".format(rRemap))
        cmds.connectAttr("{}.output1D".format(rSubTrigger), "{}.inputMax".format(rRemap))

        #connect left seal attribute to input of remap
        cmds.connectAttr("{}.R_seal".format(jawAttr), "{}.inputValue".format(rRemap))

        cmds.connectAttr("{}.output1D".format(rSub), "{}.outputMax".format(rRemap))

        #final addition of both sides
        plusName = "{}_SUM".format(indexName)
        plus = cmds.createNode("plusMinusAverage", name =plusName)

        cmds.connectAttr("{}.outValue".format(lRemap), "{}.input1D[0]".format(plus))
        cmds.connectAttr("{}.outValue".format(rRemap), "{}.input1D[1]".format(plus))

        clampName = "{}_CLAMP".format(indexName)
        clamp = cmds.createNode("remapValue", name = clampName)
        cmds.connectAttr("{}.output1D".format(plus), "{}.inputValue".format(clamp))

        cmds.addAttr(sealDriver, at = "double", ln = indexName, min = 0, max = 1, dv = 0)
        cmds.connectAttr("{}.outValue".format(clamp), "{}.{}".format(sealDriver, indexName))

        cmds.connectAttr("{}.{}".format(sealDriver, indexName), constTarget)


def CreateJawPin():
    pinDriver = cmds.createNode("lightInfo", name = "{}_pin_DRV".format(CENTER))
    jawAttr = "jaw_attributes"
    for side in "LR":


        cmds.addAttr(jawAttr, at = "bool", ln = "{}_auto_corner_pin".format(side))
        cmds.addAttr(jawAttr, at = "double", ln = "{}_corner_pin".format(side), min = -10, max = 10, dv = 0)
        cmds.addAttr(jawAttr, at="double", ln="{}_input_ty".format(side), min=-10, max=10, dv=0)

        #create clamp and connect the input ty to it
        clamp = cmds.createNode("clamp", name = "{}_corner_pin_auto_CLAMP".format(side))
        cmds.setAttr("{}.minR".format(clamp), -10)
        cmds.setAttr("{}.maxR".format(clamp), 10)

        cmds.connectAttr("{}.{}_input_ty".format(jawAttr, side), "{}.inputR".format(clamp))

        # Create condition for the two possible scenerios
        cnd = cmds.createNode("condition", name = "{}_corner_pin_auto_CND".format(side))
        cmds.setAttr("{}.operation". format(cnd), 0)
        cmds.setAttr("{}.secondTerm".format(cnd), 1)

        cmds.connectAttr("{}.{}_auto_corner_pin".format(jawAttr, side), "{}.firstTerm".format(cnd))
        cmds.connectAttr("{}.outputR".format(clamp), "{}.colorIfTrueR".format(cnd))
        cmds.connectAttr("{}.{}_corner_pin".format(jawAttr, side), "{}.colorIfFalseR".format(cnd))

        # Create addition
        plus = cmds.createNode("plusMinusAverage", name = "{}_corner_pin_PLUS".format(side))
        cmds.setAttr("{}.input1D[1]".format(plus), 10)
        cmds.connectAttr("{}.outColorR".format(cnd), "{}.input1D[0]".format(plus))

        # Create division
        div = cmds.createNode("multDoubleLinear", name = "{}_corner_pin_DIV".format(side))
        cmds.setAttr("{}.input2".format(div), 0.05)
        cmds.connectAttr("{}.output1D".format(plus), "{}.input1".format(div))

        # Add final output attributes to the driver node
        cmds.addAttr(pinDriver, at = "double", ln = "{}_pin".format(side), min = 0, max = 1, dv = 0)
        cmds.connectAttr("{}.output".format(div), "{}.{}_pin".format(pinDriver, side))

        # Connect driver to broad joint constraint targets
        constPinUp = "{}_jaw_broadCorner_jnt_OFF_parentConstraint1.C_jaw_broadUpper_jnt_OFFW0".format(side)
        constPinDown = "{}_jaw_broadCorner_jnt_OFF_parentConstraint1.C_jaw_broadLower_jnt_OFFW1".format(side)

        cmds.connectAttr("{}.{}_pin".format(pinDriver, side), constPinUp)

        rev = cmds.createNode("reverse", name = "{}_corner_pin_REV".format(side))
        cmds.connectAttr("{}.{}_pin".format(pinDriver, side), "{}.inputX".format(rev))
        cmds.connectAttr("{}.outputX".format(rev), constPinDown)










#CreateGuides(8)
buildJoints()
#
#print(GetLipParts())
#CreateConstraints()
#CreateSealAttr("upper")
