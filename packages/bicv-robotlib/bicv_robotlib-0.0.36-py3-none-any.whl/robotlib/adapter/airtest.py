import airtest.core.assertions
from airtest.core.helper import logwrap

'''
继电器
'''


class Relay:

    @classmethod
    @logwrap
    def relay_connect(cls, replay_name, state="ON"):
        from robotlib.devices.relay.single.relay_single_factory import Relay_Single_Factory
        Relay_Single_Factory.get_relay_single_device(replay_name).connect()

    @classmethod
    @logwrap
    def relay_disconnect(cls, replay_name, state="OFF"):
        from robotlib.devices.relay.single.relay_single_factory import Relay_Single_Factory
        Relay_Single_Factory.get_relay_single_device(replay_name).disconnect()


'''
三边继电器
'''


class Three_Side:
    @classmethod
    @logwrap
    def three_side_connect_embedded_and_usb(cls):
        from robotlib.devices.relay.three_side.relay_three_side_factory import Relay_Three_Side_Factory
        Relay_Three_Side_Factory.get_relay_three_side_device().connect_embedded_and_usb()

    @classmethod
    @logwrap
    def three_side_connet_pc_and_embedded(cls):
        from robotlib.devices.relay.three_side.relay_three_side_factory import Relay_Three_Side_Factory
        Relay_Three_Side_Factory.get_relay_three_side_device().connet_pc_and_embedded()

    @classmethod
    @logwrap
    def three_side_connet_pc_and_usb(cls):
        from robotlib.devices.relay.three_side.relay_three_side_factory import Relay_Three_Side_Factory
        Relay_Three_Side_Factory.get_relay_three_side_device().connet_pc_and_usb()


'''
电源
'''


class Power:
    @classmethod
    @logwrap
    def power_open(cls):
        from robotlib.devices.power.power_factory import PowerFactory
        PowerFactory.get_power_device().open_power()

    @classmethod
    @logwrap
    def power_close(cls):
        from robotlib.devices.power.power_factory import PowerFactory
        PowerFactory.get_power_device().close_power()

    @classmethod
    @logwrap
    def power_set_voltage(cls, voltage):
        from robotlib.devices.power.power_factory import PowerFactory
        PowerFactory.get_power_device().set_voltage(voltage)

    @classmethod
    @logwrap
    def power_get_voltage(cls):
        from robotlib.devices.power.power_factory import PowerFactory
        PowerFactory.get_power_device().get_voltage()

    @classmethod
    @logwrap
    def power_get_electric_current(cls):
        from robotlib.devices.power.power_factory import PowerFactory
        PowerFactory.get_power_device().get_electric_current()


'''
万用表
'''


class Multimeter:

    @classmethod
    @logwrap
    def multimeter_get_voltage(cls):
        from robotlib.devices.multimeter.multimeter_factory import Multimeter_Factory
        device = Multimeter_Factory.get_multimeter_device('MULTIMETER_WINNERS')
        if device:
            bresult, fvotage = device.get_cur_voltage()
            return fvotage if bresult else 0
        else:
            return 0

    @classmethod
    @logwrap
    def multimeter_get_current(cls):
        from robotlib.devices.multimeter.multimeter_factory import Multimeter_Factory
        device = Multimeter_Factory.get_multimeter_device('MULTIMETER_WINNERS')
        if device:
            bresult, fcurrent = device.get_cur_current()
            return fcurrent if bresult else 0
        else:
            return 0


'''
点击器
'''


class Clicker:

    @classmethod
    @logwrap
    def clicker_click_point(cls, point):
        from robotlib.devices.clicker.clicker_factory import Clicker_Factory
        Clicker_Factory.get_device_instance().sim_click_io(point)


class Notification:

    @classmethod
    @logwrap
    def send_message(cls, clent, message, reminders):
        from robotlib.notification.notification_factory import NotificationFactory
        NotificationFactory.get_client(clent).send_message_with_text(message, reminders)


class Tts:

    @classmethod
    @logwrap
    def speak_with_voice_package(cls, text, voice_id):
        from robotlib.tts.tts_factory import TtsFactory
        tts = TtsFactory.get_scheme('WINDOWS')
        tts.speak_with_voice_package(text, voice_id)

    @classmethod
    @logwrap
    def make_file(cls, text, voice_id):
        from robotlib.tts.tts_factory import TtsFactory
        tts = TtsFactory.get_scheme('WINDOWS')
        tts.make_file(text, voice_id)


class CAN:
    @classmethod
    @logwrap
    def send_signal_message(cls, message: str):
        # from robotlib.can.can_dev_factory import *
        # can_dev: CAN_Device = CAN_Device_Factory.get_device_instance()
        # can_dev.send_frame(message)
        pass

    @classmethod
    @logwrap
    def assert_test_signal_status(cls, message: str):
        # from robotlib.can.can_dev_factory import *
        # can_dev: CAN_Device = CAN_Device_Factory.get_device_instance()
        # res = can_dev.read_test_signal_status(message)
        # airtest.core.assertions.assert_true(res)
        pass


class Assert_Bicv:

    @classmethod
    @logwrap
    def camera_assert_exists(cls, image):
        from airtest.core.cv import Template
        from robotlib.assertion.assert_factory import Assert_Factory
        camera_scheme = Assert_Factory.get_assert_instance('CAMERA')
        result = camera_scheme.assert_exists(Template(image))
        print(f'result -> {result}')

    @classmethod
    @logwrap
    def camera_assert_not_exists(cls, image):
        from airtest.core.cv import Template
        from robotlib.assertion.assert_factory import Assert_Factory
        camera_scheme = Assert_Factory.get_assert_instance('CAMERA')
        result = camera_scheme.assert_not_exists(Template(image))
        print(f'result -> {result}')


class CAN:
    """
    can 模块
    """
    @classmethod
    @logwrap
    def start(cls):
        from robotlib.can.can_dev_factory import CAN_Device_Factory
        CAN_Device_Factory.get_device_instance().start()

    @classmethod
    @logwrap
    def stop(cls):
        from robotlib.can.can_dev_factory import CAN_Device_Factory
        CAN_Device_Factory.get_device_instance().stop()

    @classmethod
    @logwrap
    def change_signal_from_vehicle_2_mmi(cls, message: str):
        from robotlib.can.can_dev_factory import CAN_Device_Factory
        CAN_Device_Factory.get_device_instance().change_signal_from_vehicle_2_mmi(message)

    @classmethod
    @logwrap
    def change_signal_from_vehicle_2_mmi_by_id(cls, id, sig_list):
        from robotlib.can.can_dev_factory import CAN_Device_Factory
        CAN_Device_Factory.get_device_instance().change_signal_from_vehicle_2_mmi_by_id(id, sig_list)

    @classmethod
    @logwrap
    def send_frame_data_from_vehicle_2_mmi(cls, id: str, data: str):
        from robotlib.can.can_dev_factory import CAN_Device_Factory
        CAN_Device_Factory.get_device_instance().send_frame_data_from_vehicle_2_mmi(id, data)

    @classmethod
    @logwrap
    def check_test_signal_status(cls, message: str):
        from robotlib.can.can_dev_factory import CAN_Device_Factory
        CAN_Device_Factory.get_device_instance().check_test_signal_status(message)

    @classmethod
    @logwrap
    def check_can_bus_exist_signal(cls, id: str, sig: str, value: str):
        from robotlib.can.can_dev_factory import CAN_Device_Factory
        CAN_Device_Factory.get_device_instance().check_can_bus_exist_signal(id, sig, value)

    @classmethod
    @logwrap
    def check_can_bus_exist_id(cls, id: str):
        from robotlib.can.can_dev_factory import CAN_Device_Factory
        CAN_Device_Factory.get_device_instance().check_can_bus_exist_id(id)

class Camera:
    @classmethod
    @logwrap
    def image_assert_exists(cls, image):
        from airtest.core.cv import Template
        from robotlib.assertion.assert_factory import Assert_Factory
        camera_scheme = Assert_Factory.get_assert_instance('IMAGE')
        result = camera_scheme.assert_exists(Template(image))
        print(f'result -> {result}')



    @classmethod
    @logwrap
    def image_assert_not_exists(cls, image):
        from airtest.core.cv import Template
        from robotlib.assertion.assert_factory import Assert_Factory
        camera_scheme = Assert_Factory.get_assert_instance('CAMERA')
        result = camera_scheme.assert_not_exists(Template(image))
        print(f'result -> {result}')

