from crealand.apis.constants import DestType,HangPointType
from crealand.core.bridge.interface import call_api, call_api_async
from crealand.apis.event import onSensorUltrasonicEvent,onSensorSoundEvent ,onSensorTemperatureEvent ,onSensorHumidityEvent ,onSensorGravityEvent ,startTemperatureDetection,startHumidityDetection
from typing import Callable,Any
from crealand.utils.utils import Handle_point

# 超声波传感器

class Ultrasonic:
    _sensors = {}

    # 前端处理传感器信息绑定
    @staticmethod
    def add_sensor(sensor: str, runtime_id: int, attachment_id: tuple) ->None:
        if not isinstance(sensor, str) or not isinstance(runtime_id, int) :
            raise ValueError("Invalid arguments: sensor must be a string, runtime_id must be integers.")
        attach=Handle_point(attachment_id)
        Ultrasonic._sensors[sensor] = (runtime_id, attach)

    @staticmethod
    def get_sensor(sensor: str) -> list:
        if sensor in Ultrasonic._sensors:
            return Ultrasonic._sensors[sensor]
        else:
            raise KeyError(f"Sensor '{sensor}' not found")
        pass

    @staticmethod
    def onSensorUltrasonicEvent(sensor: str, compare: str, distance: float,cb:Callable[...,Any]):
        sensor_info = Ultrasonic.get_sensor(sensor) 
        attachment_id = sensor_info[1]
        onSensorUltrasonicEvent(sensor_info[0],attachment_id,compare,distance,cb)

    @staticmethod
    def get_obstacle_distance(sensor: str)->float:
        sensor_info = Ultrasonic.get_sensor(sensor) 
        print('print==',sensor_info)
        length = call_api_async('uinty', 'uinty.sensor.rayRanging', [sensor_info[0], sensor_info[1]])
        return length

class Auditory:

    _decibel_val=0

    # 获取声音强度
    @staticmethod
    def get_decibel_value():
        return Auditory._decibel_val

    @staticmethod
    def onSensorSoundEvent(compare,decibel_value,cb):
        def cb_wrapper(err,data):
            Auditory._decibel_val = data['data']
            cb(data['data'])

        onSensorSoundEvent(compare,decibel_value,cb_wrapper)

    # 开始分贝识别
    @staticmethod
    def start_decibel_recognition():
        def cb_wrapper(err,data):
            Auditory._decibel_val = data['data']

        onSensorSoundEvent('==','',cb_wrapper)

    # 结束分贝识别
    @staticmethod
    def stop_decibel_recognition():
        call_api_async('web-ide', 'api.openDecibelDetectionPage', [{'type':'end'}])


class Visual:
    _sensors = {}

    # 将传感器绑定到对象的挂点
    def add_sensor(self, sensor: str, runtime_id: int, attachment_id: int=HangPointType.BOTTOM):
        self._sensors[sensor] = (runtime_id, attachment_id)
        pass

    # 获取传感器信息
    def get_sensor_impl(self, sensor: str):
        return self._sensors[sensor]

    # 打开或关闭传感器画面
    def open_visual_sensor(self, action_type: bool=True,sensor: str=''):
        sensor_info=self.get_sensor_impl(sensor)
        if action_type:
            func_name = 'sensor.openVirsual'
            call_api(DestType.UNITY,func_name,[sensor_info[0], sensor_info[1]])
        else:
            func_name = 'sensor.closeVirsual'
            call_api(DestType.UNITY,func_name,[sensor])
        pass

class Temperature:

    _sensors = {}

    def add_sensor_impl(self,sensor: str, runtime_id: int) ->None:
        if not isinstance(sensor, str) or not isinstance(runtime_id, int):
            raise ValueError("Invalid arguments: sensor must be a string, runtime_id and attachment_id must be integers.")
        self._sensors[sensor] = runtime_id

    def get_sensor_impl(self,sensor: str) -> int:
        if sensor in self._sensors:
            return self._sensors[sensor]
        else:
            raise KeyError(f"Sensor '{sensor}' not found")
        pass

    def onSensorTemperatureEvent(self,sensor: str, compare: str, temperature: float,cb:Callable[...,Any]):
        runtime_id = self.get_sensor_impl(sensor) 
        onSensorTemperatureEvent(runtime_id,compare,temperature,cb)
    
    # 设置判定区域温度

    def set_temperature(self, area_id: int, temp_val: float):
        temp_val = max(-40, min(temp_val, 120))
        call_api(DestType.UNITY,'unity.sensor.setTemperature',[area_id,temp_val])

    # 持续检测判定区域温度

    def startTemperatureDetection(self, area_id: int):
        startTemperatureDetection(area_id)

    # 获取温度值

    def get_temperature_value(self, temperature_sensor: list[int]):
        call_api(DestType.UNITY,'unity.sensor.getTemperature',[temperature_sensor[0],temperature_sensor[1]])
        return 10



class Humidity:

    _sensors = {}

    def add_sensor(self,sensor: str, runtime_id: int) ->None:
        if not isinstance(sensor, str) or not isinstance(runtime_id, int):
            raise ValueError("Invalid arguments: sensor must be a string, runtime_id and attachment_id must be integers.")
        self._sensors[sensor] = runtime_id
        call_api(DestType.UNITY,'unity.sensor.attachHumidity',[runtime_id])

    def get_sensor(self,sensor: str) -> int:
        if sensor in self._sensors:
            return self._sensors[sensor]
        else:
            raise KeyError(f"Sensor '{sensor}' not found")
        pass

    def onSensorHumidityEvent(self,sensor: str, compare: str, temperature: float,cb:Callable[...,Any]):
        runtime_id = self.get_sensor(sensor) 
        onSensorHumidityEvent(runtime_id,compare,temperature,cb)

    # 设置判定区域湿度
    def set_humidity(self, area_id: int, humidity_val: float):
        call_api(DestType.UNITY,'unity.sensor.setHumidity',[area_id,humidity_val])


    def get_humidity_value(self,senser:str):
        runtime_id=self.get_sensor(senser)
        call_api(DestType.UNITY,'unity.sensor.getHumidity',[runtime_id])

    # 持续检测判定区域湿度

    def startHumidityDetection(self, area_id: int):
        startHumidityDetection(area_id)


class Gravity:

    _sensors = {}

    def add_sensor(self,sensor: str, runtime_id: int) ->None:
        if not isinstance(sensor, str) or not isinstance(runtime_id, int):
            raise ValueError("Invalid arguments: sensor must be a string, runtime_id and attachment_id must be integers.")
        self._sensors[sensor] = runtime_id
        call_api(DestType.UNITY,'unity.sensor.attachGravity',[runtime_id])

    def get_sensor(self,sensor: str) -> int:
        if sensor in self._sensors:
            return self._sensors[sensor]
        else:
            raise KeyError(f"Sensor '{sensor}' not found")
        pass

    def onSensorGravityEvent(self,sensor: str, compare: str, gravity: float,cb:Callable[...,Any]):
        runtime_id = self.get_sensor_impl(sensor) 
        onSensorGravityEvent(runtime_id,compare,gravity,cb)

    # 设置对象重力
    def set_gravity(self, runtime_id: str, gravity_value: float):
        sensor_info = self._sensors[sensor]
        gravity_value= max(0, min(gravity_value, 10000))
        call_api(DestType.UNITY,'unity.sensor.setGravity',[sensor_info[0],gravity_value])

    # 获取重力值

    def get_gravity_value(self, sensor_info: dict):
        value= call_api(DestType.UNITY,'unity.sensor.getGravity',[sensor_info[0]])
        return value

