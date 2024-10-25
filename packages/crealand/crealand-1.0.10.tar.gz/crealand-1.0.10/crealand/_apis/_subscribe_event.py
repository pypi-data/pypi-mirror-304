import uuid
import threading
from crealand._core.bridge.interface import _call_api_async
from crealand._core.websocket.websocket_client import get_event_loop, get_callback
from crealand._utils.logger_setup import _setup_logger
from crealand._apis.constants import KeyboardType, KeyActiveType, KeyboardActiveType, MouseKeyType

logger = _setup_logger()

def _subscribeEvent(dest, func_name, func_args, callback=None):
    def eventCallback(err, data):
        try:
            logger.info(f'Trigger the event callback. err: {err}, data: {data}')
            if 'type' in data:
                logger.info('This is an event trigger.')
                if data['type'] == 'trigger':
                    logger.info('The type is trigger.')
                    callback(err, data)
            else:
                logger.info('This is an api trigger.')
                callback(err, data)
            logger.info('Finished!')
        except Exception as e:
            logger.error(f'An error occurred: {e}')

    return _call_api_async(dest, func_name, func_args, eventCallback if callback else None)

def onBroadcastEvent(info, callback):
    event_callback = get_callback()
    event_callback.registerBroadcast(info, callback)

def sendBroadcast(info):
    event_callback = get_callback()
    threading.Thread(
        target=event_callback.broadcast, 
        args=(info, )
    ).start()

# Crealand IDE-WEB
def onInputsMouseEvent(click, button, callback):
    func_args = [
        'InputsMouseEvent', {
            'subscribeId': str(uuid.uuid4()), 
            'targets': [{
                'name': 'click', 
                'type': 'and', 
                'conditions': {
                    '==': click
                }}, {
                'name': 'button', 
                'type': 'and', 
                'conditions': {
                    '==': button
                }}
            ]
        }
    ]
    return _subscribeEvent(
        dest='web-ide', 
        func_name='event.subscribeRemoteEvent', 
        func_args=func_args, 
        callback=callback
    )
    
def onInputsKeyboardEvent(click, button, callback):
    logger.info(f'callback name: {callback.__name__}')
    func_args = [
        'InputsKeyboardEvent', {
            'subscribeId': str(uuid.uuid4()), 
            'targets': [{
                'name': 'click', 
                'type': 'and', 
                'conditions': {
                    '==': click
                }}, {
                'name': 'button', 
                'type': 'and', 
                'conditions': {
                    '==': button
                }}
            ]
        }
    ]
    return _subscribeEvent(
        dest='web-ide', 
        func_name='event.subscribeRemoteEvent', 
        func_args=func_args, 
        callback=callback
    )

def onAIFigureEvent(number, callback):
    func_args = [
        'AIFigureEvent', {
            'subscribeId': str(uuid.uuid4()), 
            'targets': [{
                'name': 'number', 
                'type': 'and', 
                'conditions': {
                    '==': number
                }}
            ]
        }
    ]
    return _subscribeEvent(
        dest='web-ide', 
        func_name='event.subscribeRemoteEvent', 
        func_args=func_args, 
        callback=callback
    )

def onAIGestureEvent(direction, callback):
    func_args = [
        'AIGestureEvent', {
            'subscribeId': str(uuid.uuid4()), 
            'targets': [{
                'name': 'direction', 
                'type': 'and', 
                'conditions': {
                    '==': direction
                }}
            ]
        }
    ]
    return _subscribeEvent(
        dest='web-ide', 
        func_name='event.subscribeRemoteEvent', 
        func_args=func_args, 
        callback=callback
    )

def onAIAsrEvent(text, callback):
    func_args = [
        'AIAsrEvent', {
            'subscribeId': str(uuid.uuid4()), 
            'targets': [{
                'name': 'text', 
                'type': 'and', 
                'conditions': {
                    '==': text
                }}
            ]
        }
    ]
    return _subscribeEvent(
        dest='web-ide', 
        func_name='event.subscribeRemoteEvent', 
        func_args=func_args, 
        callback=callback
    )

def onSensorSoundEvent(compare, decibel_value, callback):
    func_args = [
        'SensorSoundEvent', {
            'subscribeId': str(uuid.uuid4()), 
            'targets': [{
                'name': 'decibel_value', 
                'type': 'and', 
                'conditions': {
                    compare: decibel_value
                }}
            ]
        }
    ]
    return _subscribeEvent(
        dest='web-ide', 
        func_name='event.subscribeRemoteEvent', 
        func_args=func_args, 
        callback=callback
    )

# Crealand IDE-3D
def onAreaObjectEvent(runtime_id, action, area_id, callback):
    func_args = [
        runtime_id, 
        action, 
        area_id, {
            'subscribeId': str(uuid.uuid4()), 
            'targets': []
        }
    ]
    return _subscribeEvent(
        dest='unity', 
        func_name='unity.editableTrigger.onEventRuntimeIdTrigger', 
        func_args=func_args, 
        callback=callback
    )

def onAreaClassEvent(config_id, action, area_id, callback):
    func_args = [
        config_id, 
        action, 
        area_id, {
            'subscribeId': str(uuid.uuid4()), 
            'targets': []
        }
    ]
    return _subscribeEvent(
        dest='unity', 
        func_name='unity.editableTrigger.onEventConfigIdTrigger', 
        func_args=func_args, 
        callback=callback
    )

def onSensorUltrasonicEvent(runtime_id, attachment_id, compare, distance, callback):
    func_args = [
        runtime_id, 
        attachment_id, {
            'subscribeId': str(uuid.uuid4()), 
            'targets': [{
                'name': 'distance', 
                'type': 'and', 
                'conditions': {
                    compare: distance
                }}
            ]
        }
    ]
    return _subscribeEvent(
        dest='unity', 
        func_name='unity.sensor.onEventUltrasonicRanging', 
        func_args=func_args, 
        callback=callback
    )

def onSensorTemperatureEvent(temperature_sensor, compare, temperature, callback):
    func_args = [
        temperature_sensor, {
            'subscribeId': str(uuid.uuid4()), 
            'targets': [{
                'name': 'temperature', 
                'type': 'and', 
                'conditions': {
                    compare: temperature
                }}
            ]
        }
    ]
    return _subscribeEvent(
        dest='unity', 
        func_name='unity.sensor.onEventTemperature', 
        func_args=func_args, 
        callback=callback
    )

def onSensorHumidityEvent(humidity_sensor, compare, humidity_value, callback):
    func_args = [
        humidity_sensor, {
            'subscribeId': str(uuid.uuid4()), 
            'targets': [{
                'name': 'humidity_value', 
                'type': 'and', 
                'conditions': {
                    compare: humidity_value
                }}
            ]
        }
    ]
    return _subscribeEvent( 
        dest='unity', 
        func_name='unity.sensor.onEventHumidity', 
        func_args=func_args, 
        callback=callback
    )

def onSensorGravityEvent(gravity_sensor, compare, gravity_value, callback):
    func_args = [
        gravity_sensor, {
            'subscribeId': str(uuid.uuid4()), 
            'targets': [{
                'name': 'gravity_value', 
                'type': 'and', 
                'conditions': {
                    compare: gravity_value
                }}
            ]
        }
    ]
    return _subscribeEvent(
        dest='unity', 
        func_name='unity.sensor.onEventGravity', 
        func_args=func_args, 
        callback=callback
    )

def startTemperatureDetection(judge_area_id, callback=None):
    func_args = [
        judge_area_id, {
            'subscribeId': str(uuid.uuid4()), 
            'targets': []
        }
    ]
    return _subscribeEvent(
        dest='unity', 
        func_name='unity.sensor.startTemperatureDetection', 
        func_args=func_args, 
        callback=callback
    )

def startHumidityDetection(judge_area_id, callback=None):
    func_args = [
        judge_area_id, {
            'subscribeId': str(uuid.uuid4()), 
            'targets': []
        }
    ]
    return _subscribeEvent(
        dest='unity', 
        func_name='unity.sensor.startHumidityDetection', 
        func_args=func_args, 
        callback=callback
    )

