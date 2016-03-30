# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import serial
import serial.tools.list_ports
import threading
import time
from boto.dynamodb.condition import NULL

###########################################################################
## Class Main
###########################################################################

  
class Main ( wx.Frame ):
    
    def __init__( self, parent ):
        
        self.running = False
        self.data = list()
        self.ser = NULL
        
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Arduino Serial Monitor", pos = wx.DefaultPosition, size = wx.Size( 750,550 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        bSizer4 = wx.BoxSizer( wx.VERTICAL )
        
        bSizer7 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.textInput = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_READONLY )
        self.textInput.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        self.textInput.SetMaxSize( wx.Size( 200,-1 ) )
        
        bSizer7.Add( self.textInput, 1, wx.EXPAND, 5 )
        
        bSizer8 = wx.BoxSizer( wx.VERTICAL )
        
        self.graph = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.graph.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )
        self.graph.SetMinSize( wx.Size( -1,512 ) )
        
        bSizer8.Add( self.graph, 4, wx.EXPAND |wx.ALL, 0 )
        
        
        bSizer7.Add( bSizer8, 3, wx.EXPAND, 5 )
        
        
        bSizer4.Add( bSizer7, 1, wx.EXPAND, 5 )
        
        bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.save_button = wx.Button( self, wx.ID_ANY, u"Save Data", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer6.Add( self.save_button, 0, wx.ALL, 5 )
        
        self.start_button = wx.Button( self, wx.ID_ANY, u"Start", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer6.Add( self.start_button, 1, wx.ALL, 5 )
        
        self.stop_button = wx.Button( self, wx.ID_ANY, u"Stop", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer6.Add( self.stop_button, 1, wx.ALIGN_CENTER|wx.ALL, 5 )
        
        self.connect = wx.Button( self, wx.ID_ANY, u"Connect", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer6.Add( self.connect, 1, wx.ALL, 5 )
        
        connectionsChoices = []
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            connectionsChoices.append(p[0])
        self.connections = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, connectionsChoices, 0 )
        self.connections.SetSelection( 0 )
        bSizer6.Add( self.connections, 0, wx.ALL, 5 )
        
        
        bSizer4.Add( bSizer6, 0, wx.ALIGN_CENTER|wx.EXPAND, 5 )
        
        
        self.SetSizer( bSizer4 )
        self.Layout()
        self.status = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
        self.status.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
        self.status.SetForegroundColour( wx.Colour( 255, 0, 0 ) )
        
        self.Centre( wx.BOTH )
        
        # Connect Events
        self.textInput.Bind( wx.EVT_SET_FOCUS, self.hideCarat )
        self.start_button.Bind( wx.EVT_BUTTON, self.onStart )
        self.stop_button.Bind( wx.EVT_BUTTON, self.onStop )
        self.save_button.Bind( wx.EVT_BUTTON, self.getStats )
        self.connect.Bind( wx.EVT_BUTTON, self.initializeSerialConnection )
        self.connections.Bind( wx.EVT_CHOICE, self.initializeSerialConnection )
        self.graph.Bind(wx.EVT_PAINT, self.onPaint)
        self.graph.Bind( wx.EVT_SIZE, self.updateGraph )
    
    def __del__( self ):
        pass

    def getStats(self, event):
        print(self.graph.GetSize())
        self.graph.Refresh()
        for d in self.data:
            print d

    def onPaint(self, event=None):
        self.dc = wx.PaintDC(self.graph)
        self.dc.Clear()
        self.drawGraph(self.dc)
#        dc.SetPen(wx.Pen(wx.BLACK, 2))
#        self.dc.DrawLine(0, 0, self.getGraphHeight(), 50)
    
    def drawGraph(self, dc):
        font = wx.Font(pointSize = 10, family = wx.DEFAULT,
               style = wx.NORMAL, weight = wx.NORMAL,
               faceName = 'Consolas')
        dc.SetFont(font)
        XMarkings=25
        YMarkings=25
        HEIGHT=self.getGraphHeight() - XMarkings
        WIDTH=self.getGraphWidth()
        HR=float(HEIGHT)/1024
        INTERVAL=100
        data = self.data
        lastValue=0
        dc.SetPen(wx.Pen(wx.BLUE, 1)) 
        i=0
        while (i < (1024/INTERVAL) + 1):
            dc.DrawText(str(i * INTERVAL), 0, HEIGHT - i * INTERVAL * HR - 7)
            dc.DrawLine(YMarkings + 0, HEIGHT - i * INTERVAL * HR, WIDTH, HEIGHT - i * INTERVAL * HR)
            i+=1;
        j=0
        dc.SetPen(wx.Pen(wx.BLACK, 2))           
        for value in data[1:data.__sizeof__()]:
            print("test")
            dc.DrawLine(YMarkings + j, HEIGHT - int(lastValue) * HR, YMarkings + j+1, HEIGHT - (int(value) * HR))
#            pygame.draw.line(windowSurface, BLACK, (j, HEIGHT - lastValue * HR), (j+1, HEIGHT - value * HR))
            lastValue=value
            j+=1;
            
    def updateGraph(self, event):
        self.graph.Refresh()
        
    def getGraphHeight(self):
        return self.graph.GetSize()[1]
    
    def getGraphWidth(self):
        return self.graph.GetSize()[0]
        
    # Virtual event handlers, overide them in your derived class
    def onStart( self, event ):
        print(self.connections.GetStringSelection())
        print(self.running)
        if (self.ser == NULL):
            self.status.SetStatusText("There are no connected devices")
            return
        if (self.running == False):
            self.status.SetStatusText("")
            self.running = True
            thread = threading.Thread(target=self.LongRunning)
            thread.start()
        
    def onStop(self, event):
        self.running = False
        
    def LongRunning(self):
        while self.running:
            text = self.collectSerial()
            wx.CallAfter(self.textInput.AppendText, (text + "\n"))
#            wx.CallAfter(self.writeSerial(text))
            time.sleep(.001)
            self.graph.Refresh()
        
    def listConnections(self, value):
        port = self.connections.GetStringSelection()
        print(port)

    def initializeSerialConnection(self, connection):
        conn = self.connections.GetStringSelection()
        if (conn == ""):
            self.status.SetStatusText("There are no connected devices")
            return
        if (self.ser != NULL and self.ser.portstr == conn):
            self.status.SetStatusText("Already Connected to Port: " + self.ser.portstr)
            return
        self.ser = serial.Serial(conn)
        print(self.ser)
        print("connected to: " + self.ser.portstr)
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.read(5)

    def collectSerial(self):
        input = self.ser.readline().rstrip()
        self.data.append(input)
        return input

    def writeSerial(self, text):
        self.textInput.AppendText(str(text) + "\n")
        
        
    def hideCarat(self, event):
        self.textInput.ShowNativeCaret(False)
        event.Skip()
    

app = wx.App(False)

frame = Main(None)
frame.Show()
app.MainLoop()