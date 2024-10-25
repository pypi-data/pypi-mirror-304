from crealand._core.bridge.interface import call_api, call_api_async
from crealand._apis import subscribe_event

class event:

    @staticmethod
    def onBroadcastEvent(info,cb):
        subscribe_event.onBroadcastEvent(info,cb)
    
    @staticmethod
    def send_broadcast(info):
        subscribe_event.send_broadcast(info)

    @staticmethod
    def onAreaObjectEvent(runtime_id,action,area_id,cb):
        def cb_wrapper(err,data):
            cb()
        subscribe_event.onAreaObjectEvent(runtime_id,action,area_id,cb)
