import maya.cmds as cmds
newWindow = "Test Window"


def main():
    if cmds.window(newWindow, exists=True):
        cmds.deleteUI(newWindow)
        print "window already exists"
    else:
        UI()


def UI():
    mainWindow = cmds.window(newWindow, title="JawTool", iconName='JawTool', widthHeight=(40, 40))

    cmds.rowColumnLayout(nc=2)

    #cmds.iconTextButton(style='iconOnly',image1='D:\Python_projects\Maya\_bezier.png',label='Cylinder', c = "testFunction()")
    cmds.image(image='D:\Python_projects\Maya\_bezier.png')
    cmds.image(image='D:\Python_projects\Maya\_bezier.png')
    cmds.button(l="Select Up Edge", w=200, c = "SelectUpperCurve(1)")
    cmds.button(l="Select Low Edge", w=200, c = "SelectUpperCurve(2)")
    cmds.separator(height=20)
    cmds.separator(height=20)
    cmds.button(l="Create Joints", w=200, c="CreateJoints()")
    cmds.separator(height=20)
    cmds.separator(height=20)
    cmds.separator(height=20)
    cmds.button(l="Select Upper Mid Joint", w=200, c="FinaliseJoints()")
    cmds.button(l="Select Lower Mid Joint", w=200, c="FinaliseJoints()")

    cmds.showWindow(mainWindow)

main()



def SelectUpperCurve(part):
    selected = cmds.ls(sl = True)
    if part == 1:
        cmds.polyToCurve(n= "UpperCurve", degree =1)
    if part == 2:
        cmds.polyToCurve(n= "LowerCurve", degree= 1)

def CreateJoints():
    curves = ["Upper", "Lower"]
    for i in curves:
        grp = cmds.createNode("transform", n="{}Lip_Jnts".format(i))
        curve = cmds.select("{}Curve".format(i))
        cvs = cmds.getAttr( "{}Curve.spans".format(i))
        midJoint = (cvs)/2

        for j in range(cvs):
            pos = cmds.pointPosition("{}Curve.cv[{}]".format(i,j))
            cmds.select(cl=True)
            jnt = cmds.joint(n="{}_jnt_{:02d}".format(i,j), p=pos)
            cmds.parent(jnt, grp)
            cmds.select(cl=True)
        for k in range(midJoint):
            print(k,i)

