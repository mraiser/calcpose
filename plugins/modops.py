#!/usr/bin/python3
# -*- coding: utf-8 -*-

from .abstractop import AbstractOp
from core import G
import mh
import json

class SocketModifierOps(AbstractOp):

    def __init__(self, sockettaskview):
        super().__init__(sockettaskview)
        self.functions["applyModifier"] = self.applyModifier
        self.functions["getAppliedTargets"] = self.getAppliedTargets
        self.functions["getAvailableModifierNames"] = self.getAvailableModifierNames

    def getAvailableModifierNames(self,conn,jsonCall):
        jsonCall.data = self.api.modifiers.getAvailableModifierNames()

    def getAppliedTargets(self,conn,jsonCall):
        jsonCall.data = self.api.modifiers.getAppliedTargets()

    def applyModifier(self,conn,jsonCall):
        modifierName = jsonCall.getParam("modifier")
        if modifierName == 'all':
            values = jsonCall.getParam("power")
            for modifierName in values:
                power = values[modifierName]
                modifier = self.api.internals.getHuman().getModifier(modifierName)
                modifier.setValue(power)
                # jsonCall.setParam("modifier", modifier);
                # jsonCall.setParam("power", power);
                # self.applyModifier(conn, jsonCall)
            self.api.modifiers._threadSafeApplyAllTargets()
            jsonCall.setData("OK")
            return
        power = float(jsonCall.getParam("power"))

        if modifierName.startswith('camera/'):
            cmd = modifierName[7:]
            if cmd == 'reset':
                G.app.selectedHuman.setPosition([0.0, 0.0, 0.0])
                G.app.modelCamera.setPosition([0.0, 0.9, 0.0])
                G.app.modelCamera.setRotation([0.0, 0.0, 0.0])
                G.app.modelCamera.zoomFactor = 7
            elif cmd == 'snapshot':
                G.app.redraw()
                img = mh.grabScreen(0, 0, G.windowWidth, G.windowHeight)
                fname = jsonCall.getParam("filename")
                img.save(fname)
            elif cmd == 'zoom':
                G.app.modelCamera.zoomFactor = power
                G.app.redraw()
            elif (cmd.startswith('rot_')):
                axis = -1
                if cmd.endswith('x'): axis = 0
                elif cmd.endswith('y'): axis = 1
                elif cmd.endswith('z'): axis = 2
                G.app.rotateCamera(axis, power * 180)
            elif (cmd.startswith('trans_')):
                axis = -1
                if cmd.endswith('x'): axis = 0
                elif cmd.endswith('y'): axis = 1
                elif cmd.endswith('z'): axis = 2
                if axis != -1:
                    c = G.app.selectedHuman.getPosition()
                    c[axis] = power
                    G.app.selectedHuman.setPosition(c)
            elif (cmd.startswith('pan_')):
                axis = -1
                if cmd.endswith('x'): axis = 0
                elif cmd.endswith('y'): axis = 1
                elif cmd.endswith('z'): axis = 2
                G.app.panCamera(axis, power)
            return

        modifier = self.api.internals.getHuman().getModifier(modifierName)
        #print('MODIFYING: '+modifierName)
        #G.app.panUp()
        #G.app.axisView([0.0, 0.0, 0.0])
        #G.app.resetView()
        #G.app.rotateCamera(1,10)
        #G.app.rightView()
        #object_methods = [method_name for method_name in dir(G.app)]
        #for m in object_methods: print('- '+m)

        if not modifier:
            jsonCall.setError("No such modifier")
            return

        self.api.modifiers.applyModifier(modifierName,power,True)
        jsonCall.setData("OK")



