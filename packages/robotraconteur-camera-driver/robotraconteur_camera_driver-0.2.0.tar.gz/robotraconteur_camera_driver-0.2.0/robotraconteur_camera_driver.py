import cv2
import RobotRaconteur as RR
RRN = RR.RobotRaconteurNode.s
import RobotRaconteurCompanion as RRC
import argparse
import sys
import platform
import threading
import numpy as np
from RobotRaconteurCompanion.Util.InfoFileLoader import InfoFileLoader
from RobotRaconteurCompanion.Util.DateTimeUtil import DateTimeUtil
from RobotRaconteurCompanion.Util.SensorDataUtil import SensorDataUtil
from RobotRaconteurCompanion.Util.AttributesUtil import AttributesUtil
from RobotRaconteurCompanion.Util.IdentifierUtil import IdentifierUtil
import drekar_launch_process
from contextlib import suppress


class CameraImpl(object):

    def __init__(self, device_id, width, height, fps, camera_info, focus=None, exposure=None, gain=None,
                 brightness=None, contrast=None, saturation=None):

        # if platform.system() == "Windows":
        #    self._capture = cv2.VideoCapture(device_id + cv2.CAP_DSHOW)
        # else:
        self._capture = cv2.VideoCapture(device_id)
        assert self._capture.isOpened(), f"Could not open device: {device_id}"

        self._seqno = 0

        self._capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self._capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self._capture.set(cv2.CAP_PROP_FPS, fps)

        if focus is not None:
            self._capture.set(cv2.CAP_PROP_FOCUS, focus)

        if exposure is not None:
            self._capture.set(cv2.CAP_PROP_EXPOSURE, exposure)

        if gain is not None:
            self._capture.set(cv2.CAP_PROP_GAIN, gain)

        if brightness is not None:
            self._capture.set(cv2.CAP_PROP_BRIGHTNESS, brightness)

        if contrast is not None:
            self._capture.set(cv2.CAP_PROP_CONTRAST, contrast)

        if saturation is not None:
            self._capture.set(cv2.CAP_PROP_SATURATION, saturation)

        self._imaging_consts = RRN.GetConstants('com.robotraconteur.imaging')
        self._image_consts = RRN.GetConstants('com.robotraconteur.image')
        self._image_type = RRN.GetStructureType('com.robotraconteur.image.Image')
        self._image_info_type = RRN.GetStructureType('com.robotraconteur.image.ImageInfo')
        self._compressed_image_type = RRN.GetStructureType('com.robotraconteur.image.CompressedImage')
        self._date_time_utc_type = RRN.GetPodDType('com.robotraconteur.datetime.DateTimeUTC')
        self._isoch_info = RRN.GetStructureType('com.robotraconteur.device.isoch.IsochInfo')
        self._camera_state_type = RRN.GetStructureType('com.robotraconteur.imaging.CameraState')
        self._capture_lock = threading.Lock()
        self._streaming = False
        self._fps = self._capture.get(cv2.CAP_PROP_FPS)
        self._camera_info = camera_info
        self._date_time_util = DateTimeUtil(RRN)
        self._sensor_data_util = SensorDataUtil(RRN)
        self._identifier_util = IdentifierUtil(RRN)
        self._seqno = 0

        self._state_timer = None

    def RRServiceObjectInit(self, ctx, service_path):
        self._downsampler = RR.BroadcastDownsampler(ctx)
        self._downsampler.AddPipeBroadcaster(self.frame_stream)
        self._downsampler.AddPipeBroadcaster(self.frame_stream_compressed)
        self._downsampler.AddPipeBroadcaster(self.preview_stream)
        self._downsampler.AddWireBroadcaster(self.device_clock_now)
        self.frame_stream.MaxBacklog = 2
        self.frame_stream_compressed.MaxBacklog = 2
        self.preview_stream.MaxBacklog = 2

        # TODO: Broadcaster peek handler in Python
        self.device_clock_now.PeekInValueCallback = lambda ep: self._date_time_util.FillDeviceTime(
            self._camera_info.device_info, self._seqno)

        self._state_timer = RRN.CreateTimer(0.05, self._state_timer_cb)
        self._state_timer.Start()

    def _close(self):
        if self._streaming:
            with suppress(Exception):
                self.stop_streaming()
        if self._state_timer:
            self._state_timer.TryStop()
        if self._capture:
            self._capture.release()

    def _state_timer_cb(self, timer_evt):
        s = self._camera_state_type()
        self._seqno += 1
        s.ts = self._date_time_util.TimeSpec3Now()
        s.seqno = self._seqno
        flags = self._imaging_consts["CameraStateFlags"]["ready"]
        if self._streaming:
            flags |= self._imaging_consts["CameraStateFlags"]["streaming"]
        s.state_flags = flags

        self.camera_state.OutValue = s

    @property
    def device_info(self):
        return self._camera_info.device_info

    @property
    def camera_info(self):
        return self._camera_info

    def _cv_mat_to_image(self, mat):

        is_mono = False
        if (len(mat.shape) == 2 or mat.shape[2] == 1):
            is_mono = True

        image_info = self._image_info_type()
        image_info.width = mat.shape[1]
        image_info.height = mat.shape[0]
        if is_mono:
            image_info.step = mat.shape[1]
            image_info.encoding = self._image_consts["ImageEncoding"]["mono8"]
        else:
            image_info.step = mat.shape[1] * 3
            image_info.encoding = self._image_consts["ImageEncoding"]["bgr888"]
        image_info.data_header = self._sensor_data_util.FillSensorDataHeader(self._camera_info.device_info, self._seqno)

        image = self._image_type()
        image.image_info = image_info
        image.data = mat.reshape(mat.size, order='C')
        return image

    def _cv_mat_to_compressed_image(self, mat, quality=100):

        is_mono = False
        if (len(mat.shape) == 2 or mat.shape[2] == 1):
            is_mono = True

        image_info = self._image_info_type()
        image_info.width = mat.shape[1]
        image_info.height = mat.shape[0]

        image_info.step = 0
        image_info.encoding = self._image_consts["ImageEncoding"]["compressed"]
        image_info.data_header = self._sensor_data_util.FillSensorDataHeader(self._camera_info.device_info, self._seqno)

        image = self._compressed_image_type()
        image.image_info = image_info
        res, encimg = cv2.imencode(".jpg", mat, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
        assert res, "Could not compress frame!"
        image.data = encimg
        return image

    def capture_frame(self):
        with self._capture_lock:
            ret, mat = self._capture.read()
            if not ret:
                raise RR.OperationFailedException("Could not read from camera")
            self._seqno += 1
        return self._cv_mat_to_image(mat)

    def capture_frame_compressed(self):
        with self._capture_lock:
            ret, mat = self._capture.read()
            if not ret:
                raise RRN.OperationFailedException("Could not read from camera")
            self._seqno += 1
        return self._cv_mat_to_compressed_image(mat)

    def trigger(self):
        raise RR.NotImplementedException("Not available on this device")

    def frame_threadfunc(self):
        while (self._streaming):
            with self._capture_lock:
                ret, mat = self._capture.read()
                if not ret:
                    # TODO: notify user?
                    self._streaming = False
                    continue
                self._seqno += 1

            self.frame_stream.AsyncSendPacket(self._cv_mat_to_image(mat), lambda: None)
            self.frame_stream_compressed.AsyncSendPacket(self._cv_mat_to_compressed_image(mat), lambda: None)
            self.preview_stream.AsyncSendPacket(self._cv_mat_to_compressed_image(mat, 70), lambda: None)
            device_now = self._date_time_util.FillDeviceTime(self._camera_info.device_info, self._seqno)
            self.device_clock_now.OutValue = device_now

    def start_streaming(self):
        if (self._streaming):
            raise RR.InvalidOperationException("Already streaming")
        self._streaming = True
        t = threading.Thread(target=self.frame_threadfunc)
        t.start()

    def stop_streaming(self):
        if (not self._streaming):
            raise RR.InvalidOperationException("Not streaming")
        self._streaming = False

    @property
    def isoch_downsample(self):
        return self._downsampler.GetClientDownsample(RR.ServerEndpoint.GetCurrentEndpoint())

    @isoch_downsample.setter
    def isoch_downsample(self, value):
        return self._downsampler.SetClientDownsample(RR.ServerEndpoint.GetCurrentEndpoint(), value)

    @property
    def isoch_info(self):
        ret = self._isoch_info()
        ret.update_rate = self._fps
        ret.max_downsample = 100
        ret.isoch_epoch = np.zeros((1,), dtype=self._date_time_utc_type)

    @property
    def capabilities(self):
        return 0x1 | 0x2 | 0x4

    def getf_param(self, name):

        if name == "focus":
            return RR.VarValue(self._capture.get(cv2.CAP_PROP_FOCUS), "double")
        elif name == "exposure":
            return RR.VarValue(self._capture.get(cv2.CAP_PROP_EXPOSURE), "double")
        elif name == "gain":
            return RR.VarValue(self._capture.get(cv2.CAP_PROP_GAIN), "double")
        elif name == "brightness":
            return RR.VarValue(self._capture.get(cv2.CAP_PROP_BRIGHTNESS), "double")
        elif name == "contrast":
            return RR.VarValue(self._capture.get(cv2.CAP_PROP_CONTRAST), "double")
        elif name == "saturation":
            return RR.VarValue(self._capture.get(cv2.CAP_PROP_SATURATION), "double")
        else:
            raise RR.InvalidOperationException("Parameter not found")

    def setf_param(self, name, value):
        if name == "focus":
            self._capture.set(cv2.CAP_PROP_FOCUS, value.data[0])
        elif name == "exposure":
            self._capture.set(cv2.CAP_PROP_EXPOSURE, value.data[0])
        elif name == "gain":
            self._capture.set(cv2.CAP_PROP_GAIN, value.data[0])
        elif name == "brightness":
            self._capture.set(cv2.CAP_PROP_BRIGHTNESS, value.data[0])
        elif name == "contrast":
            self._capture.set(cv2.CAP_PROP_CONTRAST, value.data[0])
        elif name == "saturation":
            self._capture.set(cv2.CAP_PROP_SATURATION, value.data[0])
        else:
            raise RR.InvalidOperationException("Parameter not found")

    @property
    def param_info(self):

        param_info_type = RRN.GetStructureType("com.robotraconteur.param.ParameterInfo")

        data_type = RRN.GetStructureType("com.robotraconteur.datatype.DataType")
        data_type_const = RRN.GetConstants("com.robotraconteur.datatype")

        def p(name, description):
            r = param_info_type()
            r.parameter_identifier = self._identifier_util.CreateIdentifierFromName(name)
            r.data_type = data_type()
            r.data_type.type_code = data_type_const["DataTypeCode"]["double_c"]
            r.description = description
            return r

        return [
            p("focus", "Focus of the camera (CAP_PROP_FOCUS property)"),
            p("exposure", "Exposure of the camera (CAP_PROP_EXPOSURE property)"),
            p("gain", "Gain of the camera (CAP_PROP_GAIN property)"),
            p("brightness", "Brightness of the camera (CAP_PROP_BRIGHTNESS property)"),
            p("contrast", "Contrast of the camera (CAP_PROP_CONTRAST property)"),
            p("saturation", "Saturation of the camera (CAP_PROP_SATURATION property)"),
        ]


def main():
    parser = argparse.ArgumentParser(description="OpenCV based camera driver service for Robot Raconteur")
    parser.add_argument("--camera-info-file", type=argparse.FileType('r'),
                        default=None, required=True, help="Camera info file (required)")
    parser.add_argument("--device-id", type=int, default=0, help="the device to open (default 0)")
    parser.add_argument("--width", type=int, default=1280, help="try to set width of image (default 1280)")
    parser.add_argument("--height", type=int, default=720, help="try to set height of image (default 720)")
    parser.add_argument("--fps", type=int, default=15, help="try to set rate of video capture (default 15 fps)")
    parser.add_argument("--focus", type=float, default=None, help="try to set focus of camera (default unset)")
    parser.add_argument("--exposure", type=float, default=None, help="try to set exposure of camera (default unset)")
    parser.add_argument("--gain", type=float, default=None, help="try to set gain of camera (default  unset)")
    parser.add_argument("--brightness", type=float, default=None,
                        help="try to set brightness of camera (default unset)")
    parser.add_argument("--contrast", type=float, default=None, help="try to set contrast of camera (default unset)")
    parser.add_argument("--saturation", type=float, default=None,
                        help="try to set saturation of camera (default unset)")

    args, _ = parser.parse_known_args()

    rr_args = ["--robotraconteur-jumbo-message=true"] + sys.argv

    # RRN.RegisterServiceTypesFromFiles(['com.robotraconteur.imaging'],True)
    RRC.RegisterStdRobDefServiceTypes(RRN)

    with args.camera_info_file:
        camera_info_text = args.camera_info_file.read()

    info_loader = InfoFileLoader(RRN)
    camera_info, camera_ident_fd = info_loader.LoadInfoFileFromString(
        camera_info_text, "com.robotraconteur.imaging.camerainfo.CameraInfo", "camera")

    attributes_util = AttributesUtil(RRN)
    camera_attributes = attributes_util.GetDefaultServiceAttributesFromDeviceInfo(camera_info.device_info)

    camera = CameraImpl(args.device_id, args.width, args.height, args.fps, camera_info, args.focus,
                        args.exposure, args.gain, args.brightness, args.contrast, args.saturation)
    for _ in range(10):
        camera.capture_frame()

    with RR.ServerNodeSetup("com.robotraconteur.imaging.camera", 59823, argv=rr_args):

        service_ctx = RRN.RegisterService("camera", "com.robotraconteur.imaging.Camera", camera)
        service_ctx.SetServiceAttributes(camera_attributes)

        # Wait for exit
        print("Press Ctrl-C to quit...")
        drekar_launch_process.wait_exit()

        camera._close()


if __name__ == "__main__":
    main()
