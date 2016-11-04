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
		self.leftMarginSpace = 5

		# Init the frame with default size to 800x600.
		wx.Frame.__init__( self, parent, title = title, size = ( 800, 600 ) )
		self.control = stc.StyledTextCtrl( self, style = wx.TE_MULTILINE | wx.TE_WORDWRAP )

		# Key bindings for zoom in and zoom out.
		self.control.CmdKeyAssign( ord('+'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMIN ) 	# Ctrl + '+' = Zoom in.
		self.control.CmdKeyAssign( ord('-'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMIN ) 	# Ctrl + '-' = Zoom out

		# Disable showing white space.
		self.control.SetViewWhiteSpace( False )

		# Margins
		self.control.SetMargins( self.leftMarginSpace, 0 )								# Distance of the text from the margin. 5 is so it'll be very small.
		self.control.SetMarginType( 1, stc.STC_MARGIN_NUMBER )							# Each column number.		
		self.control.SetMarginWidth( 1, self.leftMarginWidth )							# Column number panel width.

		# Status bar (appears below on the left hand side)
		self.CreateStatusBar()
		self.StatusBar.SetBackgroundColour( ( 134, 187, 186 ) )

		# Menu Bars

		# File Menu.
		fileMenu = wx.Menu()
		menuNew = fileMenu.Append( wx.ID_NEW, "&New", "Create a New Document" )
		menuOpen = fileMenu.Append( wx.ID_OPEN, "&Open", "Open an Existing Document" )
		menuOpenFolder = fileMenu.Append( wx.ID_OPEN, "Open Folder...", "Open a Directory")
		menuOpenRecent = fileMenu.Append( wx.ID_OPEN, "Open &Recent", "Open Recent Document" )
		menuSave = fileMenu.Append( wx.ID_SAVE, "&Save", "Save the Current Document" )
		menuSaveAs = fileMenu.Append( wx.ID_SAVEAS, "Save &As", "Save a New Document" )
		fileMenu.AppendSeparator()
		menuClose = fileMenu.Append( wx.ID_EXIT, "&Close", "Close the Application" )

		# Edit Menu
		editMenu = wx.Menu()
		menuCopy = editMenu.Append( wx.ID_COPY, "&Copy", "Copy" )
		menuPaste = editMenu.Append( wx.ID_PASTE, "&Paste", "Paste" )
		menuCut = editMenu.Append( wx.ID_CUT, "Cu&t", "Cut" )
		menuSelectAll = editMenu.Append( wx.ID_SELECTALL, "Select &All", "Select All" )
		editMenu.AppendSeparator()
		menuUndo = editMenu.Append( wx.ID_UNDO, "&Undo", "Undo last Action" )
		menuRedo = editMenu.Append( wx.ID_REDO, "&Redo", "Redo last Action" )

		# Find Menu
		findMenu = wx.Menu()
		find = findMenu.Append( wx.ID_FIND, "Find...", "Search in the Document" )
		replace = findMenu.Append( wx.ID_REPLACE, "Replace...", "Replace in the Document" )

		# Preferences Menu.
		prefMenu = wx.Menu()
		settings = prefMenu.Append( wx.ID_ANY, "Settings", "Change Editor Settings" )

		# Help Menu.
		helpMenu = wx.Menu()
		menuHowTo = helpMenu.Append( wx.ID_ANY, "How To...", "Help Topics" )
		menuDocumentation = helpMenu.Append( wx.ID_ANY, "Documentation", "Editor Documentation" )
		helpMenu.AppendSeparator()
		menuAbout = helpMenu.Append( wx.ID_ABOUT, "About", "Know More.." )

		# Add all the menus to the menu bar.
		menuBar = wx.MenuBar()
		menuBar.Append( fileMenu, "&File" )
		menuBar.Append( editMenu, "&Edit" )
		menuBar.Append( findMenu, "F&ind" )
		menuBar.Append( prefMenu, "Prefere&nces" )
		menuBar.Append( helpMenu, "&Help" )
		self.SetMenuBar( menuBar )
		self.Show()

app = wx.App()
frame = MainWindow( None, "Advanced Text Editor" )
app.MainLoop()
