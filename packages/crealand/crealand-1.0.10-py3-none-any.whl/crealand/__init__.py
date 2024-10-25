__version__ = '1.0.10'

from ._apis import (
    ai as AI, 
    detect as Detect, 
    event, 
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
    _setup_logger as setup_logger
)

def __initialize():
    try:
        import threading
        from ._core.websocket.websocket_client import ws_connect, get_ws_client, init_callback

        logger = setup_logger()
        threading.Thread(target=ws_connect, args=()).start()
        while True:
            ws_client = get_ws_client()
            if ws_client and ws_client.session_id:
                break
        init_callback()
    except Exception as e:
        logger.error(f'An error occurred: {e}')

__initialize()

