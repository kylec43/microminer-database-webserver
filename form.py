from tkinter import ttk
import tkinter as tk
from threading import Thread
from ConnectionHandler import ConnectionHandler
from tkinter import messagebox as mb
import Constants




class Form (tk.Tk):

	def __init__(self):

		tk.Tk.__init__(self) 

		self.protocol("WM_DELETE_WINDOW", self._onClose)

		self._childThread = None
		self._serverIsRunning = False
		self.eventQueue = []
		self.after(1, self._executeEvents)

		self.title('Database Manager')
		self.minsize(400, 200)

		
		#configure grid
		self.gridSizeRows = 3
		for i in range(self.gridSizeRows):
			self.grid_rowconfigure(i, weight = 1)

		self.gridSizeColumns = 3
		for i in range(self.gridSizeColumns):
			self.grid_columnconfigure(i, weight = 1)


		self.displayStartButton()



	def _onClose(self):
		self.stopKwicServer()
		if self._childThread != None:
			self._childThread.join()
		self.destroy()

	def serverIsRunning(self):
		return self._serverIsRunning


	def addEvent(self, event):
		self.eventQueue.append(event)






	def _executeEvents(self):

		if len(self.eventQueue) > 0:

			if self.eventQueue[0].code == Constants.EVT_PRINT_ERROR:
				mb.showerror("Error", "Error: " + self.eventQueue[0].data)
			elif self.eventQueue[0].code == Constants.EVT_CONNECTION_ERROR:
				self.stopKwicServer()

			self.eventQueue.pop(0)
		
		self.after(1, self._executeEvents)



	def displayStartButton(self):
		for widget in self.winfo_children():
			widget.destroy()

		self._button_start_server = ttk.Button(self, text = 'Start server', command = self.runKwicServer)
		self._button_start_server.grid(row = 1, column = 1, sticky='NESW')

	
	def displayStopButton(self):
		for widget in self.winfo_children():
			widget.destroy()

		self._button_stop_server = ttk.Button(self, text = 'Stop server', command = self.stopKwicServer)
		self._button_stop_server.grid(row = 1, column = 1, sticky='NESW')



	def runKwicServer(self):
		kwicThread = Thread(target=ConnectionHandler, args=(self,))
		kwicThread.start()
		self._childThread = kwicThread
		self._serverIsRunning = True
		self.displayStopButton()


	def stopKwicServer(self):
		self._serverIsRunning = False
		if self._childThread != None:
			self._childThread.join()
			self._childThread = None
		self.displayStartButton()


