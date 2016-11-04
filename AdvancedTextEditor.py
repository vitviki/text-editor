import wx
import wx.lib.dialogs
import wx.stc as stc

# Fonts
faces = {
	'times' :'Times New Roman',
	'mono' : 'Courier New',
	'helv' : 'Ariel',
	'other' :  'Comic Sans MS',
	'size' : 10,
	'size2' : 8,
}

# Window of the text editor class.
class MainWindow( wx.Frame ):

	# Class Init
	def __init__( self, parent, title ):
		self.leftMarginWidth = 25

		wx.Frame.__init__( self, parent, title = title, size = ( 800, 600 ) )
		self.control = stc.StyledTextCtrl( self, style = wx.TE_MULTILINE | wx.TE_WORDWRAP )

		self.Show()

app = wx.App()
frame = MainWindow( None, "Advanced Text Editor" )
app.MainLoop()
