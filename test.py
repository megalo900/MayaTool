import maya.cmds as cmds



newWindow = "Test Window"
def creatLocator(*args):
    print "pressed"
    cmds.spaceLocator(p=(1, 1, 0))
def main():
    if cmds.window(newWindow, exists=True):
        cmds.deleteUI(newWindow)
        print "window already exists"
    else:
        UI()
def UI():

    mainWindow = cmds.window(newWindow, title="Test Window", iconName='Test Window', widthHeight=(200, 55),
                             bgc=(0.5, 1.0, 0.5))
    cmds.columnLayout(adjustableColumn=True)
    cmds.button(label='Create locators', command=creatLocator)


    cmds.showWindow(mainWindow)

main()



























