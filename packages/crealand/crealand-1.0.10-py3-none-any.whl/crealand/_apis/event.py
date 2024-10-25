from crealand._core.bridge.interface import _call_api
from crealand._apis import _subscribe_event

class event:

    #收到广播事件
    @staticmethod
    def onBroadcastEvent(info,cb):
        _subscribe_event.onBroadcastEvent(info,cb)
    
    #发送广播事件
    @staticmethod
    def send_broadcast(info):
        _subscribe_event.sendBroadcast(info)

    #对象进入/离开判定区域事件
    @staticmethod
    def onAreaObjectEvent(runtime_id,action,area_id,cb):
        def cb_wrapper(err,data):
            cb()
        _subscribe_event.onAreaObjectEvent(runtime_id,action,area_id,cb_wrapper)

    #分类进入/离开判定区域事件
    @staticmethod
    def onAreaClassEvent(config_id,action,area_id,cb):
        def cb_wrapper(err,data):
            cb()
        _subscribe_event.onAreaClassEvent(config_id,action,area_id,cb_wrapper)
    
    # 获取鼠标按键值
    @staticmethod
    def get_mouse_value():
        result = _call_api('web-ide',"api.getMouseValue",[{'code':0}])
        return result
    # 获取键盘code值
    @staticmethod
    def get_keyboard_value():
        result = _call_api('web-ide',"api.getKeyboardValue",[{}])
        return result


    
