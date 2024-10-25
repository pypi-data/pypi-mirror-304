from crealand._core.bridge.interface import _call_api, _call_api_async
from crealand._apis.constants import DestType
from crealand._apis import _subscribe_event
class Detect:
    _decibel_val=0
    # 分贝值
    @staticmethod
    def get_decibel_value():
        return Detect._decibel_val

    # 开始识别
    @staticmethod
    def start_decibel_recognition():

        def cb_wrapper(err,data):
            Detect._decibel_val = data['data']

        _subscribe_event.onSensorSoundEvent('==','',cb_wrapper)

    # 结束识别
    def stop_decibel_recognition():
        _call_api_async('web-ide', 'api.openDecibelDetectionPage', [{'type':'end'}])

    @staticmethod
    def onEventDecibel(decibel_value,cb):
        def cb_wrapper(err,data):
            Detect._decibel_val = data['data']
            cb(data['data'])

        _subscribe_event.onSensorSoundEvent('>',decibel_value,cb_wrapper)


    # 获取虚拟相机
    @staticmethod
    def virtual_camera(runtime_id: int,status: bool, ):
        _call_api('unity', 'unity.camera.openVirsual', [runtime_id,status])
