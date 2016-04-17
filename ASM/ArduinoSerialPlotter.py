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
from wx.lib.buttons import GenButton

###########################################################################
## Class Main
###########################################################################

class Graph ( wx.Panel):
    
    def __init__( self, *args, **kwargs ):
        self.data = list()
        self.XMarkings=25
        self.YMarkings=25
        self.MaxValue=1024
        self.MinValue=0
        self.font = wx.Font(pointSize = 10, family = wx.DEFAULT,
               style = wx.NORMAL, weight = wx.NORMAL,
               faceName = 'Consolas')
        
     
        wx.Panel.__init__ ( self, *args, **kwargs )
        self.SetDoubleBuffered(True)
        
        self.Bind( wx.EVT_SIZE, self.updateGraph )
        self.Bind(wx.EVT_PAINT, self.onPaint)
        
    def onPaint(self, event=None):        
        self.dc = wx.PaintDC(self)
        self.dc.Clear()
        self.draw(self.dc)    

    def draw(self, dc):
        dc.SetFont(self.font)
        HEIGHT=self.getGraphHeight() - self.XMarkings
        WIDTH=self.getGraphWidth()
        
        if (self.MaxValue > 500):
            INTERVAL=100
            PADDING=25
        elif (self.MaxValue <= 500 and self.MaxValue > 200):
            INTERVAL=50
            PADDING=16
        elif (self.MaxValue <= 200 and self.MaxValue > 100):
            INTERVAL=20
            PADDING=11
        elif (self.MaxValue <= 100 and self.MaxValue >= 20):
            INTERVAL=10
            PADDING=5
        else:
            INTERVAL=2
            PADDING=3
            
        GRAPH_SIZE=self.MaxValue + PADDING
        HR=float(HEIGHT)/GRAPH_SIZE
        data = self.data
        
        # Draw Grid Lines
        dc.SetPen(wx.Pen(wx.BLUE, 1)) 
        i=0
        while (i < (GRAPH_SIZE/INTERVAL) + 1):
            
            dc.DrawText(str(i * INTERVAL), 0, HEIGHT - i * INTERVAL * HR - 7)
            dc.DrawLine(self.YMarkings + 0, HEIGHT - i * INTERVAL * HR, WIDTH, HEIGHT - i * INTERVAL * HR)
            i+=1;
        
        # Draw Data Line
        if (len(data) < 2):
            lastValue = 0
        else:
            lastValue=data[1]
        j=0
        dc.SetPen(wx.Pen(wx.BLACK, 2))           
        for value in data[1:data.__sizeof__()]:
            dc.DrawLine(self.YMarkings + j, HEIGHT - int(lastValue) * HR, self.YMarkings + j+1, HEIGHT - (int(value) * HR))
            lastValue=value
            j+=1;
            
    def setData(self, data):
        self.data = data
#        self.MaxValue = int(max(data))
#        print int(max(data))
#        print self.MaxValue
        
    def setMax(self, max):
        self.MaxValue = max
        self.updateGraph()
        
    def setMin(self, min):
        self.MinValue = min    
    
    def updateGraph(self, *args):
        self.Refresh()

    def getGraphHeight(self):
        return self.GetSize()[1]
    
    def getGraphWidth(self):
        return self.GetSize()[0]
  
class Main ( wx.Frame ):
    
    def __init__( self, parent ):
        
        self.drag = False
        self.running = False
        self.data = list()
        self.ser = NULL
        
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 750,550 ), style = wx.MAXIMIZE_BOX|wx.RESIZE_BORDER|wx.NO_BORDER|wx.TAB_TRAVERSAL )
        
#        self.SetBackgroundColour( wx.Colour( 5, 88, 100 ) )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        bSizer4 = wx.BoxSizer( wx.VERTICAL )
        
        bSizer8 = wx.BoxSizer( wx.HORIZONTAL )
        
        bSizer8.AddSpacer( ( 0, 0), 0, wx.EXPAND|wx.LEFT, 5 )
        
        self.m_bitmap2 = wx.StaticBitmap( self, wx.ID_ANY, wx.Bitmap( u"img/iconmonstr-chart-16-32.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer8.Add( self.m_bitmap2, 0, wx.TOP|wx.RIGHT, 3 )
        
        self.titleText = wx.StaticText( self, wx.ID_ANY, u"Arduino Serial Monitor", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.titleText.Wrap( -1 )
        self.titleText.SetFont( wx.Font( 18, 70, 90, 92, False, "Nevis" ) )
        
        bSizer8.Add( self.titleText, 1, wx.ALL, 5 )
        
        self.resize_button = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( u"img/iconmonstr-resize-8-24.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        bSizer8.Add( self.resize_button, 0, wx.ALL, 3 )
        
        self.close_button = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( u"img/iconmonstr-x-mark-1-24.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        bSizer8.Add( self.close_button, 0, wx.ALL|wx.EXPAND, 3 )
        
        
        bSizer4.Add( bSizer8, 0, wx.EXPAND, 5 )
        
        self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer4.Add( self.m_staticline1, 0, wx.EXPAND|wx.RIGHT|wx.LEFT, 5 )
        
        bSizer7 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.textInput = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_READONLY )
        self.textInput.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        self.textInput.SetMaxSize( wx.Size( 200,-1 ) )
        
        bSizer7.Add( self.textInput, 1, wx.EXPAND |wx.ALL, 5 )
        
        bSizer8 = wx.BoxSizer( wx.HORIZONTAL )
        
        SliderSizer = wx.BoxSizer( wx.VERTICAL )
        
        self.max_slider = wx.Slider( self, wx.ID_ANY, 1024, 0, 1024, wx.DefaultPosition, wx.DefaultSize, wx.SL_INVERSE|wx.SL_VERTICAL )
        self.max_slider.SetForegroundColour( wx.Colour( 255, 128, 0 ) )
        
        SliderSizer.Add( self.max_slider, 1, wx.ALL|wx.EXPAND, 5 )
        
        self.min_slider = wx.Slider( self, wx.ID_ANY, 0, 0, 1024, wx.DefaultPosition, wx.DefaultSize, wx.SL_INVERSE|wx.SL_VERTICAL )
        SliderSizer.Add( self.min_slider, 1, wx.ALL, 5 )
        
        
        bSizer8.Add( SliderSizer, 0, wx.EXPAND, 5 )
        
        self.graph = Graph( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.graph.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )
        self.graph.SetMinSize( wx.Size( -1,512 ) )
        
        bSizer8.Add( self.graph, 4, wx.EXPAND |wx.ALL, 5 )
        
        
        bSizer7.Add( bSizer8, 3, wx.EXPAND, 5 )
        
        
        bSizer4.Add( bSizer7, 1, wx.EXPAND, 5 )
        
        self.m_staticline2 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer4.Add( self.m_staticline2, 0, wx.EXPAND|wx.RIGHT|wx.LEFT, 5 )
        
        bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.test_button = GenButton(self, wx.ID_ANY, "Test", wx.DefaultPosition, wx.DefaultSize,style=wx.BORDER_SIMPLE)
        #wx.Button( self, wx.ID_ANY, u"Save Data", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer6.Add( self.test_button, 0, wx.ALL, 5 )
        
        self.save_button = wx.Button( self, wx.ID_ANY, u"Save Data", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer6.Add( self.save_button, 0, wx.ALL, 5 )
        
        self.start_button = wx.Button( self, wx.ID_ANY, u"Start", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer6.Add( self.start_button, 1, wx.ALL, 5 )
        
        self.stop_button = wx.Button( self, wx.ID_ANY, u"Stop", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer6.Add( self.stop_button, 1, wx.ALIGN_CENTER|wx.ALL, 5 )
        
        self.clear_button = wx.Button( self, wx.ID_ANY, u"Clear", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer6.Add( self.clear_button, 1, wx.ALIGN_CENTER|wx.ALL, 5 )
        
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
        self.save_button.Bind( wx.EVT_BUTTON, self.saveFile )
        self.clear_button.Bind( wx.EVT_BUTTON, self.onClear )
#        self.save_button.Bind( wx.EVT_BUTTON, self.getStats )
        self.connect.Bind( wx.EVT_BUTTON, self.initializeSerialConnection )
        self.connections.Bind( wx.EVT_CHOICE, self.initializeSerialConnection )
        self.max_slider.Bind( wx.EVT_SCROLL_THUMBTRACK, self.UpdateMax )
        self.min_slider.Bind( wx.EVT_SCROLL_CHANGED, self.UpdateMin )
        
        
        self.titleText.Bind( wx.EVT_MOTION, self.moveFrame )
        self.titleText.Bind( wx.EVT_LEFT_DOWN, self.OnFrame1LeftDown )
        
        self.resize_button.Bind( wx.EVT_BUTTON, self.onResize )
        self.close_button.Bind( wx.EVT_BUTTON, self.onClose )
        
#        self.Bind( wx.EVT_MOTION, self.test )
        self.test_button.Bind( wx.EVT_BUTTON, self.test)
        
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.Bind(wx.EVT_LEFT_UP, self.onUnclick)
    
        self.lastMousePos = wx.Point(0, 0)
    
    def __del__( self ):
        pass
    
    def test(self, event):
        while True:
            print(wx.GetMousePosition())
            time.sleep(.001)

    def getStats(self, event):
        print(self.graph.GetSize())
        self.graph.Refresh()
        for d in self.data:
            print d
        
    # Virtual event handlers, overide them in your derived class
    def onStart( self, event ):
#        print(self.connections.GetStringSelection())
#        print(self.running)
        if (self.ser == NULL):
            self.status.SetStatusText("There are no connected devices")
            return
        if (self.running == False):
            print("Starting Monitoring")
            self.status.SetStatusText("")
            self.running = True
            self.thread = threading.Thread(target=self.LongRunning)
            self.thread.start()
        
    def onStop(self, event):
        print("Stopping Monitoring")
        self.running = False
        
    def onClear(self, event):
        self.data = list()
        self.graph.setData(self.data)
        self.graph.Refresh()
        self.textInput.Clear()
        
    def UpdateMax( self, event ):
        print(self.max_slider.GetValue())
        self.graph.setMax(self.max_slider.GetValue())
        
    def UpdateMin( self, event ):
        event.Skip()
        
    def LongRunning(self):
        
        while self.running:
            text = self.collectSerial()
#            wx.CallAfter(self.textInput.AppendText, (text + "\n"))
            wx.CallAfter(self.writeSerial, (text))
            time.sleep(.001)
            self.graph.updateGraph()
        while self.running == False:
            text = self.collectSerial()
            time.sleep(.001)
#        else:
#            text = self.collectSerial()
#            time.sleep(.001)
        
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
#        print(self.ser)
        print("connected to: " + self.ser.portstr)
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.read(5)

    def collectSerial(self):
        input = self.ser.readline().rstrip()
        return input

    def writeSerial(self, text):
        if (text.isdigit()):
            self.data.append(text)
            self.graph.setData(self.data)
            self.textInput.AppendText(str(text) + "\n")
        
        
    def hideCarat(self, event):
        self.textInput.ShowNativeCaret(False)
        event.Skip()
        
    def saveFile(self, event):
        saveFileDialog = wx.FileDialog(
            self, message="Choose a file",
            defaultFile="",
            wildcard="",
            style=wx.SAVE | wx.FD_OVERWRITE_PROMPT
            )
        if saveFileDialog.ShowModal() == wx.ID_OK:
            self.textInput.SaveFile(saveFileDialog.GetPath())
        event.Skip()
    
    def onOpenFile(self, event):
        """
        Create and show the Open FileDialog
        """
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultFile="",
            wildcard="",
            style=wx.SAVE | wx.FD_OVERWRITE_PROMPT
            )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            print "You chose the following file(s):"
            for path in paths:
                print path
        dlg.Destroy()
    
    def onResize(self, event):
#        self.Maximize(True)
        self.ShowFullScreen(not self.IsFullScreen())
    
    def onClose(self, event):
        self.running = False
        self.graph.Destroy()
        self.Destroy()
        
    def moveFrame( self, event ):
        if event.LeftIsDown():
            windowX = self.lastMousePos[0]
            windowY = self.lastMousePos[1]
            screenX = wx.GetMousePosition()[0]
            screenY = wx.GetMousePosition()[1]
            deltaX  = screenX - windowX
            deltaY  = screenY - windowY
#            print(str(deltaX) + ", " + str(deltaY))
#            self.Move(wx.Point(screenX - windowX, screenY - windowY))
            self.Move(wx.Point(self.GetPosition()[0] + deltaX, self.GetPosition()[1] + deltaY))
            self.lastMousePos = wx.GetMousePosition()
            print("it's moving")
        else:
            print("False")
        event.Skip()
 
    def OnFrame1LeftDown(self, event):
#        self.lastMousePos = event.GetPosition()
        self.lastMousePos = wx.GetMousePosition()
        if event.LeftIsDown():
            self.drag = True
            print("true")
        else:
            self.drag = False
            print("false")
#        print(self.lastMousePos)
#        print(wx.GetMousePosition())
#        self.lastMousePos = wx.GetMousePosition()
        event.Skip()
 
    def onUnclick(self, event):
        print("All clear")


app = wx.App(False)

frame = Main(None)
frame.Show()
app.MainLoop()