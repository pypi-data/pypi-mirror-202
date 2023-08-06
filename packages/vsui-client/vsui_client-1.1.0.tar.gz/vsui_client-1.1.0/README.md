# Volume Segmantics User Interface Client

This package allows a python script to connect to the volume segmantics server and update the server's information about a corresponding process. <br>
The task id must match the name of a process definition in the connected server. The provided methods are:
- **set_task_id** (id : str)
    - This should correspond to the name of this process on the server.
- **connect** (HOST : str = 'localhost', PORT : str = '8000')
    - Initiates a socketio session with the server.
- **edit_element** (element_uid : str, value : Any)
    - Target a specific display component and update its data.
- **notify** (txt : str, type : str)
    - send a toast to the client
    - types:
        - success
        - error
        - info
        - warning
    - changing the type only changes the toast colour and icon
- **set_logging_target** (key: str)
    - Define the component key of the task element that logs should be forwarded to.

<br>
A log component can be configured to display all messages sent to a logger using 

    # (if you want to get the default logger)
    logger = logging.getLogger()
    # add the vsui handler to your logger
    handler = vsui_client.RequestHandler()


Now all logging messages will be forwarded to the specified component in the web client.