from pymodaq_plugins_pylablib_camera.daq_viewer_plugins.plugins_2D.daq_2Dviewer_GenericPylablibCamera import DAQ_2DViewer_GenericPylablibCamera
from pymodaq.control_modules.viewer_utility_classes import main

from pylablib.devices import Andor


class DAQ_2DViewer_AndorPLL(DAQ_2DViewer_GenericPylablibCamera):
    # For Andor, this returns the number of connected cameras
    camera_list = [*range(Andor.get_cameras_number_SDK3())]

    # Update the params (nothing to change here)
    params = DAQ_2DViewer_GenericPylablibCamera.params
    params[next((i for i, item in enumerate(params) if item["name"] == "camera_list"), None)]['limits'] = camera_list


    def init_controller(self):
        # Define the camera controller.
        # Init camera with currently selected serial number in the camera list
        return Andor.AndorSDK3Camera(idx=self.settings["camera_list"])


if __name__ == '__main__':
    main(__file__)
