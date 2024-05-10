import maya.cmds as mc
import pymel.core as pm
from PySide2 import QtCore, QtGui
from PySide2.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSlider, QLabel

def IsMesh(obj):
    shapes = mc.listRelatives(obj, s =True)
    if not shapes:
        return False
    for s in shapes:
        if mc.objectType(s) == "mesh":
            return True
    return False

def IsCurve(obj):
    return mc.objectType(obj) == 'transform'


class BuildCable:
    def __init__(self):
        self.spline = []
        self.profile = []
        self.divValue = 40

    def BuildCableForPrflSpln(self):
        if not self.profile:
            print("Please select a profile mesh")
            return
        if not self.spline:
            print("Please select a curve")
            return
        print(self.spline)
        print(self.profile)

        startTime = mc.playbackOptions(q = True, min = True)
        endTime = mc.playbackOptions(q = True, max = True)
        dup = mc.duplicate(self.profile)[0]
        
        motionPath = mc.pathAnimation(dup, self.spline, fm=True, f=True, fa='y', ua='x', wut='vector', wu=(0,1,0), startTimeU = startTime, endTimeU = endTime)
        
        mc.matchTransform(self.profile, dup)
        mc.delete(motionPath)
        mc.delete(dup)

        mc.select(f"{self.profile}.f[:]", r=True)
        mc.select(self.spline, add=True)

        mc.polyExtrudeFacet(inputCurve = self.spline, d = self.divValue)


    def SetPrfl(self):
        profile = mc.ls(sl=True)[0]
        if not IsMesh(profile):
            print("Please Select Model")
            return
        self.profile = profile

    def SetSpln(self):
        selected_objects = mc.ls(sl=True)
        selected_curve = None
        for obj in selected_objects:
            shapes = mc.listRelatives(obj, shapes=True, type="nurbsCurve")
        if shapes:
            self.spline = shapes[0]
        else: 
            print("Please select a curve")
            return

class BuildCableWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.masterLayout = QVBoxLayout()
        self.setLayout(self.masterLayout)

        self.setWindowTitle("Build Cable")
        self.setGeometry(0,0,300,300)

        setProfBtn = QPushButton("Set Profile")
        setProfBtn.clicked.connect(self.SetProfileBtnClicked)
        self.masterLayout.addWidget(setProfBtn)

        setSplinBtn = QPushButton("Set Spline")
        setSplinBtn.clicked.connect(self.SetSplinBtnClicked)
        self.masterLayout.addWidget(setSplinBtn)

        buildBtn = QPushButton("Build Cable")
        buildBtn.clicked.connect(self.BuildCableBtnClicked)
        self.masterLayout.addWidget(buildBtn)

        hintLabel = QLabel("Extrude Devisions:")        
        self.masterLayout.addWidget(hintLabel)
        extrudeDivSlider = QSlider()
        extrudeDivSlider.setOrientation(QtCore.Qt.Horizontal)
        extrudeDivSlider.setRange(1,100)
        extrudeDivSlider.setTickInterval(10)
        extrudeDivSlider.valueChanged.connect(self.DivSliderChange)
        self.masterLayout.addWidget(extrudeDivSlider)

        self.adjustSize()

        self.builder = BuildCable()

    def BuildCableBtnClicked(self):
        self.builder.BuildCableForPrflSpln()

    def DivSliderChange(self,newVal):
        self.divValue = newVal
        print(f"New extrusion division value is: {self.divValue}")

    def SetProfileBtnClicked(self):
        self.builder.SetPrfl()

    def SetSplinBtnClicked(self):
        self.builder.SetSpln()


buildCableWidget = BuildCableWidget()
buildCableWidget.show()     