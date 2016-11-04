import wx
import wx.lib.dialogs
import wx.stc as stc
import os

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
		self.dirname = ''							# Name of the current directory we are working on.
		self.filename = ''							# Name of the fiel we are working on.
		self.lineNoEnabled = True					# Toggle on/off the line number column.
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
		lineNumbers = prefMenu.Append( wx.ID_ANY, "&Line Numbers", "Toggles Line Numbers On/Off" )

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

		# Assign the menu bar to the window.
		self.SetMenuBar( menuBar )

		# Let's bind the menus with events and actions.
		self.Bind( wx.EVT_MENU, self.OnNew, menuNew )
		self.Bind( wx.EVT_MENU, self.OnOpen, menuOpen )
		self.Bind( wx.EVT_MENU, self.OnSave, menuSave )
		self.Bind( wx.EVT_MENU, self.OnSaveAs, menuSaveAs )
		self.Bind( wx.EVT_MENU, self.OnClose, menuClose ) 

		self.Bind( wx.EVT_MENU, self.OnRedo, menuRedo )
		self.Bind( wx.EVT_MENU, self.OnUndo, menuUndo )
		self.Bind( wx.EVT_MENU, self.OnCopy, menuCopy )
		self.Bind( wx.EVT_MENU, self.OnCut, menuCut )
		self.Bind( wx.EVT_MENU, self.OnSelectAll, menuSelectAll )
		self.Bind( wx.EVT_MENU, self.OnPaste, menuPaste )

		self.Bind( wx.EVT_MENU, self.OnToggleLineNumbers, lineNumbers )

		self.Bind( wx.EVT_MENU, self.OnAbout, menuAbout )

		# Make the window visible.
		self.Show()

	def OnNew( self, event ):
		self.filename = "Untitled"
		self.control.SetValue("")

	def OnOpen( self, event ):
		try:
			# We will try an open the file selected from the dialog box if that's an acceptable file.
			# Note: Basically any file will be readable.
			diag = wx.FileDialog( self, "Choose a File...", self.dirname, "", "*.*", wx.FD_OPEN )
			if( wx.ID_OK == diag.ShowModal() ):
				self.filename = diag.GetFilename()
				self.dirname = diag.GetDirectory()
				currentFile = open( os.path.join( self.dirname, self.filename ), 'r' )
				self.control.SetValue( currentFile.read() )
				currentFile.close()
			diag.Destroy()
		except Exception as e:
			diag = wx.MessageDialog( self, "Unable to open the selected file. Please check the file before continuing.", wx.ICON_ERROR )
			diag.ShowModal()
			diag.Destroy()

	# For save, we will try to save the current file as it is.
	# If that's not possible, like if the file is not yet in the disk to save, then we will call save as to save the file to the disk first.
	def OnSave( self, event ):
		try:
			currentFile = open( os.path.join( self.dirname, self.filename ), 'w' )
			currentFile.write( self.control.GetValue )
			currentFile.Close()
		except:
			try:
				diag = wx.FileDialog( self, "Save File As", self.dirname, "Untitled", "*.*", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT )
				if( wx.ID_OK == diag.ShowModal() ):
					self.filename = diag.GetFilename()
					self.dirname = diag.GetDirectory()
					currentFile = open( os.path.join( self.dirname, self.filename ), 'w' )
					currentFile.write(self.control.GetValue() )
					currentFile.close()
				diag.Destory()
			except:
				pass

	def OnSaveAs( self, event ):
		try:
			diag = wx.FileDialog( self, "Save File As...", self.dirname, "Untitled", "*.*", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT )
			if( wx.ID_OK == diag.ShowModal() ):
				self.filename = diag.GetFilename()
				self.dirname = diag.GetDirectory()
				currentFile = open( os.path.join( self.dirname, self.filename ), 'w' )
				currentFile.write( self.control.GetValue() )
				currentFile.close()
			diag.Destory()
		except:
			pass

	def OnClose( self, event ):
		self.Close( True )

	def OnUndo( self, event ):
		self.control.Undo()

	def OnRedo( self, event ):
		self.control.Redo()

	def OnSelectAll( self, event ):
		self.control.SelectAll()

	def OnCopy( self, event ):
		self.control.Copy()

	def OnCut( self, event ):
		self.control.Cut()

	def OnPaste( self, event ):
		self.control.Paste()

	def OnToggleLineNumbers( self, event ):
		if( self.lineNoEnabled ):
			self.control.SetMarginWidth( 1, 0 )
			self.lineNoEnabled = False
		else:
			self.control.SetMarginWidth( 1, self.leftMarginWidth )
			self.lineNoEnabled = True

	def OnAbout( self, event ):
		diag = wx.MessageDialog( self, "Advanced Text Editor. Created by Varun Tyagi using Pyhon and wx. Ver: 1.0", "About Advanced Text Editor", wx.OK )
		diag.ShowModal()
		diag.Destroy()


app = wx.App()
frame = MainWindow( None, "Advanced Text Editor" )
app.MainLoop()
