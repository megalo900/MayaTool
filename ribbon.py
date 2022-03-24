import maya.cmds as cmds
import maya.mel as mel
newWindow = "Test Window"


def main():
    if cmds.window(newWindow, exists=True):
        cmds.deleteUI(newWindow)
        print "window already exists"
    else:
        UI()


def UI():
    global ribbonName
    mainWindow = cmds.window(newWindow,menuBar = True, title="RibbonTool", iconName='RibbonTool', widthHeight=(40, 100))
    '''
    cmds.menu(label='File', tearOff=True)
    cmds.menuItem(label='New')
    cmds.menuItem(label='Open')
    cmds.menuItem(label='Save')
    cmds.menuItem(divider=True)
    cmds.menuItem(label='Quit')
    cmds.menu(label='Help', helpMenu=True)
    cmds.menuItem('Application..."', label='"About')
    '''
    cmds.scrollLayout("scroll")

    cmds.rowColumnLayout(nc=1)
    cmds.image(image='D:\Python_projects\Maya\_ribbon-black-banner.png')
    #cmds.rowColumnLayout(nc=2)
    cmds.frameLayout(l="Joint Setup", cll=True)
    cmds.rowColumnLayout(nc=2)
    cmds.text("Name Ribbon", w = 100)
    ribbonName = cmds.textField("Name Ribbon", w = 100)
    cmds.separator(height=20)
    cmds.separator(height=20)
    cmds.button(l="Select Edge 1", w=100, c = "SelectCurve(1)")
    cmds.button(l="Select Edge 2", w=100, c = "SelectCurve(2)")
    cmds.setParent('..')
    cmds.rowColumnLayout(nc=1)
    cmds.button(l="Make Ribbon", w=200, c="MakeRibbon()")
    cmds.separator(height=20)
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.frameLayout(l="Control Setup", cll=True)


    cmds.rowColumnLayout(nc=1)
    cmds.separator(height=20)
    cmds.text("First Select The Joints Where", w=100)
    cmds.text("The Controls will Be Placed", w=100)
    cmds.separator(height=20)
    cmds.button(l="Make Ctrls", w=200, c="MakeCtrls()")

    cmds.separator(height=20)
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.frameLayout(l="Accessibility", cll=True)
    cmds.rowColumnLayout(nc=1)
    cmds.button(l="Select Bind Joints", w=200, c="SelectBindJoints()")
    cmds.showWindow(mainWindow)

main()


def SelectCurve(part):
    selected = cmds.ls(sl = True)
    if part == 1:
        cmds.polyToCurve(n= "FirstCurve", degree =3)
    if part == 2:
        cmds.polyToCurve(n= "SecondCurve", degree= 3)

def MakeRibbon():
    name = cmds.textField(ribbonName, q=True, tx=True)
    if cmds.objExists("{}_follicles_grp".format(name)) == False:
        if name == "":
            print("Name Ribbon")
        else:
            surface = cmds.loft("FirstCurve","SecondCurve", n = "{}_RibbonSurface".format(name),ch = False,c=False, u = True, po = 0, d = 1, ar = True, ss = 1, rn = False, rsn = True)
            cmds.setAttr("{}_RibbonSurface.visibility".format(name), 0)
            MakeHair(name)
            cmds.delete("FirstCurve", "SecondCurve")
            grp = cmds.createNode("transform", n = "{}_ribbon_grp".format(name))

            cmds.parent(surface, grp)
            cmds.parent("{}_follicles_grp".format(name), grp)
    cmds.select(cl = True)



def MakeHair(name):
    cvs = cmds.getAttr("FirstCurve.spans")
    if cmds.objExists("hairSystem1") == False:
        hairSys = mel.eval("createHair {} 1 6 0 0 1 0 2.6122 0 2 2 1;".format(cvs+1))
        cmds.delete("hairSystem1OutputCurves")
        cmds.delete("hairSystem1")
        cmds.delete("nucleus1")
        cmds.rename("hairSystem1Follicles", "{}_follicles_grp".format(name))
    fols = cmds.listRelatives("{}_follicles_grp".format(name))
    num = 1
    for i in fols:
        x = cmds.rename(i, "{}_follicles{}".format(name,num))
        cmds.setAttr("{}_folliclesShape{}.visibility".format(name,num), 0)
        pos = cmds.xform(x, q = True, t = True, ws = True)
        curves = cmds.listRelatives(x, ad = True)
        cmds.delete(curves[2])
        CreateJoints(name, num,pos, x)
        num = num + 1
        #cmds.delete("curve{}".format(num))

def CreateJoints(name, num,pos, prnt):
    jnt = cmds.joint(p = pos, n = "{}_ribbon_joint_{}".format(name, num))
    cmds.parent(jnt ,prnt)

def scaleLocator(amount, name):
    cmds.scale(amount, amount, amount, name)

def MakeCtrls():
    selection = cmds.ls(sl = True)
    name = cmds.textField(ribbonName, q=True, tx=True)
    ctrlGrp = cmds.createNode("transform", n="{}_Ribbon_Ctrls".format(name))
    for i in selection:
        cmds.duplicate(i, n = "{}_ctrl_joint".format(i), ic = False)
        index = i.split("_")
        numb = index[len(index) - 1]

        pos = cmds.xform(i, q = True, t = True, ws = True)
        rot = cmds.xform("{}_follicles{}".format(name, numb), q = True, ro =True, ws = True)
        grp = cmds.createNode("transform", n="ctrl_Offset_{}".format(i))
        cmds.parent("ctrl_Offset_{}".format(i), ctrlGrp)
        sphere = cmds.sphere(p=(0, 0, 0), n="ctrl_{}".format(i))
        cmds.parent("ctrl_{}".format(i), "ctrl_Offset_{}".format(i))

        cmds.setAttr("ctrl_Offset_{}.translateX".format(i), pos[0])
        cmds.setAttr("ctrl_Offset_{}.translateY".format(i), pos[1])
        cmds.setAttr("ctrl_Offset_{}.translateZ".format(i), pos[2])
        cmds.setAttr("ctrl_Offset_{}.rotateX".format(i), rot[0])
        cmds.setAttr("ctrl_Offset_{}.rotateY".format(i), rot[1])
        cmds.setAttr("ctrl_Offset_{}.rotateZ".format(i), rot[2])
        cmds.parent("{}_ctrl_joint".format(i), "ctrl_{}".format(i))
        scaleLocator(0.2, "ctrl_{}".format(i))
        cmds.joint("{}_ctrl_joint".format(i), e = True, rad = 10)
    SkinJoints()
    cmds.setAttr("{}_ribbon_grp.visibility".format(name), 0)
    if cmds.objExists("{}_Ribbon".format(name)):
        cmds.parent("{}_Ribbon_Ctrls".format(name), "{}_Ribbon".format(name))
        cmds.parent("{}_ribbon_grp".format(name), "{}_Ribbon".format(name))
    else:
        cmds.createNode("transform", n = "{}_Ribbon".format(name))
        cmds.parent("{}_Ribbon_Ctrls".format(name), "{}_Ribbon".format(name))
        cmds.parent("{}_ribbon_grp".format(name), "{}_Ribbon".format(name))




def SkinJoints():
    controlJoints = []
    name = cmds.textField(ribbonName, q=True, tx=True)
    ctrlJoint = cmds.listRelatives("{}_Ribbon_Ctrls".format(name), allDescendents =True)
    #print(ctrlJoint)
    for i in ctrlJoint:
        if cmds.objectType(i) == "joint":
            controlJoints.append(i)

    cmds.skinCluster("{}_RibbonSurface".format(name), controlJoints, bm=0, sm=2, dr=4.0)
    #cmds.geomBind("skinCluster" + str(j), bm=3, gvp=[1024, 1])
    for i in controlJoints:
        cmds.setAttr("{}.visibility".format(i), 0)

def SelectBindJoints():
    name = cmds.textField(ribbonName, q=True, tx=True)
    everything = cmds.listRelatives("{}_follicles_grp".format(name), ad=True)
    joints = []
    for i in everything:
        if cmds.objectType(i) == "joint":
            joints.append(i)
    cmds.select(joints)