__version__ = '1.0.18'

from ._apis import (
    ai as AI, 
    detect as Detect, 
    event as Event, 
    interactive as Interactive, 
    object as Object
)

from ._apis.interactive import (
    Dialogue, 
    HelpPanel, 
    TaskPanel, 
    Speak, 
    Interactive
)

from ._apis.media import (
    Sound, 
    Video, 
    Image
)

from ._apis.sensor import (
    Ultrasonic, 
    Auditory, 
    Visual, 
    Temperature, 
    Humidity, 
    Gravity
)

from ._utils.logger_setup import (
    enable_logger, 
    disable_logger, 
    setup_logger
)

def __initialize():
    try:
        import os
        import threading
        from ._core.websocket.websocket_client import ws_connect, get_ws_client, init_callback

        logger = setup_logger()
        server_url = os.getenv('ENV_CREALAND_UCODELINK_SERVER_URL')
        session_id = os.getenv('ENV_CREALAND_SESSIONID')
        logger.info(f'server_url: {server_url}, session_id: {session_id}')
        logger.info('The version is 1.0.17')
        #taskId = os.getenv('ENV_CREALAND_TASKID')
        threading.Thread(target=ws_connect, args=(server_url, session_id, )).start()
        while True:
            ws_client = get_ws_client()
            if ws_client and ws_client.session_id:
                break
        init_callback()
    except Exception as e:
        logger.error(f'An error occurred: {e}')

__initialize()

