import zmq
from muntjac.api import Application, Button, GridLayout, Label, Window

from muntjac.ui.button import IClickListener

"""Code below by Kasper Loopstra, taken from the Muntjac calculator example"""
class EarUI(Application, IClickListener):
    """A simple calculator using Muntjac."""

    def __init__(self):
        super(EarUI, self).__init__()

        # All variables are automatically stored in the session.

        # User interface components


    def init(self):
        # Application.init is called once for each application. Here it
        # creates the UI and connects it to the business logic.
	context = zmq.Context()
	socket = context.socket(zmq.REQ)
	socket.connect("tcp://localhost:5555")
	socket.send_json('dir')
	self.socket=socket
	events=socket.recv_json()
	
        # Create the main layout for our application (4 columns, 5 rows)
        layout = GridLayout(4, len(events)//4+1)

        # Create the main window for the application using the main layout.
        # The main window is shown when the application is starts.
        self.setMainWindow(Window('Ear WebUI', layout))

        for event in events:
            # Create a button and use this application for event handlin
            print event
            if "script" in event:
		continue
            button = Button(event)
            button.addListener(self)

            # Add the button to our main layout
            layout.addComponent(button)


    def buttonClick(self, event):
        # Event handler for button clicks. Called for all the buttons in
        # the application.

        # Get the button that was clicked
        button = event.getButton()

        # Get the requested operation from the button caption
        requestedOperation = button.getCaption()

        # Calculate the new value
	self.socket.send_json("event:"+requestedOperation)
	newValue=self.socket.recv_json()
        # Update the result label with the new value
        #self._display.setValue(newValue)


if __name__ == '__main__':
    from muntjac.main import muntjac
    muntjac(EarUI, nogui=True, forever=True, debug=True)
