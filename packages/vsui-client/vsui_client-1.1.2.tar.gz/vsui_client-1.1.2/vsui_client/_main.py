from vsui_client import _oo_interface

client = None

def get_client() -> _oo_interface.VSUIClient:
    ''' return the current vsui client instance
    Returns:
        _oo_interface.VSUIClient: the client instance
    '''
    if client is None:
        raise Exception('vsui client not initialized')
    return client

def init_vsui(enabled: bool, task_id: str = None, logging_target: str = None) -> _oo_interface.VSUIClient:
    ''' initialize the vsui client
    Args:
        enabled (bool): whether vsui is enabled
        task_id (str): the id of the task
        logging_target (str): the key of the logging target
    Returns:
        _oo_interface.VSUIClient: the client instance
    '''
    if enabled:
        client = _oo_interface.VSUIEnabled()
    else:
        client = _oo_interface.VSUIDisabled()
        client.set_task_id(task_id)
        client.set_logging_target(logging_target)
    return client