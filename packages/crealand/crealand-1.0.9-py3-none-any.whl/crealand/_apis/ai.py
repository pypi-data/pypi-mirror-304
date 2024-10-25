from crealand._apis.constants import DestType,HangPointType,Direction
from crealand._core.bridge.interface import call_api, call_api_async
from crealand._apis.subscribe_event import onAIFigureEvent,onAIGestureEvent,onAIAsrEvent
from crealand._utils.logger_setup import setup_logger

logger = setup_logger()
# 人脸识别
# 机器学习
# 数字识别


class Figure:

    _digit=''
    # 打开手写数字识别教学页面
    @staticmethod
    def open_teach_page():
        call_api('web-ide','api.openDigitRecognitionTeachingPage',[{'name':''}])

    # 打开神经网络教学页面
    @staticmethod
    def open_NN_teach_page():
        call_api('web-ide','api.openNeuralNetworkTeachingPage',[{'type':''}])

    # 开始手写数字识别
    @staticmethod
    def start_digital_recognition():
        # 识别返回的结果需要设置保存
        # call_api_async('web-ide','api.digitRecognition',[{'type':'start'}])
        def on_result(err,data):
            Figure._digit = int(data['data'])

        onAIFigureEvent('',on_result)

    # 结束手写数字识别
    @staticmethod
    def stop_digital_recognition():
        try:
            Figure._digit =''
            call_api_async('web-ide','api.digitRecognition',[{'type':'end'}])
        except Exception as e:
            logger.info(f'{e}')

    # 数字识别结果
    @staticmethod
    def get_figure_value():
        return Figure._digit

    # 清除数字识别结果
    @staticmethod
    def clear_figure_value(val: int):
        Figure._digit =''
        call_api('web-ide','api.digitRecognitionClear')

    @staticmethod
    def onAIFigureEvent(number,cb):
        # 识别返回的结果需要设置保存
        # call_api_async('web-ide','api.digitRecognition',[{'type':'start'}])
        def on_result(err,data):
            Figure._digit = int(data['data'])
            cb(int(data['data']))

        onAIFigureEvent(number,on_result)


# 手势识别
class Gesture:
    _direction=''
    # 开始手势识别 并等待结束
    @staticmethod
    def start_gesture_recognition():
        def on_result(err,data):
            Gesture._direction = data['data']

        onAIGestureEvent('',on_result)

    # 结束手势识别
    @staticmethod
    def stop_gesture_recognition():
        Gesture._direction=''
        call_api_async('web-ide','api.gestureRecognition',[{'type':'end'}])

    # 当前手势识别结果为
    @staticmethod
    def get_gesture_value():
        return Gesture._direction

    # 帽子积木块
    @staticmethod
    def AIGestureEvent(direction,cb):
        def on_result(err,data):
            print(data['data'])
            Gesture._direction = data['data']
            cb(data['data'])

        onAIGestureEvent(direction,on_result)

def cb():
    print('cb')
# 语音识别
class Voice:
    _text=''
    # 开始语音识别
    @staticmethod
    def start_voice_recognition():
        def on_result(err,data):
            Voice._text = data['data']

        onAIAsrEvent('',on_result)


    # 结束识别
    @staticmethod
    def stop_voice_recognition():
        Voice._text =''
        call_api('web-ide','api.openVoiceRecognition',[{'type':'end'}])

    # 语音识别结果
    @staticmethod
    def get_voice_value():
        return Voice._text


    # 打开语音识别教学页面
    @staticmethod
    def open_voice_teach_page():
        call_api('web-ide','api.openVoiceRecognitionTeachingPage',[{'name':''}])

    # 帽子积木块
    @staticmethod
    def onAIAsrEvent(text,cb):
        def on_result(err,data):
            print(data['data'])
            Voice._text = data['data']
            cb(data['data'])

        onAIAsrEvent(text,on_result)


