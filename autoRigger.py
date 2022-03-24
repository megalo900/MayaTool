import maya.cmds as cmds
newWindow = "Auto Rigger"



def main():
    newWindow = "Auto Rigger"
    if cmds.window(newWindow, exists=True):
        cmds.deleteUI(newWindow)
        print "window already exists"
    else:
        UI()


def UI():
    global spineCnt
    global fingerCnt
    global cBox

    mainWindow = cmds.window(newWindow, title="Auto Rigger", iconName='AutoRigger', widthHeight=(200, 55))

    cmds.scrollLayout("scroll")
    cmds.frameLayout(l="Initial Setup", cll=True)
    cmds.columnLayout()
    cmds.colorSliderGrp(label='Blue', rgb=(0, 0, 1))
    # cmds.text(l="No of Spine Joints")
    # spineCnt = cmds.intSliderGrp(minValue=1, maxValue=10, value=4)
    spineCnt = cmds.intSliderGrp(l="No of Spines", minValue=1, maxValue=10, value=4, step=1, field=True)
    cmds.separator(height=20)

    fingerCnt = cmds.intSliderGrp(l="No of finger Joints", minValue=3, maxValue=5, value=5, step=1, field=True)

    cmds.rowColumnLayout(nc=2)
    cmds.button(label='Create locators', w=200, c="createLocators()")

    cmds.button(l="Delete Locator", w=200, c="deleteLocators()")

    cmds.separator(height=20)
    cmds.separator(height=20)
    cmds.separator(height=20)
    cBox = cmds.checkBox(l="Locator Visibility", cc="check()")
    cmds.separator(height=20)
    cmds.separator(height=20)

    # cmds.button(l = "Create Hand", w= 200, c = "createHandCmd()")
    cmds.button(l="Mirror Locators L - R", w=200, c="mirrorLocators(1)")
    cmds.button(l="Mirror Locators R - L", w=200, c="mirrorLocators(-1)")

    cmds.separator(height=20)
    cmds.separator()

    cmds.setParent('..')
    cmds.setParent('..')
    cmds.setParent('..')

    cmds.frameLayout(l="Joints Setup", cll=True)
    cmds.rowColumnLayout(nc=2)

    cmds.separator(height=20)
    cmds.separator(height=20)
    cmds.button(l="Create Joints", w=200, c="createJoints()")
    cmds.button(l="Delete Joints", w=200, c="deleteJoints()")
    cmds.separator(height=20)
    cmds.separator(height=20)
    cmds.setParent('..')

    cmds.frameLayout(l="Finger Orientation Adjustment", cll=True)
    cmds.rowColumnLayout(nc=2)
    cmds.separator(height=20)
    cmds.separator(height=20)
    cmds.radioCollection()
    cmds.radioButton(l="Thumb only", onc="radioInput(1)", ofc="radioInput(0)")
    cmds.radioButton(l="All", onc="radioInput(0)", ofc="radioInput(1)")
    cmds.separator(height=20)
    cmds.separator(height=20)
    # cmds.button(l="Fix Orientation",w= 200, c="fixOrientation()")
    cmds.button(l="Show Manipulators", w=200, c="makeFingerGizmo(radioOpt)")
    cmds.button(l="Finalize Adjustment", w=200, c="applyOrientationToFinger()")
    cmds.separator(height=20)
    cmds.separator(height=20)
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.frameLayout(l="IK FK Setting", cll=True)
    cmds.rowColumnLayout(nc=2)
    cmds.separator(height=20)
    cmds.separator(height=20)
    cmds.button(l="Heel Locators", w=200, c="makeReverseFootLoc()")
    cmds.button(l="Make Ctrl Rig", w=200, c="makeCtrlRig()")

    cmds.button(l="Make Controls", w=200, c="makeTheControls()")
    cmds.separator(height=20)
    cmds.separator(height=20)



    cmds.setParent('..')
    cmds.setParent('..')

    cmds.frameLayout(l="Eyes and jaw", cll=True)
    cmds.rowColumnLayout(nc=2)
    cmds.button(l="Eyes and Locators", w=200, c="createEyesAndJawLoc()")
    cmds.button(l="Finish", w=200, c="createEyesAndJawJoints()")

    cmds.setParent('..')
    cmds.setParent('..')

    cmds.frameLayout(l="Skinning", cll=True)
    cmds.rowColumnLayout(nc=2)
    cmds.button(l="Bind Skin", w=200, c="skinGeo()")
    cmds.button(l="Clean Up", w=200, c="cleanUp()")



    cmds.showWindow(mainWindow)


main()


def scaleLocator(amount, name):
    cmds.scale(amount, amount, amount, name)


def createLocators():
    global locator

    if cmds.objExists("Loc_MasterGroup"):
        print "object already exist"
    else:
        cmds.group(em=True, n="Loc_MasterGroup")
        root = cmds.sphere(p=(0, 0, 0), n="Root")
        scaleLocator(0.5, root)
        cmds.makeIdentity(apply=True)
        root = cmds.parent(root, "Loc_MasterGroup")
        locator = cmds.sphere(p=(0, 0, 0), n="Cog")
        scaleLocator(0.5, locator)
        locator = cmds.parent(locator, "Root")
        createSpine()
        cmds.move(0, 11, 0, locator)
        visibilityToggle(True)
        cmds.setAttr("lambert1.color",0.5,0,0, type = "double3" )


def createEyesAndJawLoc():
    rootScale = cmds.xform("Root", q = True, s =True)
    cmds.group(em=True, n="EyesAndJaw_Loc_Group")
    cmds.sphere(p=(0, 0, 0), n="L_Eye")
    cmds.move(1,24,4)
    cmds.scale(0.1,0.1,0.1)
    cmds.parent("L_Eye","EyesAndJaw_Loc_Group")

    cmds.sphere(p=(0, 0, 0), n="R_Eye")
    cmds.move(-1,24,4)
    cmds.scale(0.1, 0.1, 0.1)
    cmds.parent("R_Eye", "EyesAndJaw_Loc_Group")

    cmds.sphere(p=(0, 0, 0), n="Jaw")
    cmds.move(0, 22, 2)
    cmds.scale(0.1, 0.1, 0.1)
    cmds.parent("Jaw", "EyesAndJaw_Loc_Group")

    cmds.sphere(p=(0, 0, 0), n="Chin")
    cmds.move(0, 22, 3.5)
    cmds.scale(0.2, 0.2, 0.2)
    cmds.parent("Chin", "EyesAndJaw_Loc_Group")


    cmds.scale(rootScale[0],rootScale[1],rootScale[2],"EyesAndJaw_Loc_Group")


def createEyesAndJawJoints():
    cmds.setAttr("EyesAndJaw_Loc_Group.visibility", False)
    loc = ["L_Eye","R_Eye","Jaw","Chin"]
    orientation = ["xzy", "yzx", "zyx"]
    for i,j in enumerate(loc):
        pos = cmds.xform(j, q = True, t = True, ws =True)
        cmds.joint(n=j+"_Jnt", p = pos)
        cmds.select(cl = True)
    cmds.parent("Chin_Jnt","Jaw_Jnt")
    cmds.joint("Jaw_Jnt",e=True, oj=orientation[2], sao="zup", ch=True)
    cmds.parent("Jaw_Jnt","Head_Jnt")
    cmds.parent("L_Eye_Jnt", "Head_Jnt")
    cmds.parent("R_Eye_Jnt", "Head_Jnt")
    createJawCtrl()
    createEyeCtrl()
    colorCtrls()


def createJawCtrl():
    drawHalfTorus("Jaw_Ctrl")
    cmds.rotate(0, 90, 0)
    cmds.makeIdentity(apply=True)
    cmds.rotate(90, 0, 0)
    cmds.makeIdentity(apply=True)

    cmds.group(em = True, n = "Jaw_Ctrl_Offset")
    cmds.parent("Jaw_Ctrl","Jaw_Ctrl_Offset")
    pos = cmds.xform("Jaw_Jnt", q=True, t=True, ws=True)
    ros = cmds.xform("Jaw_Jnt", q=True, ro=True, ws=True)
    cmds.move(pos[0], pos[1], pos[2], "Jaw_Ctrl_Offset")
    cmds.rotate(ros[0], ros[1], ros[2],"Jaw_Ctrl_Offset")
    cmds.scale(1,1,1.25,"Jaw_Ctrl_Offset")
    cmds.parent("Jaw_Ctrl_Offset", "Head_Ctrl")
    cmds.parentConstraint("Jaw_Ctrl","Jaw_Jnt",mo = True)


def createEyeCtrl():
    Vert = [(1, 0.5, 0), (1, -0.5, 0), (-1, -0.5, 0), (-1, 0.5, 0), (1, 0.5, 0)]

    rootScale = cmds.xform("Root", q=True, s=True)
    eyePos = cmds.xform("L_Eye", q=True, t=True, ws=True)
    cmds.curve(p=Vert, n="Eyes_Global_Ctrl", d=1)

    cmds.scale(rootScale[0], rootScale[0], rootScale[0])
    cmds.move(0, eyePos[1], 6 * rootScale[0])
    cmds.parent("Eyes_Global_Ctrl", "Head_Ctrl")
    side = ["L", "R"]
    for i, j in enumerate(side):
        eyePos = cmds.xform(j + "_Eye", q=True, t=True, ws=True)
        cmds.circle(nr=(0, 0, 1), c=(0, 0, 0), n=j + "_Eye_Ctrl")
        cmds.scale(0.2 * rootScale[0], 0.2 * rootScale[0], 0.2 * rootScale[0])
        cmds.move(eyePos[0], eyePos[1], 6 * rootScale[0])
        cmds.parent(j + "_Eye_Ctrl", "Eyes_Global_Ctrl")

        cmds.aimConstraint(j+"_Eye_Ctrl", j+"_Eye_Jnt", aim = [0,0,1])


def deleteLocators():
    loc_group = cmds.ls("Loc_*")
    cmds.delete(loc_group)


def deleteJoints():
    loc_group = cmds.ls("Deform_Skeleton_Group")
    cmds.delete(loc_group)
    ik_group = cmds.ls("IK_*")
    cmds.delete(ik_group)


def createSpine():
    for i in range(0, cmds.intSliderGrp(spineCnt, q=True, value=True)):
        spine = cmds.sphere(n="Spine_" + str(i))

        scaleLocator(0.5, spine)
        if i == 0:
            cmds.parent(spine, locator)
            cmds.move(0, 2, 0, spine)
        else:
            cmds.parent(spine, "Spine_" + str(i - 1))
            cmds.move(0, 2 + (2 * i), 0, spine)

    createArms(1)
    createArms(-1)
    createLegs(1)
    createLegs(-1)

    createNeckNHead()
    createHandCmd()


def createArms(side):
    # The Left Side
    if side == 1:
        if cmds.objExists("L_Arm_Grp"):
            print "L_Arm_Grp already exist"
        else:
            # L_Arm = cmds.group(em = True, n = "L_Arm_Grp")
            # cmds.parent(L_Arm, "Spine_" + str(cmds.intSliderGrp(spineCnt, q = True, value = True) - 1))

            # Creating the Left clavicle
            clavicle = cmds.sphere(n="L_Clavicle")
            scaleLocator(0.5, clavicle)
            cmds.parent(clavicle, "Spine_" + str(cmds.intSliderGrp(spineCnt, q=True, value=True) - 1))
            # cmds.parent(clavicle, L_Arm)
            cmds.move(2 * side, (2.2 * cmds.intSliderGrp(spineCnt, q=True, value=True)), 0, clavicle)

            # Creating the Left humerus
            humerus = cmds.sphere(n="L_Humerus")
            scaleLocator(0.5, humerus)
            cmds.parent(humerus, clavicle)
            cmds.move(4 * side, (2 * cmds.intSliderGrp(spineCnt, q=True, value=True)), 0, humerus)

            # Creating the Left radius
            radius = cmds.sphere(n="L_Radius")
            scaleLocator(0.5, radius)
            cmds.parent(radius, humerus)
            cmds.move(6 * side, (1.5 * cmds.intSliderGrp(spineCnt, q=True, value=True)), -0.5, radius)

            # Creating the Left wrist
            wrist = cmds.sphere(n="L_Wrist")
            scaleLocator(0.4, wrist)
            cmds.parent(wrist, radius)
            cmds.move(8 * side, (1 * cmds.intSliderGrp(spineCnt, q=True, value=True)), 0, wrist)

    # the Right Side
    if side == -1:
        if cmds.objExists("R_Arm_Grp"):
            print "R_Arm_Grp already exist"
        else:
            # R_Arm = cmds.group(em = True, n = "R_Arm_Grp")
            # cmds.parent(R_Arm, "Spine_" + str(cmds.intSliderGrp(spineCnt, q = True, value = True) - 1))

            # Creating the Left clavicle
            clavicle = cmds.sphere(n="R_Clavicle")
            scaleLocator(0.5, clavicle)
            cmds.parent(clavicle, "Spine_" + str(cmds.intSliderGrp(spineCnt, q=True, value=True) - 1))
            # cmds.parent(clavicle, R_Arm)
            cmds.move(2 * side, (2.2 * cmds.intSliderGrp(spineCnt, q=True, value=True)), 0, clavicle)

            # Creating the Left humerus
            humerus = cmds.sphere(n="R_Humerus")
            scaleLocator(0.5, humerus)
            cmds.parent(humerus, clavicle)
            cmds.move(4 * side, (2 * cmds.intSliderGrp(spineCnt, q=True, value=True)), 0, humerus)

            # Creating the Left radius
            radius = cmds.sphere(n="R_Radius")
            scaleLocator(0.5, radius)
            cmds.parent(radius, humerus)
            cmds.move(6 * side, (1.5 * cmds.intSliderGrp(spineCnt, q=True, value=True)), -0.5, radius)

            # Creating the Left wrist
            wrist = cmds.sphere(n="R_Wrist")
            scaleLocator(0.4, wrist)
            cmds.parent(wrist, radius)
            cmds.move(8 * side, (1 * cmds.intSliderGrp(spineCnt, q=True, value=True)), 0, wrist)


def createLegs(side):
    # Left Side
    if side == 1:
        if cmds.objExists("L_Leg_Grp"):
            print "L_Leg_Grp already exist"
        else:
            # L_Leg = cmds.group(em=True, n="L_Leg_Grp")
            # cmds.parent(L_Leg, "Cog")

            # Creating the Left hip
            hip = cmds.sphere(n="L_Hip")
            scaleLocator(0.5, hip)
            cmds.parent(hip, "Cog")
            # cmds.parent(hip, L_Leg)
            cmds.move(2 * side, -2, 0, hip)

            # Creating the Left knee
            knee = cmds.sphere(n="L_Knee")
            scaleLocator(0.5, knee)
            cmds.parent(knee, hip)
            cmds.move(2 * side, -6, 0.5, knee)

            # Creating the Left ankle
            ankle = cmds.sphere(n="L_Ankle")
            scaleLocator(0.4, ankle)
            cmds.parent(ankle, knee)
            cmds.move(2 * side, -10, 0, ankle)

            # Creating the Left Foot
            foot = cmds.sphere(n="L_Foot")
            scaleLocator(0.3, foot)
            cmds.parent(foot, ankle)
            cmds.move(2 * side, -11, 1, foot)

            # Creating the Left Toes
            toe = cmds.sphere(n="L_Toe")
            scaleLocator(0.2, toe)
            cmds.parent(toe, foot)
            cmds.move(2 * side, -11, 2, toe)

    # Right side
    if side == -1:
        if cmds.objExists("R_Leg_Grp"):
            print "R_Leg_Grp already exist"
        else:
            # R_Leg = cmds.group(em=True, n="R_Leg_Grp")
            # cmds.parent(R_Leg, "Cog")

            # Creating the Right Hip
            hip = cmds.sphere(n="R_Hip")
            scaleLocator(0.5, hip)
            cmds.parent(hip, "Cog")
            # cmds.parent(hip, R_Leg)
            cmds.move(2 * side, -2, 0, hip)

            # Creating the Right Knee
            knee = cmds.sphere(n="R_Knee")
            scaleLocator(0.5, knee)
            cmds.parent(knee, hip)
            cmds.move(2 * side, -6, 0.5, knee)

            # Creating the Right ankle
            ankle = cmds.sphere(n="R_Ankle")
            scaleLocator(0.4, ankle)
            cmds.parent(ankle, knee)
            cmds.move(2 * side, -10, 0, ankle)

            # Creating the Left Foot
            foot = cmds.sphere(n="R_Foot")
            scaleLocator(0.3, foot)
            cmds.parent(foot, ankle)
            cmds.move(2 * side, -11, 1, foot)

            # Creating the Left Toes
            toe = cmds.sphere(n="R_Toe")
            scaleLocator(0.2, toe)
            cmds.parent(toe, foot)
            cmds.move(2 * side, -11, 2, toe)


def createNeckNHead():
    neck = cmds.sphere(n="Neck")
    cmds.parent(neck, "Spine_" + str(cmds.intSliderGrp(spineCnt, q=True, value=True) - 1))
    scaleLocator(1, neck)
    cmds.move(0, 10, 0, neck)

    head = cmds.sphere(n="Head")
    cmds.parent(head, neck)
    scaleLocator(1, head)
    cmds.move(0, 12, 0, head)


def createHand(side):
    createThumb(side)

    fingers = cmds.intSliderGrp(fingerCnt, q=True, value=True)
    if side == 1:
        if cmds.objExists("L_Wrist"):
            for i in range(fingers):
                if i == 0:
                    F_index = cmds.sphere(n="L_index_" + str(i))
                    scaleLocator(.1, F_index)
                    cmds.parent(F_index, "L_Wrist")
                    cmds.move(9, 3, 0.5, F_index)

                    F_middle = cmds.sphere(n="L_middle_" + str(i))
                    scaleLocator(.1, F_middle)
                    cmds.parent(F_middle, "L_Wrist")
                    cmds.move(9, 3, 0, F_middle)

                    F_ring = cmds.sphere(n="L_ring_" + str(i))
                    scaleLocator(.1, F_ring)
                    cmds.parent(F_ring, "L_Wrist")
                    cmds.move(9, 3, -0.5, F_ring)

                    F_pinky = cmds.sphere(n="L_pinky_" + str(i))
                    scaleLocator(.1, F_pinky)
                    cmds.parent(F_pinky, "L_Wrist")
                    cmds.move(9, 3, -1, F_pinky)


                else:
                    # index finger
                    F_index = cmds.sphere(n="L_index_" + str(i))
                    scaleLocator(.1, F_index)
                    cmds.parent(F_index, "L_index_" + str(i - 1))
                    cmds.move((9 + (0.5 * (i))), 3, 0.5, F_index)

                    # middle finger
                    F_middle = cmds.sphere(n="L_middle_" + str(i))
                    scaleLocator(.1, F_middle)
                    cmds.parent(F_middle, "L_middle_" + str(i - 1))
                    cmds.move((9 + (0.5 * (i))), 3, 0, F_middle)

                    # ring finger
                    F_ring = cmds.sphere(n="L_ring_" + str(i))
                    scaleLocator(.1, F_ring)
                    cmds.parent(F_ring, "L_ring_" + str(i - 1))
                    cmds.move((9 + (0.5 * (i))), 3, -0.5, F_ring)

                    # pinky finger
                    F_pinky = cmds.sphere(n="L_pinky_" + str(i))
                    scaleLocator(.1, F_pinky)
                    cmds.parent(F_pinky, "L_pinky_" + str(i - 1))
                    cmds.move((9 + (0.5 * (i))), 3, -1, F_pinky)
    if side == -1:
        if cmds.objExists("R_Wrist"):
            for i in range(fingers):
                if i == 0:
                    F_index = cmds.sphere(n="R_index_" + str(i))
                    scaleLocator(.1, F_index)
                    cmds.parent(F_index, "R_Wrist")
                    cmds.move(-9, 3, 0.5, F_index)

                    F_middle = cmds.sphere(n="R_middle_" + str(i))
                    scaleLocator(.1, F_middle)
                    cmds.parent(F_middle, "R_Wrist")
                    cmds.move(-9, 3, 0, F_middle)

                    F_ring = cmds.sphere(n="R_ring_" + str(i))
                    scaleLocator(.1, F_ring)
                    cmds.parent(F_ring, "R_Wrist")
                    cmds.move(-9, 3, -0.5, F_ring)

                    F_pinky = cmds.sphere(n="R_pinky_" + str(i))
                    scaleLocator(.1, F_pinky)
                    cmds.parent(F_pinky, "R_Wrist")
                    cmds.move(-9, 3, -1, F_pinky)


                else:
                    # index finger
                    F_index = cmds.sphere(n="R_index_" + str(i))
                    scaleLocator(.1, F_index)
                    cmds.parent(F_index, "R_index_" + str(i - 1))
                    cmds.move(-(9 + (0.5 * (i))), 3, 0.5, F_index)

                    # middle finger
                    F_middle = cmds.sphere(n="R_middle_" + str(i))
                    scaleLocator(.1, F_middle)
                    cmds.parent(F_middle, "R_middle_" + str(i - 1))
                    cmds.move(-(9 + (0.5 * (i))), 3, 0, F_middle)

                    # ring finger
                    F_ring = cmds.sphere(n="R_ring_" + str(i))
                    scaleLocator(.1, F_ring)
                    cmds.parent(F_ring, "R_ring_" + str(i - 1))
                    cmds.move(-(9 + (0.5 * (i))), 3, -0.5, F_ring)

                    # pinky finger
                    F_pinky = cmds.sphere(n="R_pinky_" + str(i))
                    scaleLocator(.1, F_pinky)
                    cmds.parent(F_pinky, "R_pinky_" + str(i - 1))
                    cmds.move(-(9 + (0.5 * (i))), 3, -1, F_pinky)


def createThumb(side):
    fingers = cmds.intSliderGrp(fingerCnt, q=True, value=True)
    if side == 1:

        if cmds.objExists("L_Wrist"):
            for i in range(fingers - 1):
                if i == 0:
                    F_thumb = cmds.sphere(n="L_thumb_" + str(i))
                    scaleLocator(.1, F_thumb)
                    cmds.parent(F_thumb, "L_Wrist")
                    cmds.move(9, 3, 1, F_thumb)

                else:
                    # thumb finger
                    F_thumb = cmds.sphere(n="L_thumb_" + str(i))
                    scaleLocator(.1, F_thumb)
                    cmds.parent(F_thumb, "L_thumb_" + str(i - 1))
                    cmds.move(9 + (0.5 * (i)), 3, 1, F_thumb)
    if side == -1:
        if cmds.objExists("R_Wrist"):
            for i in range(fingers - 1):
                if i == 0:
                    F_thumb = cmds.sphere(n="R_thumb_" + str(i))
                    scaleLocator(.1, F_thumb)
                    cmds.parent(F_thumb, "R_Wrist")
                    cmds.move(-9, 3, 1, F_thumb)

                else:
                    # thumb finger
                    F_thumb = cmds.sphere(n="R_thumb_" + str(i))
                    scaleLocator(.1, F_thumb)
                    cmds.parent(F_thumb, "R_thumb_" + str(i - 1))
                    cmds.move(-(9 + (0.5 * (i))), 3, 1, F_thumb)


def createHandCmd():
    createHand(1)
    createHand(-1)


def mirrorLocators(side):
    allLeftLocators = cmds.ls("L_*")
    allLeftLocators = cmds.listRelatives(allLeftLocators, p=True, f=True)
    # print allLeftLocators
    allRightLocators = cmds.ls("R_*")
    allRightLocators = cmds.listRelatives(allRightLocators, p=True, f=True)
    # print allRightLocators

    if side == 1:
        for i, l in enumerate(allLeftLocators):
            pos = cmds.xform(l, q=True, t=True, ws=True)
            cmds.move(-pos[0], pos[1], pos[2], allRightLocators[i])
    if side == -1:
        for i, l in enumerate(allRightLocators):
            pos = cmds.xform(l, q=True, t=True, ws=True)
            cmds.move(-pos[0], pos[1], pos[2], allLeftLocators[i])


def createJoints():
    visibilityToggle(False)
    if cmds.objExists("Deform_Skeleton_Group"):
        print "Rig_Group already exist"
    else:
        cmds.group(em=True, n="Deform_Skeleton_Group")

        all_Loc = cmds.ls("Loc_MasterGroup")
        all_Loc = cmds.listRelatives(all_Loc, ad=True, pa=True)
        filtered = cmds.ls(all_Loc, tr=True, o=True)
        for i, l in reversed(list(enumerate(filtered))):
            pos = cmds.xform(l, q=True, t=True, ws=True)
            theJoints = cmds.joint(n=str(l) + "_Jnt", p=pos)
            # print l
            # print pos
        fixParent()
        fixOrientation()
        makeSets()


def fixParent():
    cmds.parent("L_Hip_Jnt", "Cog_Jnt")
    # cmds.parent("R_Hip_Jnt", "Cog_Jnt")
    cmds.parent("Spine_0_Jnt", "Cog_Jnt")
    cmds.parent("R_Clavicle_Jnt", "Spine_" + str(cmds.intSliderGrp(spineCnt, q=True, value=True) - 1) + "_Jnt")
    cmds.parent("L_Clavicle_Jnt", "Spine_" + str(cmds.intSliderGrp(spineCnt, q=True, value=True) - 1) + "_Jnt")

    L_fingerRoots = ["L_index_0_Jnt", "L_middle_0_Jnt", "L_thumb_0_Jnt", "L_ring_0_Jnt"]
    R_fingerRoots = ["R_index_0_Jnt", "R_middle_0_Jnt", "R_thumb_0_Jnt", "R_ring_0_Jnt"]
    for i, j in enumerate(L_fingerRoots):
        cmds.parent(j, "L_Wrist_Jnt")
    for i, j in enumerate(R_fingerRoots):
        cmds.parent(j, "R_Wrist_Jnt")


def visibilityToggle(visibility):
    if cmds.objExists("Loc_MasterGroup"):
        cmds.setAttr("Loc_MasterGroup.visibility", visibility)
    else:
        print "Create Locator First"


def check():
    state = cmds.checkBox(cBox, q=True, v=True)
    visibilityToggle(state)


def fixOrientation():
    print "fixing orientation"
    orientation = ["xzy", "yzx", "zyx"]
    side = ["L", "R"]
    fingerRoots = ["_index_0_Jnt", "_thumb_0_Jnt", "_ring_0_Jnt", "_pinky_0_Jnt"]
    for a, b in enumerate(side):
        for i, j in enumerate(fingerRoots):
            cmds.parent(b + j, w=True)

    cmds.select("Spine_0_Jnt")
    cmds.joint(e=True, oj=orientation[1], sao="zup", ch=True)

    for a, b in enumerate(side):
        cmds.select(b + "_Hip_Jnt")
        cmds.joint(e=True, oj=orientation[1], sao="zup", ch=True)
        cmds.select(b + "_Ankle_Jnt")
        cmds.joint(e=True, oj=orientation[2], sao="yup", ch=True)
        cmds.parent(b + "_middle_0_Jnt", w=True)

    fingerRoots = []
    fingerRoots = ["_index_0_Jnt", "_middle_0_Jnt", "_thumb_0_Jnt", "_ring_0_Jnt", "_pinky_0_Jnt"]

    for a, b in enumerate(side):
        for i, j in enumerate(fingerRoots):
            cmds.select(b + j)
            cmds.joint(e=True, oj=orientation[0], sao="zup", ch=True)

        for i, j in enumerate(fingerRoots):
            cmds.parent(b + j, b + "_Wrist_Jnt")


def radioInput(inp):
    global radioOpt
    if inp == 0:
        radioOpt = False
    if inp == 1:
        radioOpt = True

############################### not Using this anymore
def makeOrientationGizmo(finger):
    if cmds.objExists("tmp"):
        cmds.delete("tmp")
    cmds.group(em=True, n="tmp")
    cmds.parent("tmp", "Deform_Skeleton_Group")
    fingers = []
    if finger == True:
        fingers = ["thumb"]
    if finger == False:
        fingers = ["thumb", "index", "middle", "ring", "pinky"]
    for i, j in enumerate(fingers):
        arrow = cmds.textCurves(n=j + "_Arrow_", f='Wingdings 3', t='h')
        cmds.select("curve1")
        cmds.parent(w=True, r=True)
        cmds.rename("curve1", j)
        cmds.xform(cp=True)
        cmds.move(-0.297, 0, 0)
        cmds.xform(piv=[0, 0, 0], ws=True)
        cmds.rotate(0, 90, 0)
        cmds.makeIdentity(apply=True)
        cmds.delete(j + "_Arrow_Shape")

        offset_Grp = cmds.group(em=True, n=j + "_Offset")
        cmds.parent(j, offset_Grp)
        cmds.parentConstraint("L_" + j + "_0_Jnt", j + "_Offset", n="Temp_Const")
        cmds.delete("Temp_Const")
        cmds.parent(j + "_Offset", "tmp")
        rootScale = cmds.xform("Root", q=True, s=True)
        cmds.scale(rootScale[0], rootScale[1], rootScale[2], j + "_Offset", r=True)
###############################

def applyOrientationToFinger():
    fingers = []
    finger = radioOpt
    if finger == True:
        fingers = ["thumb"]
    if finger == False:
        fingers = ["thumb", "index", "middle", "ring", "pinky"]
    for i, j in enumerate(fingers):
        gizmo_rotation = cmds.xform(j, q=True, ro=True)
        print gizmo_rotation
        cmds.select("L_" + j + "_0_Jnt", hi=True)
        joints = cmds.ls(sl=True)
        print joints
        for k, l in enumerate(joints):
            cmds.joint(l, e=True, zso=True)
            rotAx = cmds.select(l + ".rotateAxis")
            cmds.rotate(-gizmo_rotation[0], 0, 0, l + ".rotateAxis", r=False, os=True)
            cmds.joint(l, e=True, zso=True)

    applyOrientationToWrist()
    cmds.delete("tmp")
    mirrorFingers()


def applyOrientationToWrist():
    fingers = ["thumb_0_Jnt", "index_0_Jnt", "middle_0_Jnt", "ring_0_Jnt", "pinky_0_Jnt"]
    cmds.parent("L_Wrist_Jnt", w=True)
    for i, j in enumerate(fingers):
        cmds.parent("L_" + j, w = True)
        cmds.parent("R_" + j, w=True)
    cmds.delete("R_Wrist_Jnt")
    gizmo_rotation = cmds.xform("Wrist_Gizmo", q=True, ro=True)
    rotAx = cmds.select("L_Wrist_Jnt.rotateAxis")
    cmds.rotate(-gizmo_rotation[0],-gizmo_rotation[1], 0, "L_Wrist_Jnt.rotateAxis", r=False, os=True)
    cmds.joint("L_Wrist_Jnt", e=True, zso=True)
    cmds.parent("L_Wrist_Jnt", "Root_Jnt")
    cmds.mirrorJoint("L_Wrist_Jnt", myz=True, mb=True, sr=("L_", "R_"))
    cmds.parent("L_Wrist_Jnt", "L_Radius_Jnt")
    cmds.parent("R_Wrist_Jnt", "R_Radius_Jnt")


def mirrorFingers():
    fingers = ["thumb_0_Jnt", "index_0_Jnt", "middle_0_Jnt", "ring_0_Jnt", "pinky_0_Jnt"]
    for i, j in enumerate(fingers):
        cmds.delete("R_" + j)
        cmds.parent("L_" + j, "Root_Jnt")
        cmds.mirrorJoint("L_" + j, myz=True, mb=True, sr=("L_", "R_"))
        cmds.parent("L_" + j, "L_Wrist_Jnt")
        cmds.parent("R_" + j, "R_Wrist_Jnt")


def duplicateJointsForIKFK():
    ikfk = ["IK", "FK"]
    if cmds.objExists("IKFK_Group"):
        print "Group already exist"
    else:
        cmds.group(em=True, n="IKFK_Group")
        for a, b in enumerate(ikfk):
            if cmds.objExists("L_" + b + "_Group") or cmds.objExists("R_" + b + "_Group") and cmds.objExists(
                    b + "_Group"):
                print "IKFK_Group Already exists"
            else:
                ikfk_Group = cmds.group(em=True, n=b + "_Group")
                cmds.parent(ikfk_Group, "IKFK_Group")

            # Duplicating left hand IK
            l_hand_joints = ["L_Humerus", "L_Radius", "L_Wrist"]
            r_hand_joints = ["R_Humerus", "R_Radius", "R_Wrist"]

            jointList = [l_hand_joints, r_hand_joints]
            for k, l in enumerate(jointList):
                joint = []
                for i, j in enumerate(l):
                    cmds.duplicate(j + "_Jnt", n=b + "_" + j + "_Jnt", po=True)
                    joint += cmds.parent(b + "_" + j + "_Jnt", b + "_Group")
                cmds.parent(joint[2], joint[1])
                cmds.parent(joint[1], joint[0])
                print joint
            l_leg_joints = ["L_Hip", "L_Knee", "L_Ankle", "L_Foot", "L_Toe"]
            r_leg_joints = ["R_Hip", "R_Knee", "R_Ankle", "R_Foot", "R_Toe"]
            leg_jointList = [l_leg_joints, r_leg_joints]
            for k, l in enumerate(leg_jointList):
                joint = []
                for i, j in enumerate(l):
                    cmds.duplicate(j + "_Jnt", n=b + "_" + j + "_Jnt", po=True)
                    joint += cmds.parent(b + "_" + j + "_Jnt", b + "_Group")
                cmds.parent(joint[4], joint[3])
                cmds.parent(joint[3], joint[2])
                cmds.parent(joint[2], joint[1])
                cmds.parent(joint[1], joint[0])


def makeIKHandles():
    side = ["L", "R"]
    for i, j in enumerate(side):
        cmds.ikHandle(n=j + "_Hand_IK_Handle", sj="IK_" + j + "_Humerus_Jnt", ee="IK_" + j + "_Wrist_Jnt",
                      sol="ikRPsolver", p=1, w=1, pw=1, s="sticky")
        cmds.ikHandle(n=j + "_Leg_IK_Handle", sj="IK_" + j + "_Hip_Jnt", ee="IK_" + j + "_Ankle_Jnt", sol="ikRPsolver",
                      p=1, w=1, pw=1, s="sticky")
        cmds.ikHandle(n=j + "_Foot_IK_Handle", sj="IK_" + j + "_Ankle_Jnt", ee="IK_" + j + "_Foot_Jnt",
                      sol="ikSCsolver", p=1, w=1, pw=1, s="sticky")
        cmds.ikHandle(n=j + "_Toe_IK_Handle", sj="IK_" + j + "_Foot_Jnt", ee="IK_" + j + "_Toe_Jnt", sol="ikSCsolver",
                      p=1, w=1, pw=1, s="sticky")
        cmds.parent(j + "_Hand_IK_Handle", "IK_Group")

        cmds.group(em=True, n=j + "_IK_Humerus_Group")
        humerusPos = cmds.xform(j + "_Humerus_Jnt", q=True, t=True, ws=True)
        humerusRo = cmds.xform(j + "_Humerus_Jnt", q=True, t=True, ws=True)
        cmds.move(humerusPos[0], humerusPos[1], humerusPos[2], j + "_IK_Humerus_Group")
        cmds.rotate(humerusRo[0], humerusRo[1], humerusRo[2], j + "_IK_Humerus_Group")

        cmds.parent("IK_" + j + "_Humerus_Jnt", j + "_IK_Humerus_Group")


def makeReverseFootLoc():
    if cmds.objExists("Rev_Foot_Loc"):
        print "Rev_Foot_Loc already exists"
    else:
        rootScale = cmds.xform("Root", q=True, s=True)

        l_toePos = cmds.xform("L_Toe", q=True, t=True, ws=True)
        cmds.group(em=True, n="Rev_Foot_Loc")

        heel = cmds.sphere(n="L_Heel")
        scaleLocator(rootScale[0] * 0.2, heel)
        cmds.parent(heel, "Rev_Foot_Loc")
        cmds.move(l_toePos[0], 0, -0.5, heel)
    makeBankingLocators()


def mirrorHeelLoc():
    rootScale = cmds.xform("Root", q=True, s=True)
    r_toePos = cmds.xform("R_Toe", q=True, t=True, ws=True)
    lHeelPos = cmds.xform("L_Heel", q=True, t=True, ws=True)
    heel = cmds.sphere(n="R_Heel")
    scaleLocator(rootScale[0] * 0.2, heel)
    cmds.parent(heel, "Rev_Foot_Loc")
    cmds.move(-lHeelPos[0], lHeelPos[1], lHeelPos[2], heel)


def makeReverseFootJoint():
    if cmds.objExists("Rev_Foot_Loc"):
        mirrorHeelLoc()
        cmds.group(em=True, n="Rev_Foot_Jnt_Group")
        pos = cmds.xform("L_Heel", q=True, t=True, ws=True)
        cmds.joint(n="L_Rev_Heel_Jnt", p=pos)
        pos = cmds.xform("R_Heel", q=True, t=True, ws=True)
        cmds.joint(n="R_Rev_Heel_Jnt", p=pos)
        cmds.parent("R_Rev_Heel_Jnt", "Rev_Foot_Jnt_Group")
        side = ["R", "L"]
        footJoints = ["_Toe", "_Foot", "_Ankle"]

        for i, j in enumerate(side):
            joint = []
            for k, l in enumerate(footJoints):
                cmds.duplicate(j + l + "_Jnt", n=j + "_Rev" + l + "_Jnt", po=True)
                joint += cmds.parent(j + "_Rev" + l + "_Jnt", "Rev_Foot_Jnt_Group")
            cmds.parent(joint[2], joint[1])
            cmds.parent(joint[1], joint[0])
            cmds.parent(joint[0], j + "_Rev_Heel_Jnt")
        cmds.delete("Rev_Foot_Loc")
    else:
        print "Create Heel First"


def finalizeReverseFoot():
    side = ["L", "R"]
    for i, j in enumerate(side):
        if cmds.objExists(j + "_Bank_Out") or cmds.objExists(j + "_Bank_In") or cmds.objExists(j + "_Toe_Tap"):
            print "already Exists"
        else:
            cmds.group(em=True, n=j + "_Bank_Out")
            cmds.group(em=True, n=j + "_Bank_In")
            cmds.group(em=True, n=j + "_Toe_Tap")
            cmds.group(em=True, n=j + "_IK_Foot_Group")

            footPos = cmds.xform(j + "_Foot_Jnt", q=True, t=True, ws=True)

            cmds.xform(j + "_Toe_Tap", piv=footPos, ws=True)
            cmds.parent(j + "_Bank_In", j + "_Bank_Out")
            cmds.parent(j + "_Bank_Out", "Rev_Foot_Jnt_Group")
            cmds.parent(j + "_Leg_IK_Handle", j + "_Rev_Ankle_Jnt")
            cmds.parent(j + "_Toe_IK_Handle", j + "_Toe_Tap")
            cmds.parent(j + "_Toe_Tap", j + "_Rev_Toe_Jnt")
            cmds.parent(j + "_Foot_IK_Handle", j + "_Rev_Foot_Jnt")
            cmds.parent(j + "_Rev_Heel_Jnt", j + "_Bank_In")
            cmds.parent(j + "_IK_Foot_Group", "Rev_Foot_Jnt_Group")
            cmds.parent(j + "_Bank_Out", j + "_IK_Foot_Group")
            anklePos = cmds.xform(j + "_Ankle_Jnt", q=True, t=True, ws=True)
            cmds.xform(j + "_IK_Foot_Group", piv=anklePos, ws=True)


def makeBankingLocators():
    rootScale = cmds.xform("Root", q=True, s=True)

    l_footPos = cmds.xform("L_Foot", q=True, t=True, ws=True)
    cmds.group(em=True, n="Banking_Group")

    cmds.spaceLocator(n="L_InnerBank")
    cmds.move(l_footPos[0] - rootScale[0], l_footPos[1], l_footPos[2])
    cmds.scale(rootScale[0], rootScale[1], rootScale[2])

    cmds.spaceLocator(n="L_OuterBank")
    cmds.move(l_footPos[0] + rootScale[0], l_footPos[1], l_footPos[2])
    cmds.scale(rootScale[0], rootScale[1], rootScale[2])

    cmds.parent("L_InnerBank", "Banking_Group")
    cmds.parent("L_OuterBank", "Banking_Group")


def mirrorBankingLocators():
    rootScale = cmds.xform("Root", q=True, s=True)

    l_inner_locPos = cmds.xform("L_InnerBank", q=True, t=True, ws=True)
    l_outer_locPos = cmds.xform("L_OuterBank", q=True, t=True, ws=True)

    cmds.spaceLocator(n="R_InnerBank")
    cmds.move(-l_inner_locPos[0], l_inner_locPos[1], l_inner_locPos[2])
    cmds.scale(rootScale[0], rootScale[1], rootScale[2])

    cmds.spaceLocator(n="R_OuterBank")
    cmds.move(-l_outer_locPos[0], l_outer_locPos[1], l_outer_locPos[2])
    cmds.scale(rootScale[0], rootScale[1], rootScale[2])

    cmds.parent("R_InnerBank", "Banking_Group")
    cmds.parent("R_OuterBank", "Banking_Group")
    movingBanKingPivots()


def movingBanKingPivots():
    side =["L","R"]
    for i, j in enumerate(side):
        inner_locPos = cmds.xform(j+"_InnerBank", q=True, t=True, ws=True)
        outer_locPos = cmds.xform(j+"_OuterBank", q=True, t=True, ws=True)

        cmds.select(j+"_Bank_In")
        cmds.xform(piv = (inner_locPos[0],inner_locPos[1],inner_locPos[2]))
        cmds.select(j + "_Bank_Out")
        cmds.xform(piv=(outer_locPos[0], outer_locPos[1], outer_locPos[2]))
    cmds.delete("Banking_Group")


def makeCtrlRig():
    duplicateJointsForIKFK()
    makeIKHandles()
    makeReverseFootJoint()
    finalizeReverseFoot()


def makeTheControls():
    makeFKCtrl()
    drawCtrl()
    parentingCtrls()
    #connectFingerToSwitch()
    mirrorBankingLocators()
    settingUpAttributes()


def makeFKCtrl():
    side = ["L", "R"]
    scale = 0.6
    hands = ["_Humerus", "_Radius", "_Wrist"]
    legs = ["_Hip", "_Knee","_Ankle","_Foot"]
    for i, j in enumerate(side):
        for k, l in enumerate(hands):
            drawTorus(j + l + "_FK_Ctrl")
            cmds.scale(scale, scale, scale)
            cmds.makeIdentity(apply=True)
            cmds.group(em=True, n=j + l + "_FK_Offset")
            cmds.parent(j + l + "_FK_Ctrl", j + l + "_FK_Offset")
            jointPos = cmds.xform(j + l + "_Jnt", q=True, t=True, ws=True)
            jointRo = cmds.xform(j + l + "_Jnt", q=True, ro=True, ws=True)
            cmds.move(jointPos[0], jointPos[1], jointPos[2], j + l + "_FK_Offset")
            cmds.rotate(jointRo[0], jointRo[1], jointRo[2], j + l + "_FK_Offset")

        for k, l in enumerate(legs):
            drawTorus(j + l + "_FK_Ctrl")
            cmds.scale(scale, scale, scale)
            cmds.makeIdentity(apply=True)
            cmds.group(em=True, n=j + l + "_FK_Offset")
            cmds.parent(j + l + "_FK_Ctrl", j + l + "_FK_Offset")
            jointPos = cmds.xform(j + l + "_Jnt", q=True, t=True, ws=True)
            jointRo = cmds.xform(j + l + "_Jnt", q=True, ro=True, ws=True)
            cmds.move(jointPos[0], jointPos[1], jointPos[2], j + l + "_FK_Offset")
            cmds.rotate(jointRo[0], jointRo[1], jointRo[2], j + l + "_FK_Offset")
        cmds.scale(1.7, 1.7, 1.7, j + "_Hip_FK_Offset")

        cmds.parent(j + legs[3] + "_FK_Offset",j + legs[2] + "_FK_Ctrl")
        cmds.parent(j + legs[2] + "_FK_Offset", j + legs[1] + "_FK_Ctrl")
        cmds.parent(j + legs[1] + "_FK_Offset", j + legs[0] + "_FK_Ctrl")


        cmds.parent(j + hands[2] + "_FK_Offset", j + hands[1] + "_FK_Ctrl")
        cmds.parent(j + hands[1] + "_FK_Offset", j + hands[0] + "_FK_Ctrl")
# drawing nurb ctrls

def drawCtrl():
    drawCogCtrl()
    drawSpineCtrl()
    drawFootIKCtrl()
    drawHandIKCtrl()
    drawShoulderCtrl()
    makeHeadCtrl()
    makeNeckCtrl()

    applyConstraints()
    makeIKFKSwitch()
    makeFingerCtrl()


def drawFootIKCtrl():
    rootScale = cmds.xform("Root", q=True, s=True)
    side = ["L", "R"]
    revFootParts = ["Heel","Toe"]
    for i, j in enumerate(side):
        drawFootCtrl(j + "_Foot_IK_Ctrl")

        heelPos = cmds.xform(j + "_Rev_Heel_Jnt", q=True, t=True, r=True)
        cmds.move(heelPos[0], heelPos[1], heelPos[2], r=True, ws=True)
        cmds.makeIdentity(apply=True)
        anklePos = cmds.xform(j + "_Rev_Ankle_Jnt", q=True, t=True, ws=True)
        cmds.xform(piv=(anklePos[0], anklePos[1], anklePos[2]))

        drawPyramid(j + "_Leg_Pole_Ctrl")
        kneePos = cmds.xform(j + "_Knee_Jnt", q=True, t=True, ws=True)
        cmds.move(kneePos[0], kneePos[1], kneePos[2])
        cmds.rotate(180, 0, 0)
        cmds.makeIdentity(apply=True)
        cmds.move(3 * rootScale[2], z=True)
        cmds.makeIdentity(apply=True)

        drawTorus(j + "_Hip_IK_Ctrl")
        hipPos = cmds.xform(j + "_Hip_Jnt", q=True, t=True, ws=True)
        cmds.move(hipPos[0], hipPos[1], hipPos[2])
        cmds.makeIdentity(apply=True)
        cmds.parent(j + "_Hip_IK_Ctrl", "Hip_Ctrl")

        for k, l in enumerate(revFootParts):
            drawCylinder(j + "_" + l + "_Ctrl")
            cmds.scale(0.2, 1, 0.2)
            cmds.rotate(0, 0, 90)
            cmds.makeIdentity(apply=True)
            pos = cmds.xform(j + "_Rev_" + l + "_Jnt", q=True, t=True, ws=True)
            cmds.move(pos[0], pos[1], pos[2], j + "_" + l + "_Ctrl")
            cmds.makeIdentity(apply=True)
            cmds.parent(j + "_" + l + "_Ctrl", j + "_Foot_IK_Ctrl")


def drawHandIKCtrl():
    rootScale = cmds.xform("Root", q=True, s=True)
    side = ["L", "R"]
    for i, j in enumerate(side):
        # pole vectors
        drawPyramid(j + "_Hand_Pole_Ctrl")
        elbowPos = cmds.xform(j + "_Radius_Jnt", q=True, t=True, ws=True)

        cmds.move(elbowPos[0], elbowPos[1], elbowPos[2])
        cmds.move(-3 * rootScale[2], z=True)
        cmds.makeIdentity(apply=True)
        # Hand
        drawCylinder(j + "_Hand_IK_Ctrl")
        cmds.scale(1, 0.5, 1)
        cmds.group(em=True, n=j + "_Hand_IK_Offset")
        cmds.parent(j + "_Hand_IK_Ctrl", j + "_Hand_IK_Offset")
        wristPos = cmds.xform(j + "_Wrist_Jnt", q=True, t=True, ws=True)
        wristRo = cmds.xform(j + "_Wrist_Jnt", q=True, ro=True, ws=True)
        cmds.move(wristPos[0], wristPos[1], wristPos[2], j + "_Hand_IK_Offset")
        cmds.rotate(wristRo[0], wristRo[1], wristRo[2], j + "_Hand_IK_Offset")


def drawSpineCtrl():
    for i in range(0, cmds.intSliderGrp(spineCnt, q=True, value=True)):
        spine = drawTorus("Spine_" + str(i) + "_Ctrl")
        spinePos = cmds.xform("Spine_" + str(i) + "_Jnt", q=True, t=True, ws=True)
        spineRo = cmds.xform("Spine_" + str(i) + "_Jnt", q=True, ro=True, ws=True)
        cmds.move(spinePos[0], spinePos[1], spinePos[2], "Spine_" + str(i) + "_Ctrl")
        # cmds.rotate(spineRo[0],spineRo[1],spineRo[2],"Spine_"+str(i)+"_Ctrl" )
        # cmds.makeIdentity(apply = True)

        if i == 0:
            cmds.scale(1.4, 1.4, 1.4, "Spine_" + str(i) + "_Ctrl")
            cmds.makeIdentity(apply=True)
            cmds.parent("Spine_" + str(i) + "_Ctrl", "Cog_Ctrl")
        else:
            cmds.parent("Spine_" + str(i) + "_Ctrl", "Spine_" + str(i - 1) + "_Ctrl")
    spineIndex = cmds.intSliderGrp(spineCnt, q=True, value=True)

    cmds.scale(1.1, 1.3, 1.3, "Spine_"+str(spineIndex - 1)+"_Ctrl")
    cmds.scale(1.1, 1.1, 1.1, "Spine_"+str(spineIndex - 2)+"_Ctrl")
    cmds.scale(1.5, 1.1, 1.1, "Spine_"+str(spineIndex - 3)+"_Ctrl")


def drawShoulderCtrl():
    side = ["L", "R"]
    lastSpine = cmds.intSliderGrp(spineCnt, q=True, value=True)
    for i, j in enumerate(side):
        # shoulders
        drawHalfTorus(j + "_Shoulder_Ctrl")
        clavPos = cmds.xform(j + "_Clavicle_Jnt", q=True, t=True, ws=True)
        cmds.move(clavPos[0], clavPos[1], clavPos[2])
        cmds.makeIdentity(apply=True)
        cmds.parent(j + "_Shoulder_Ctrl", "Spine_" + str(lastSpine - 1) + "_Ctrl")
        cmds.makeIdentity(apply=True)
        cmds.parent(j + "_IK_Humerus_Group", j + "_Shoulder_Ctrl")


def drawCogCtrl():
    drawTorus("Cog_Ctrl")
    cmds.scale(2.5, 2.5, 2.5)
    cogPos = cmds.xform("Cog_Jnt", q=True, t=True, ws=True)
    cmds.move(cogPos[0], cogPos[1], cogPos[2])
    cmds.makeIdentity(apply=True)

    drawTorus("Hip_Ctrl")
    cmds.scale(2, 6, 2)
    cogPos = cmds.xform("Cog_Jnt", q=True, t=True, ws=True)
    cmds.move(cogPos[0], cogPos[1], cogPos[2])
    cmds.makeIdentity(apply=True)
    cmds.parent("Hip_Ctrl", "Cog_Ctrl")


def makeIKFKSwitch():
    side = ["L", "R"]

    rootScale = cmds.xform("Root", q=True, s=True)
    for i, j in enumerate(side):
        drawHandShape(j + "_Hand_IKFK_Switch")
        cmds.scale(2 * rootScale[0], 2 * rootScale[0], 2 * rootScale[0])
        cmds.move(2 * rootScale[0], 0, 0)
        cmds.xform(piv=[0, 0, 0], ws=True)
        cmds.makeIdentity(apply=True)

        drawPointDown(j+"_Leg_IKFK_Switch")
        cmds.scale(2 * rootScale[0], 2 * rootScale[0], 2 * rootScale[0])
        cmds.move(2 * rootScale[0], 0, 0)
        cmds.xform(piv=[0, 0, 0], ws=True)
        cmds.makeIdentity(apply=True)

    cmds.rotate(0, 180, 0, "R_Hand_IKFK_Switch")
    cmds.makeIdentity(apply=True)
    cmds.rotate(0, 180, 0, "R_Leg_IKFK_Switch")
    cmds.makeIdentity(apply=True)

    for i,j in enumerate(side):# Moving to humerus and parenting to joint
        humerusPos = cmds.xform(j +"_Humerus_Jnt", q = True, t = True, ws = True)
        cmds.move(humerusPos[0],humerusPos[1],humerusPos[2], j +"_Hand_IKFK_Switch")
        cmds.makeIdentity(apply = True)
        cmds.parentConstraint(j + "_Humerus_Jnt", j + "_Hand_IKFK_Switch", mo=True, n=j + "_Hand_IKFK_Switch_ParentConstraint")

        kneePos = cmds.xform(j + "_Knee_Jnt", q=True, t=True, ws=True)
        cmds.move(kneePos[0], kneePos[1], kneePos[2], j + "_Leg_IKFK_Switch")
        cmds.makeIdentity(apply=True)
        cmds.parentConstraint(j + "_Knee_Jnt", j + "_Leg_IKFK_Switch", mo=True,
                              n=j + "_Leg_IKFK_Switch_ParentConstraint")

    for i,j in enumerate(side):
        axis = ["x","y","z"]
        cmds.select(j + "_Hand_IKFK_Switch")
        cmds.addAttr(ln="IK_FK", at="double", k=True, defaultValue=0, minValue=0, maxValue=1)
        for k,l in enumerate(axis):
            cmds.setAttr(j +"_Hand_IKFK_Switch.t"+l,lock = True,keyable = False,channelBox = False)
            cmds.setAttr(j + "_Hand_IKFK_Switch.r"+l, lock=True,keyable = False,channelBox = False)
            cmds.setAttr(j + "_Hand_IKFK_Switch.s"+l, lock=True,keyable = False,channelBox = False)

        cmds.select(j + "_Leg_IKFK_Switch")
        cmds.addAttr(ln="IK_FK", at="double", k=True, defaultValue=0, minValue=0, maxValue=1)
        for k, l in enumerate(axis):
            cmds.setAttr(j + "_Leg_IKFK_Switch.t" + l, lock=True, keyable=False, channelBox=False)
            cmds.setAttr(j + "_Leg_IKFK_Switch.r" + l, lock=True, keyable=False, channelBox=False)
            cmds.setAttr(j + "_Leg_IKFK_Switch.s" + l, lock=True, keyable=False, channelBox=False)
    wiringIKFKSwitch()


def makeFingerGizmo(finger):
    if cmds.objExists("tmp"):
        cmds.delete("tmp")
    cmds.group(em=True, n="tmp")
    cmds.parent("tmp", "Deform_Skeleton_Group")
    fingers = []

    if finger == True:
        fingers = ["thumb"]
    if finger == False:
        fingers = ["thumb", "index", "middle", "ring", "pinky"]
    for i, j in enumerate(fingers):
        drawAxisGizmo(j)
        offset_Grp = cmds.group(em=True, n=j + "_Offset")
        cmds.parent(j, offset_Grp)
        cmds.parentConstraint("L_" + j + "_0_Jnt", j + "_Offset", n="Temp_Const")
        cmds.delete("Temp_Const")
        cmds.parent(j + "_Offset", "tmp")
        rootScale = cmds.xform("Root", q=True, s=True)
        cmds.scale(rootScale[0], rootScale[1], rootScale[2], j + "_Offset", r=True)

        cmds.setAttr(j+".overrideEnabled", 1)
        cmds.setAttr("Xaxis_" + j + ".overrideEnabled", 1)
        cmds.setAttr("Xaxis_"+j+".overrideColor", 13)
        cmds.setAttr("Yaxis_" + j + ".overrideEnabled", 1)
        cmds.setAttr("Yaxis_" + j + ".overrideColor", 14)
        cmds.setAttr("Zaxis_" + j + ".overrideEnabled", 1)
        cmds.setAttr("Zaxis_" + j + ".overrideColor", 6)
    makeWristGizmo()


def makeWristGizmo():
    offset_Grp = cmds.group(em=True, n="Wrist_Gizmo_Offset")
    drawAxisGizmo("Wrist_Gizmo")
    cmds.parent("Wrist_Gizmo", "Wrist_Gizmo_Offset")
    cmds.parentConstraint("L_Wrist_Jnt", "Wrist_Gizmo_Offset", n="Temp_Wrist_Const")
    cmds.delete("Temp_Wrist_Const")
    cmds.parent("Wrist_Gizmo_Offset", "tmp")
    rootScale = cmds.xform("Root", q=True, s=True)
    cmds.scale(rootScale[0], rootScale[1], rootScale[2], "Wrist_Gizmo_Offset", r=True)


def makeHeadCtrl():
    drawCrown("Head_Ctrl")
    headPos = cmds.xform("Head_Jnt", q =True,t = True, ws =True)
    rootScale = cmds.xform("Root", q=True, s=True)
    cmds.move(headPos[0],headPos[1]+(3*rootScale[0]),headPos[2], "Head_Ctrl")
    cmds.scale(2*rootScale[0],1.5*rootScale[1],2*rootScale[2],"Head_Ctrl")
    cmds.makeIdentity(apply = True)
    cmds.xform(piv =[headPos[0],headPos[1],headPos[2]])


def makeNeckCtrl():
    drawNeckCtrl("Neck_Ctrl")
    neckPos = cmds.xform("Neck_Jnt", q=True, t=True, ws=True)
    rootScale = cmds.xform("Root", q=True, s=True)
    cmds.move(neckPos[0], neckPos[1], neckPos[2], "Neck_Ctrl")
    cmds.scale(rootScale[0], rootScale[1], rootScale[2], "Neck_Ctrl")
    cmds.makeIdentity(apply=True)


def makeFingerCtrl():

    side = ["L", "R"]
    fingers = ["thumb", "index", "middle", "ring", "pinky"]
    fingerJoints = cmds.intSliderGrp(fingerCnt, q=True, value=True) - 1

    for i, j in enumerate(side):
        for k, l in enumerate(fingers):
            for z in range(0, fingerJoints):
                jointPos = cmds.xform(j + "_" + l + "_" + str(z) + "_Jnt", q=True, t=True, ws=True)
                jointRo = cmds.xform(j + "_" + l + "_" + str(z) + "_Jnt", q=True, ro=True, ws=True)
                fingerCtrl = drawfingerCtrl(j + "_" + l + "_" + str(z) + "_Ctrl")
                cmds.group(em=True, n=j + "_" + l + "_" + str(z) + "_Offset")
                cmds.parent(j + "_" + l + "_" + str(z) + "_Ctrl", j + "_" + l + "_" + str(z) + "_Offset")
                cmds.move(jointPos[0], jointPos[1], jointPos[2], j + "_" + l + "_" + str(z) + "_Offset")
                cmds.rotate(jointRo[0], jointRo[1], jointRo[2], j + "_" + l + "_" + str(z) + "_Offset")
        cmds.delete(j + "_thumb_3_Offset")

    fingers = ["index", "middle", "ring", "pinky"]
    for i, j in enumerate(fingers):
        for z in range(0, fingerJoints):
            jointRo = cmds.xform("R_" + j + "_" + str(z) + "_Jnt", q=True, ro=True, ws=True)
            jointRo = [jointRo[0] + 180, jointRo[1], jointRo[2]]
            cmds.rotate(jointRo[0], jointRo[1], jointRo[2], "R_" + j + "_" + str(z) + "_Offset")

    for i in range(0, fingerJoints - 1):
        jointRo = cmds.xform("R_thumb_" + str(i) + "_Jnt", q=True, ro=True, ws=True)
        jointRo = [jointRo[0] + 180, jointRo[1], jointRo[2]]
        cmds.rotate(jointRo[0], jointRo[1], jointRo[2], "R_thumb_" + str(i) + "_Offset")

    for i, j in enumerate(side):
        cmds.group(em=True, n=j + "_Finger_Group")
        cmds.parentConstraint(j+"_Wrist_Jnt", j + "_Finger_Group", mo=False, n=j+"_Temp_ParentConstraint")
        cmds.delete(j+"_Temp_ParentConstraint")
        for k, l in enumerate(fingers):
            fingerCtrls = []
            for z in range(0, fingerJoints):
                fingerCtrls += cmds.parent(j + "_" + l + "_" + str(z) + "_Offset", j + "_Finger_Group")
            cmds.parent(fingerCtrls[3], fingerCtrls[2])
            cmds.parent(fingerCtrls[2], fingerCtrls[1])
            cmds.parent(fingerCtrls[1], fingerCtrls[0])

    fingers = ["thumb"]
    for i, j in enumerate(side):
        for k, l in enumerate(fingers):
            fingerCtrls = []
            for z in range(0, fingerJoints - 1):
                fingerCtrls += cmds.parent(j + "_" + l + "_" + str(z) + "_Offset", j + "_Finger_Group")

            cmds.parent(fingerCtrls[2], fingerCtrls[1])
            cmds.parent(fingerCtrls[1], fingerCtrls[0])
    applyFingerConstraints(side, fingers, fingerJoints-1)
    fingers = ["index", "middle", "ring", "pinky"]
    applyFingerConstraints(side, fingers, fingerJoints)
    correctParentingFingers()


def correctParentingFingers():
    side = ["L","R"]
    fingers = ["index","middle","ring","pinky"]
    fingerJoints = cmds.intSliderGrp(fingerCnt, q=True, value=True) - 1
    for i,j in enumerate(side):
        for k,l in enumerate(fingers):
            cmds.parent(j + "_" + l + "_" + str(fingerJoints -1) + "_Offset", j + "_" + l + "_" + str(fingerJoints -2) + "_Ctrl")
            cmds.parent(j + "_" + l + "_" + str(fingerJoints - 2) + "_Offset",j + "_" + l + "_" + str(fingerJoints - 3) + "_Ctrl")
            cmds.parent(j + "_" + l + "_" + str(fingerJoints - 3) + "_Offset",j + "_" + l + "_" + str(fingerJoints - 4) + "_Ctrl")
        cmds.parent(j + "_thumb_" + str(fingerJoints-2) + "_Offset",j + "_thumb_"+str(fingerJoints-3)+"_Ctrl")
        cmds.parent(j + "_thumb_" + str(fingerJoints - 3) + "_Offset",j + "_thumb_" + str(fingerJoints - 4) + "_Ctrl")


def applyFingerConstraints(side, fingers,fingerJoints):
    for i, j in enumerate(side):
        for k, l in enumerate(fingers):
            for z in range(0, fingerJoints):
                cmds.parentConstraint(j + "_" + l + "_" + str(z) + "_Ctrl",j + "_" + l + "_" + str(z) + "_Jnt", mo =True)
        cmds.parentConstraint(j+"_Wrist_Jnt",j+"_Finger_Group", mo = True, n= j+"_Finger_Ctrl_ParentConstraint")
        #cmds.parentConstraint(j + "_Wrist_FK_Ctrl", j + "_Finger_Group", mo=True, n=j + "_Finger_Ctrl_ParentConstraint")


#def connectFingerToSwitch():
    #side = ["L","R"]
    #for i,j in enumerate(side):
        #cmds.connectAttr(j + "_Hand_IKFK_Switch.IK_FK", j + "_Finger_Ctrl_ParentConstraint." + j + "_Hand_IK_CtrlW0")
        #cmds.connectAttr(j + "_Arm_IKFK_Reverse.outputX",j+"_Finger_Ctrl_ParentConstraint."+ j + "_Wrist_FK_CtrlW1")


def applyConstraints():
    # correcting spine_3_Ctrl pivot
    spineIndex = cmds.intSliderGrp(spineCnt, q=True, value=True)
    spinePos = cmds.xform("Spine_"+str(spineIndex - 1)+"_Jnt", q=True, t=True, ws=True)
    cmds.select("Spine_"+str(spineIndex - 1)+"_Ctrl")
    #################
    cmds.xform(piv=[spinePos[0], spinePos[1], spinePos[2]], ws=True)
    side = ["L", "R"]
    arm = ["Humerus", "Radius"]
    leg = ["Hip", "Knee", "Ankle", "Foot"]

    for i in range(0, cmds.intSliderGrp(spineCnt, q=True, value=True)):
        cmds.parentConstraint("Spine_" + str(i) + "_Ctrl", "Spine_" + str(i) + "_Jnt", mo=True,
                              n="Spine_" + str(i) + "_Ctrl_ParentConstraint")
    cmds.parentConstraint("Cog_Ctrl", "Cog_Jnt", mo=True, n="Cog_Ctrl_ParentConstraint")
    for i, j in enumerate(side):
        cmds.parent(j + "_Hand_IK_Handle",j + "_Hand_IK_Ctrl" )

        cmds.parentConstraint(j + "_Hand_IK_Ctrl", "IK_" + j + "_Wrist_Jnt",st = ["x","y","z"], mo=True,n=j + "_IK_Wrist_Ctrl_ParentConstraint")  # wrist parent constraint
        cmds.parentConstraint(j + "_Wrist_FK_Ctrl","FK_" + j + "_Wrist_Jnt",st = ["x","y","z"], mo=True,n = j + "_FK_Wrist_Ctrl_ParentConstraint")  # wrist parent constraint

        cmds.parentConstraint("FK_" + j + "_Wrist_Jnt",j + "_Wrist_Jnt", mo=True, n=j + "_Wrist_Ctrl_ParentConstraint")
        cmds.parentConstraint("IK_" + j + "_Wrist_Jnt", j + "_Wrist_Jnt", mo=True, n=j + "_Wrist_Ctrl_ParentConstraint")

        cmds.poleVectorConstraint(j + "_Hand_Pole_Ctrl", j + "_Hand_IK_Handle", n=j + "_Hand_PoleVector")
        cmds.parentConstraint(j + "_Foot_IK_Ctrl", j + "_IK_Foot_Group", mo=True, n=j + "_Leg_Ctrl_ParentConstraint")
        cmds.poleVectorConstraint(j + "_Leg_Pole_Ctrl", j + "_Leg_IK_Handle", n=j + "_Leg_PoleVector")
        cmds.parentConstraint(j + "_Hip_IK_Ctrl", "IK_" + j + "_Hip_Jnt", mo=True, n=j + "_Hip_Ctrl_ParentConstraint")
        # cmds.parentConstraint(j + "_Hip_IK_Ctrl", j + "_Ankle_Jnt", mo=True, st=["x", "y", "z"],n=j + "_Ankle_Ctrl_ParentConstraint")

        cmds.parentConstraint(j + "_Shoulder_Ctrl", j + "_Clavicle_Jnt", mo=True, n=j + "_Shoulder_Ctrl_ParentConstraint")



        for k, l in enumerate(arm):
            cmds.parentConstraint("IK_" + j + "_" + l + "_Jnt", j + "_" + l + "_Jnt", mo=True,n=j + "_" + l + "_ParentConstraint")
            cmds.parentConstraint(j + "_" + l + "_FK_Ctrl", "FK_" + j + "_" + l + "_Jnt", mo=True,n=j + "_" + l + "_FK_Ctrl_ParentConstraint")
            cmds.parentConstraint("FK_" + j + "_" + l + "_Jnt", j + "_" + l + "_Jnt", mo=True,
                                  n=j + "_" + l + "_ParentConstraint")

        for k, l in enumerate(leg):
            cmds.parentConstraint("IK_" + j + "_" + l + "_Jnt", j + "_" + l + "_Jnt", mo=True,
                                  n=j + "_" + l + "_ParentConstraint")
            cmds.parentConstraint(j+"_"+l+"_FK_Ctrl", "FK_"+j+"_"+l+"_Jnt",mo = True, n =j + "_" + l + "_FK_Ctrl_ParentConstraint")
            cmds.parentConstraint("FK_" + j + "_" + l + "_Jnt", j + "_" + l + "_Jnt", mo=True,
                                  n=j + "_" + l + "_ParentConstraint")

    cmds.parentConstraint("Head_Ctrl","Head_Jnt",mo=True)
    cmds.parentConstraint("Neck_Ctrl", "Neck_Jnt", mo=True)


def settingUpAttributes():
    side = ["L", "R"]
    for i, j in enumerate(side):
        cmds.select(j + "_Foot_IK_Ctrl")
        cmds.addAttr(ln="Foot_Roll", at="double", k=True, defaultValue=0.0, minValue=0, maxValue=100)
        cmds.addAttr(ln="Toe_Roll", at="double", k=True, defaultValue=0.0, minValue=0, maxValue=100)
        cmds.addAttr(ln="Toe_Tap", at="double", k=True, defaultValue=0.0, minValue=-100, maxValue=0)
        cmds.addAttr(ln="Toe_Twist", at="double", k=True, defaultValue=0, minValue=-50, maxValue=50)
        cmds.addAttr(ln="Heel_Roll", at="double", k=True, defaultValue=0, minValue=-50, maxValue=50)
        cmds.addAttr(ln="Heel_Twist", at="double", k=True, defaultValue=0, minValue=-50, maxValue=50)
        cmds.addAttr(ln="Bank_In", at="double", k=True, defaultValue=0, minValue=-50, maxValue=50)
        cmds.addAttr(ln="Bank_Out", at="double", k=True, defaultValue=0, minValue=-50, maxValue=50)

        cmds.connectAttr(j + "_Foot_IK_Ctrl.Foot_Roll", j + "_Rev_Foot_Jnt.rx")
        cmds.connectAttr(j + "_Foot_IK_Ctrl.Toe_Roll", j + "_Rev_Toe_Jnt.rx")
        cmds.connectAttr(j + "_Foot_IK_Ctrl.Toe_Tap", j + "_Toe_Tap.rx")
        cmds.connectAttr(j + "_Foot_IK_Ctrl.Toe_Twist", j + "_Rev_Toe_Jnt.ry")
        cmds.connectAttr(j + "_Foot_IK_Ctrl.Heel_Roll", j + "_Rev_Heel_Jnt.rx")
        cmds.connectAttr(j + "_Foot_IK_Ctrl.Heel_Twist", j + "_Rev_Heel_Jnt.ry")
        cmds.connectAttr(j + "_Foot_IK_Ctrl.Bank_In", j + "_Bank_In.rz")
        cmds.connectAttr(j + "_Foot_IK_Ctrl.Bank_Out", j + "_Bank_Out.rz")


def wiringIKFKSwitch():
    side = ["L", "R"]
    leg = ["Hip", "Knee", "Ankle", "Foot"]
    arm = ["Humerus", "Radius"]
    cmds.createNode("reverse", n="L_Leg_IKFK_Reverse")
    cmds.createNode("reverse", n="R_Leg_IKFK_Reverse")
    cmds.createNode("reverse", n="L_Arm_IKFK_Reverse")
    cmds.createNode("reverse", n="R_Arm_IKFK_Reverse")
    for i, j in enumerate(side):#legs
        cmds.connectAttr(j + "_Leg_IKFK_Switch.IK_FK", j + "_Leg_IKFK_Reverse.inputX")
        for k, l in enumerate(leg):
            cmds.connectAttr(j + "_Leg_IKFK_Reverse.outputX",
                             j + "_" + l + "_ParentConstraint.FK_" + j + "_" + l + "_JntW1")
            cmds.connectAttr(j + "_Leg_IKFK_Switch.IK_FK",
                             j + "_" + l + "_ParentConstraint.IK_" + j + "_" + l + "_JntW0")


    for i,j in enumerate(side):
        cmds.connectAttr(j + "_Hand_IKFK_Switch.IK_FK", j + "_Arm_IKFK_Reverse.inputX")
        cmds.connectAttr(j +"_Arm_IKFK_Reverse.outputX",j+"_Wrist_Ctrl_ParentConstraint.FK_"+j+"_Wrist_JntW0")
        cmds.connectAttr(j + "_Hand_IKFK_Switch.IK_FK", j+"_Wrist_Ctrl_ParentConstraint.IK_"+j+"_Wrist_JntW1")
        #cmds.connectAttr(j + "_Hand_IKFK_Switch.IK_FK", j + "_Arm_IKFK_Reverse.inputY")
        #cmds.connectAttr(j + "_Arm_IKFK_Reverse.outputY",j + "_Wrist_Jnt.blendParent1")
        for k, l in enumerate(arm):
            cmds.connectAttr(j + "_Arm_IKFK_Reverse.outputX",
                             j + "_" + l + "_ParentConstraint.FK_" + j + "_" + l + "_JntW1")
            cmds.connectAttr(j + "_Hand_IKFK_Switch.IK_FK",
                             j + "_" + l + "_ParentConstraint.IK_" + j + "_" + l + "_JntW0")


def parentingCtrls():
    side = ["L","R"]
    lastSpine = cmds.intSliderGrp(spineCnt, q=True, value=True)
    cmds.parent("Head_Ctrl","Neck_Ctrl")
    cmds.parent("Neck_Ctrl","Spine_"+str(lastSpine - 1)+"_Ctrl")
    cmds.parent("Rev_Foot_Jnt_Group","IK_Group")
    cmds.group(em=True, n="IK_Ctrl_Group")
    cmds.group(em=True, n="Control_Group")
    cmds.group(em=True, n="Rig_Group")
    cmds.parent("IK_Ctrl_Group", "Control_Group")
    cmds.parent("Cog_Ctrl", "Control_Group")
    cmds.parent("Control_Group", "Rig_Group")
    cmds.parent("IKFK_Group", "Rig_Group")
    for i,j in enumerate(side):
        cmds.parent(j + "_Hip_FK_Offset", "Hip_Ctrl")
        cmds.parent(j + "_Humerus_FK_Offset", j + "_Shoulder_Ctrl")
        cmds.group(em=True, n=j+"_Leg_IK_Ctrl_Group")
        cmds.group(em=True, n=j+"_Arm_IK_Ctrl_Group")
        cmds.parent(j+"_Hand_IK_Offset",j+"_Arm_IK_Ctrl_Group")
        cmds.parent(j + "_Hand_Pole_Ctrl", j + "_Arm_IK_Ctrl_Group")
        cmds.parent(j + "_Foot_IK_Ctrl", j + "_Leg_IK_Ctrl_Group")
        cmds.parent(j + "_Leg_Pole_Ctrl", j + "_Leg_IK_Ctrl_Group")
        cmds.parent(j + "_Leg_IK_Ctrl_Group", "IK_Ctrl_Group")
        cmds.parent(j + "_Arm_IK_Ctrl_Group", "IK_Ctrl_Group")
        cmds.parent(j+"_Hand_IKFK_Switch", "Control_Group")
        cmds.parent(j + "_Leg_IKFK_Switch", "Control_Group")
        cmds.parent(j + "_Finger_Group", "Cog_Ctrl")
        cmds.parent("FK_"+ j +"_Humerus_Jnt", j + "_Shoulder_Ctrl")

    rootScale = cmds.xform("Root", q=True, s=True)
    cmds.circle(nr=(0, 1, 0), c=(0, 0, 0), n="Global_Ctrl")
    cmds.scale(8 * rootScale[0], 8 * rootScale[0], 8 * rootScale[0], "Global_Ctrl")
    cmds.makeIdentity(apply=True)
    cmds.circle(nr=(0, 1, 0), c=(0, 0, 0), n="Translate_Ctrl")
    cmds.scale(6 * rootScale[0], 6 * rootScale[0], 6 * rootScale[0], "Translate_Ctrl")
    cmds.makeIdentity(apply=True)
    cmds.parent("Translate_Ctrl", "Global_Ctrl")
    cmds.parent("Rig_Group", "Translate_Ctrl")
    cmds.parent("Deform_Skeleton_Group", "Global_Ctrl")
    ikfkSwitchVisibility()


def ikfkSwitchVisibility():
    side = ["L","R"]
    for i,j in enumerate(side):
        #IK
        cmds.connectAttr(j+"_Hand_IKFK_Switch.IK_FK",j+"_Arm_IK_Ctrl_Group.v")
        cmds.connectAttr(j + "_Leg_IKFK_Switch.IK_FK", j + "_Leg_IK_Ctrl_Group.v")
        cmds.connectAttr(j + "_Leg_IKFK_Switch.IK_FK", j + "_Hip_IK_Ctrl.v")
        #FK
        cmds.connectAttr(j + "_Arm_IKFK_Reverse.outputX", j + "_Humerus_FK_Offset.v")
        cmds.connectAttr(j + "_Leg_IKFK_Reverse.outputX", j + "_Hip_FK_Offset.v")


def makeSets():
    if cmds.objExists("Skeleton Set"):
        cmds.delete("Skeleton Set")
        cmds.selectType(j=True)
        joints = cmds.select("Root_Jnt", hi=True)
        joints = cmds.ls(sl=True)
        newset = cmds.sets(n="Skeleton Set")
        print joints
    else:
        cmds.selectType(j=True)
        joints = cmds.select("Root_Jnt", hi=True)
        joints = cmds.ls(sl=True)
        newset = cmds.sets(n="Skeleton Set")
        print joints


def skinGeo():
    geo = cmds.ls(sl=True)
    if len(geo) == 0:
        cmds.confirmDialog(title = "Empty Selection", message = "Please select a mesh to be skinned", button = "OK")
    else:
        geo = cmds.ls(sl=True)
        cmds.group(em=True, n="GEO")
        cmds.parent(geo, "GEO")
        for i in range(0, len(geo)):
            cmds.skinCluster(geo[i], "Root_Jnt", bm=3, sm=1, dr=0.1)
        for j in range(1, len(geo) + 1):
            cmds.geomBind("skinCluster" + str(j), bm=3, gvp=[1024, 1])


# shapes
def drawTorus(name):
    vert = [(0.825, 0.087, 1.429), (0.775, 0.087, 1.342), (0.750, 0.00, 1.299), (0.775, -0.087, 1.342),
            (0.825, -0.087, 1.429), (0.850, 0.000, 1.472), (0.825, 0.087, 1.429),
            (-0.825, 0.087, 1.429), (-0.775, 0.087, 1.342), (-0.750, 0.000, 1.299), (-0.775, -0.087, 1.342),
            (-0.825, -0.087, 1.429), (-0.850, 0.000, 1.472), (-0.825, 0.087, 1.429),
            (-1.650, 0.087, 0.000), (-1.550, 0.087, 0.000), (-1.500, 0.000, 0.000), (-1.550, -0.087, 0.000),
            (-1.650, -0.087, 0.000), (-1.700, 0.000, 0.000), (-1.650, 0.087, 0.000),
            (-0.825, 0.087, -1.429), (-0.775, 0.087, -1.342), (-0.750, 0.000, -1.299), (-0.775, -0.087, -1.342),
            (-0.825, -0.087, -1.429), (-0.850, 0.000, -1.472), (-0.825, 0.087, -1.429),
            (0.825, 0.087, -1.429), (0.775, 0.087, -1.342), (0.750, 0.00, -1.299), (0.775, -0.087, -1.342),
            (0.825, -0.087, -1.429), (0.850, 0.000, -1.472), (0.825, 0.087, -1.429),
            (1.650, 0.087, 0.000), (1.550, 0.087, 0.000), (1.500, 0.000, 0.000), (1.550, -0.087, 0.000),
            (1.650, -0.087, 0.000), (1.700, 0.000, 0.000), (1.650, 0.087, 0.000),
            (0.825, 0.087, 1.429),
            (0.775, 0.087, 1.342), (-0.775, 0.087, 1.342), (-1.550, 0.087, 0.000), (-0.775, 0.087, -1.342),
            (0.775, 0.087, -1.342), (1.550, 0.087, 0.000), (0.775, 0.087, 1.342),
            (0.750, 0.00, 1.299), (-0.750, 0.000, 1.299), (-1.500, 0.000, 0.000), (-0.750, 0.000, -1.299),
            (0.750, 0.00, -1.299), (1.500, 0.000, 0.000), (0.750, 0.00, 1.299),
            (0.775, -0.087, 1.342), (-0.775, -0.087, 1.342), (-1.550, -0.087, 0.000), (-0.775, -0.087, -1.342),
            (0.775, -0.087, -1.342), (1.550, -0.087, 0.000), (0.775, -0.087, 1.342),
            (0.825, -0.087, 1.429), (-0.825, -0.087, 1.429), (-1.650, -0.087, 0.000), (-0.825, -0.087, -1.429),
            (0.825, -0.087, -1.429), (1.650, -0.087, 0.000), (0.825, -0.087, 1.429),
            (0.850, 0.000, 1.472), (-0.850, 0.000, 1.472), (-1.700, 0.000, 0.000), (-0.850, 0.000, -1.472),
            (0.850, 0.000, -1.472), (1.700, 0.000, 0.000),
            (0.850, 0.000, 1.472)]
    theCurve = cmds.curve(p=vert, n=name, d=1)
    rootScale = cmds.xform("Root", q=True, s=True, ws=True)
    cmds.scale(rootScale[0], rootScale[1], rootScale[2])
    cmds.makeIdentity(apply=True)


def drawCylinder(name):
    cylinderVert = [(1, 1, 0), (0.5, 1, -0.866), (-0.5, 1, -0.866), (-1, 1, 0), (-0.5, 1, 0.866), (0.5, 1, 0.866),
                    (1, 1, 0),
                    (1, -1, 0), (0.5, -1, -0.866), (-0.5, -1, -0.866), (-1, -1, 0), (-0.5, -1, 0.866), (0.5, -1, 0.866),
                    (1, -1, 0),
                    (0.5, -1, -0.866), (0.5, 1, -0.866), (-0.5, 1, -0.866), (-0.5, -1, -0.866), (-1, -1, 0), (-1, 1, 0),
                    (-0.5, 1, 0.866), (-0.5, -1, 0.866),
                    (0.5, -1, 0.866), (0.5, 1, 0.866)]
    theCurve = cmds.curve(p=cylinderVert, n=name, d=1)

    cmds.makeIdentity(apply=True)
    rootScale = cmds.xform("Root", q=True, s=True, ws=True)
    cmds.scale(rootScale[0], rootScale[1], rootScale[2])
    cmds.makeIdentity(apply=True)


def drawPyramid(name):
    pyramidVert = [(0, 0, 1), (1, 0, -1), (0, 1, -1), (0, 0, 1), (0, 1, -1), (-1, 0, -1), (0, 0, 1), (-1, 0, -1),
                   (0, -1, -1), (0, 0, 1), (0, -1, -1), (1, 0, -1)]
    theCurve = cmds.curve(p=pyramidVert, n=name, d=1)
    cmds.xform(piv=(0, 0, 1))
    cmds.move(0, 0, -1)
    cmds.scale(0.5, 0.5, 0.5)
    cmds.makeIdentity(apply=True)
    rootScale = cmds.xform("Root", q=True, s=True, ws=True)
    cmds.scale(rootScale[0], rootScale[1], rootScale[2])
    cmds.makeIdentity(apply=True)


def drawHalfTorus(name):
    halfTorusVert = [(0, 0, -1.1), (0.087, 0, -1.050), (0.087, 0, -0.950), (0, 0, -0.900), (-0.087, 0, -0.950),
                     (-0.087, 0, -1.050), (0, 0, -1.1),
                     (0.000, 0.550, -0.953), (0.087, 0.525, -0.909), (0.087, 0.475, -0.823), (0, 0.450, -0.779),
                     (-0.087, 0.475, -0.823), (-0.087, 0.525, -0.909), (0.000, 0.550, -0.953),
                     (0, 0.953, -0.550), (0.087, 0.909, -0.525), (0.087, 0.823, -0.475), (0.000, 0.779, -0.450),
                     (-0.087, 0.823, -0.475), (-0.087, 0.909, -0.525), (0, 0.953, -0.550),
                     (0, 1.100, 0), (0.087, 1.050, 0), (0.087, 0.950, 0), (0, 0.9, 0), (-0.087, 0.950, 0),
                     (-0.087, 1.050, 0), (0, 1.100, 0),
                     (0, 0.953, 0.550), (0.087, 0.909, 0.525), (0.087, 0.823, 0.475), (0.000, 0.779, 0.450),
                     (-0.087, 0.823, 0.475), (-0.087, 0.909, 0.525), (0, 0.953, 0.550),
                     (0.000, 0.550, 0.953), (0.087, 0.525, 0.909), (0.087, 0.475, 0.823), (0, 0.450, 0.779),
                     (-0.087, 0.475, 0.823), (-0.087, 0.525, 0.909), (0.000, 0.550, 0.953),
                     (0, 0, 1.1), (0.087, 0, 1.050), (0.087, 0, 0.950), (0, 0, 0.900), (-0.087, 0, 0.950),
                     (-0.087, 0, 1.050), (0, 0, 1.1),
                     (0.087, 0, 1.050), (0.087, 0.525, 0.909), (0.087, 0.909, 0.525), (0.087, 1.050, 0),
                     (0.087, 0.909, -0.525), (0.087, 0.525, -0.909), (0.087, 0, -1.050),
                     (0.087, 0, -0.950), (0.087, 0.475, -0.823), (0.087, 0.823, -0.475), (0.087, 0.950, 0),
                     (0.087, 0.823, 0.475), (0.087, 0.475, 0.823), (0.087, 0, 0.950),
                     (0, 0, 0.900), (0, 0.450, 0.779), (0.000, 0.779, 0.450), (0, 0.9, 0), (0.000, 0.779, -0.450),
                     (0, 0.450, -0.779), (0, 0, -0.900),
                     (-0.087, 0, -0.950), (-0.087, 0.475, -0.823), (-0.087, 0.823, -0.475), (-0.087, 0.950, 0),
                     (-0.087, 0.823, 0.475), (-0.087, 0.475, 0.823), (-0.087, 0, 0.950),
                     (-0.087, 0, 1.050), (-0.087, 0.525, 0.909), (-0.087, 0.909, 0.525), (-0.087, 1.050, 0),
                     (-0.087, 0.909, -0.525), (-0.087, 0.525, -0.909), (-0.087, 0, -1.050)]
    theCurve = cmds.curve(p=halfTorusVert, n=name, d=1)
    rootScale = cmds.xform("Root", q=True, s=True, ws=True)
    cmds.scale(rootScale[0], rootScale[1], rootScale[2])
    cmds.makeIdentity(apply=True)


def drawFootCtrl(name):
    footCtrlVert = [(0, 1, 0), (1, 1, 0), (1, 1, 1), (0, 1, 1), (0, 1, 0), (0, 0, 0), (0, 0, 3), (1, 0, 3), (1, 0, 0),
                    (0, 0, 0),
                    (0, 1, 0), (0, 1, 1), (0, 0.5, 3), (1, 0.5, 3), (1, 1, 1), (1, 1, 0), (1, 0, 0), (1, 0, 3),
                    (1, 0.5, 3),
                    (0, 0.5, 3), (0, 0, 3)]
    theCurve = cmds.curve(p=footCtrlVert, n=name, d=1)
    cmds.xform(piv=(0.5, 0, 0))
    cmds.move(-0.5, 0, 0)
    cmds.scale(1.5, 1.2, 1.2)
    cmds.makeIdentity(apply=True)
    rootScale = cmds.xform("Root", q=True, s=True, ws=True)
    cmds.scale(rootScale[0], rootScale[1], rootScale[2])
    cmds.makeIdentity(apply=True)


def drawHandShape(name):
    handCurve = cmds.textCurves(n=name, f='Wingdings 2', t='N')
    cmds.pickWalk("curve2", d="down")
    cmds.select("curve1", add=True)
    cmds.parent(s=True, r=True)
    cmds.parent("curve1", w=True)
    cmds.delete(name + "Shape")
    cmds.rename("curve1", name)


def drawAwrrowShape(name):
    arrowVert = [(-0.029, 0.00, 0.029), (0.029, 0.00, 0.029), (0.029, 0.00, -0.029), (-0.029, 0.00, -0.029),
                 (-0.029, 0.00, 0.029),
                 (-0.029, 0.7, 0.029), (0.029, 0.7, 0.029), (0.029, 0.7, -0.029), (-0.029, 0.7, -0.029),
                 (-0.029, 0.7, 0.029),
                 (0.029, 0.7, 0.029), (0.029, 0.00, 0.029), (0.029, 0.00, -0.029), (0.029, 0.7, -0.029),
                 (-0.029, 0.7, -0.029), (-0.029, 0.00, -0.029), (-0.029, 0.700, -0.029),
                 (-0.05, 0.7, -0.05), (-0.05, 0.7, 0.05), (-0.029, 0.700, 0.029), (-0.05, 0.7, 0.05), (0.05, 0.7, 0.05),
                 (0.029, 0.7, 0.029), (0.05, 0.7, 0.05), (0.05, 0.7, -0.05),
                 (0.029, 0.700, -0.029), (0.05, 0.7, -0.05), (-0.05, 0.7, -0.05),
                 (0, 1, 0), (-0.05, 0.7, 0.05), (0, 1, 0), (0.05, 0.7, 0.05), (0, 1, 0), (0.05, 0.7, -0.05)]
    theCurve = cmds.curve(p=arrowVert, n=name, d=1)


def drawPointDown(name):
    pointD = cmds.textCurves(n=name, f='Wingdings 2', t='M')
    cmds.parent("curve1", w=True)
    cmds.delete(name + "Shape")
    cmds.rename("curve1", name)


def drawCrown(name):
    crownVert = [(0, 0, 1), (0.5, 0, 0.866), (0.866, 0, 0.5), (1, 0, 0), (0.866, 0, -0.5), (0.5, 0, -0.866), (0, 0, -1),
                 (-0.5, 0, -0.866), (-0.866, 0, -0.5), (-1, 0, 0), (-0.866, 0, 0.5), (-0.5, 0, 0.866), (0, 0, 1),
                 (0, 1.5, 1), (0.5, 1, 0.866), (0.866, 1.5, 0.5), (1, 1, 0), (0.866, 1.5, -0.5), (0.5, 1, -0.866),
                 (0, 1.5, -1), (-0.5, 1, -0.866), (-0.866, 1.5, -0.5), (-1, 1, 0), (-0.866, 1.5, 0.5), (-0.5, 1, 0.866),
                 (0, 1.5, 1),
                 (0, 0, 1), (0.5, 1, 0.866), (0.866, 0, 0.5), (1, 1, 0), (0.866, 0, -0.5), (0.5, 1, -0.866), (0, 0, -1),
                 (-0.5, 1, -0.866), (-0.866, 0, -0.5), (-1, 1, 0), (-0.866, 0, 0.5), (-0.5, 1, 0.866), (0, 0, 1)]
    theCurve = cmds.curve(p=crownVert, n=name, d=1)


def drawNeckCtrl(name):
    neckCtrlVert = [(0, -0.852, 1.243), (0.477, -0.661, 1.109), (0.826, -0.025, 0.792), (0.954, 0.355, 0.151),
                 (0.826, 0.524, -0.580), (0.477, 0.338, -1.246), (0, 0.302, -1.476), (-0.477, 0.338, -1.246),
                 (-0.826, 0.524, -0.580), (-0.954, 0.355, 0.151),
                 (-0.826, -0.025, 0.792), (-0.477, -0.661, 1.109), (0, -0.852, 1.243),
                 (0, -0.529, 1.380), (0.477, -0.338, 1.246), (0.826, 0.298, 0.929), (0.954, 0.678, 0.288),
                 (0.826, 0.847, -0.443), (0.477, 0.661, -1.109), (0, 0.625, -1.339), (-0.477, 0.661, -1.109),
                 (-0.826, 0.847, -0.443), (-0.954, 0.678, 0.288),
                 (-0.826, 0.298, 0.929), (-0.477, -0.338, 1.246), (0, -0.529, 1.380),
                 (0.477, -0.661, 1.109), (0.477, -0.338, 1.246), (0.826, -0.025, 0.792), (0.826, 0.298, 0.929),
                 (0.954, 0.355, 0.151), (0.954, 0.678, 0.288), (0.826, 0.524, -0.580), (0.826, 0.847, -0.443),
                 (0.477, 0.338, -1.246), (0.477, 0.661, -1.109), (0, 0.302, -1.476), (0, 0.625, -1.339),
                 (-0.477, 0.338, -1.246), (-0.477, 0.661, -1.109), (-0.826, 0.524, -0.580), (-0.826, 0.847, -0.443),
                 (-0.954, 0.355, 0.151), (-0.954, 0.678, 0.288),
                 (-0.826, -0.025, 0.792), (-0.826, 0.298, 0.929), (-0.477, -0.661, 1.109), (-0.477, -0.338, 1.246),
                 (0, -0.852, 1.243), (0, -0.529, 1.380)]
    theCurve = cmds.curve(p=neckCtrlVert, n=name, d=1)


def drawfingerCtrl(name):
    fingerVert = [(0, 0, 0), (0, 2, 0), (0, 4, 1), (0, 4, -1), (0, 2, 0)]
    theCurve = cmds.curve(p=fingerVert, n=name, d=1)


def drawAxisGizmo(name):
    drawAwrrowShape("Yaxis")
    cmds.pickWalk("Yaxis", d="down")
    cmds.rename("Yaxis_" + name)
    drawAwrrowShape("Xaxis")
    cmds.rotate(0,0,-90)
    cmds.makeIdentity(apply = True)
    drawAwrrowShape("Zaxis")
    cmds.rotate(90, 0, 0)
    cmds.makeIdentity(apply=True)

    cmds.pickWalk("Zaxis", d="down")
    cmds.rename("Zaxis_"+name)
    cmds.select("Yaxis",add = True)
    cmds.parent(s=True, r=True)
    cmds.pickWalk("Xaxis", d="down")
    cmds.rename("Xaxis_"+name)
    cmds.select("Yaxis", add=True)
    cmds.parent(s=True, r=True)
    cmds.delete("Xaxis")
    cmds.delete("Zaxis")
    cmds.rename("Yaxis",name, ignoreShape = True)
##############################

def colorCtrls():
    cmds.setAttr("Global_Ctrl.overrideEnabled", 1)
    cmds.setAttr("Global_Ctrl.overrideColor", 31)
    cmds.setAttr("Translate_Ctrl.overrideEnabled", 1)
    cmds.setAttr("Translate_Ctrl.overrideColor", 16)
    cmds.setAttr("Cog_Ctrl.overrideEnabled", 1)
    cmds.setAttr("Cog_Ctrl.overrideColor", 17)
    cmds.setAttr("Hip_Ctrl.overrideEnabled", 1)
    cmds.setAttr("Hip_Ctrl.overrideColor", 18)
    cmds.setAttr("Spine_0_Ctrl.overrideEnabled", 1)
    cmds.setAttr("Spine_0_Ctrl.overrideColor", 20)
    cmds.setAttr("Neck_Ctrl.overrideEnabled", 1)
    cmds.setAttr("Neck_Ctrl.overrideColor", 9)
    side = ["L","R"]
    items = ["_Leg_IK_Ctrl_Group","_Arm_IK_Ctrl_Group","_Finger_Group","_Hand_IKFK_Switch","_Leg_IKFK_Switch","_Shoulder_Ctrl","_Eye_Ctrl","_Hip_FK_Offset","_Hip_IK_Ctrl"]
    for i,j in enumerate(side):
        for k,l in enumerate(items):
            cmds.setAttr(j+l+".overrideEnabled", 1)
    for i,j in enumerate(items):
        cmds.setAttr(side[0] + j+ ".overrideColor", 14)
        cmds.setAttr(side[1] + j + ".overrideColor", 13)

def cleanUp():
    cmds.setAttr("IKFK_Group.visibility", 0)
    cmds.setAttr("IK_L_Humerus_Jnt.visibility", 0)
    cmds.setAttr("IK_R_Humerus_Jnt.visibility", 0)
    unwanted = cmds.ls("FK_*")
    cmds.sets(unwanted, rm="Skeleton_Set")
    unwanted = cmds.ls("IK_*")
    cmds.sets(unwanted, rm="Skeleton_Set")
