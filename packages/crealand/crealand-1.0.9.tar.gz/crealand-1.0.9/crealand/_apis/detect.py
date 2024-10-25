from crealand._core.bridge.interface import call_api, call_api_async
from crealand._apis.constants import DestType
from crealand._apis import event
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

        event.onSensorSoundEvent('==','',cb_wrapper)

    # 结束识别
    def stop_decibel_recognition():
        call_api_async('web-ide', 'api.openDecibelDetectionPage', [{'type':'end'}])

    @staticmethod
    def onEventDecibel(decibel_value,cb):
        def cb_wrapper(err,data):
            Detect._decibel_val = data['data']
            cb(data['data'])

        event.onSensorSoundEvent('>',decibel_value,cb_wrapper)


    # 获取虚拟相机
    @staticmethod
    def virtual_camera(runtime_id: int,status: bool, ):
        call_api('unity', 'unity.camera.openVirsual', [runtime_id,status])
