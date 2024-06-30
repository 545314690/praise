import subprocess
from typing import List

import WSDiscovery
from camera_discovery import CameraDiscovery
from onvif import ONVIFCamera

import zeep  # 额外加的


def ws_discovery(scope = None) -> List:
    """Discover cameras on network using onvif discovery.

    Returns:
        List: List of ips found in network.
    """
    lst = list()
    if(scope == None):
        cmd = 'hostname -f'
        scope = subprocess.check_output(cmd, shell=True).decode('utf-8')
    wsd = WSDiscovery.WSDiscovery()
    wsd.start()
    ret = wsd.searchServices(timeout=5)
    for service in ret:
        get_ip = str(service.getXAddrs())
        get_types = str(service.getTypes())
        for ip_scope in scope.split():
            result = get_ip.find(ip_scope.split('.')[0] + '.' + ip_scope.split('.')[1])
            if result > 0 and get_types.find('onvif') > 0:
                #下面是更改的代码
                #string_result = get_ip[result:result+13]
                string_result = get_ip[result:].split('/')[0]
                string_result = string_result.split(':')
                if len(string_result)>1:
                    lst.append([string_result[0],string_result[1]])
                else:
                    lst.append([string_result[0],'80'])
    wsd.stop()
    lst.sort()
    return lst



class CameraONVIF:
    """This class is used to get the information from all cameras discovered on this specific
    network."""

    def __init__(self, ip,user, password, port):
        """Constructor.

        Args:
            ip (str): Ip of the camera.
            user (str): Onvif login.
            password (str): Onvif password.
        """
        self.camera_media = None
        self.cam_ip = ip
        self.cam_user = user
        self.cam_password = password
        self.cam_port = port #加入port参数




    def zeep_pythonvalue(self, xmlvalue):  # 额外加的
        return xmlvalue

    def camera_start(self):
        """Start module.
        """
        mycam = ONVIFCamera(self.cam_ip, self.cam_port, self.cam_user, self.cam_password, no_cache=True)
        media = mycam.create_media_service()

        zeep.xsd.simple.AnySimpleType.pythonvalue = self.zeep_pythonvalue  # 额外加的

        media_profile = media.GetProfiles()[0]
        self.mycam = mycam
        self.camera_media = media
        self.camera_media_profile = media_profile

    def get_hostname(self) -> str:
        """Find hostname of camera.

        Returns:
            str: Hostname.
        """
        resp = self.mycam.devicemgmt.GetHostname()
        return resp.Name

    def get_manufacturer(self) -> str:
        """Find manufacturer of camera.

        Returns:
            str: Manufacturer.
        """
        resp = self.mycam.devicemgmt.GetDeviceInformation()
        return resp.Manufacturer

    def get_model(self) -> str:
        """Find model of camera.

        Returns:
            str: Model.
        """
        resp = self.mycam.devicemgmt.GetDeviceInformation()
        return resp.Model

    def get_firmware_version(self) -> str:
        """Find firmware version of camera.

        Returns:
            str: Firmware version.
        """
        resp = self.mycam.devicemgmt.GetDeviceInformation()
        return resp.FirmwareVersion

    def get_mac_address(self) -> str:
        """Find serial number of camera.

        Returns:
            str: Serial number.
        """
        resp = self.mycam.devicemgmt.GetDeviceInformation()
        return resp.SerialNumber

    def get_hardware_id(self) -> str:
        """Find hardware id of camera.

        Returns:
            str: Hardware Id.
        """
        resp = self.mycam.devicemgmt.GetDeviceInformation()
        return resp.HardwareId

    def get_resolutions_available(self) -> List:
        """Find all resolutions of camera.

        Returns:
            tuple: List of resolutions (Width, Height).
        """
        request = self.camera_media.create_type('GetVideoEncoderConfigurationOptions')
        request.ProfileToken = self.camera_media_profile.token
        config = self.camera_media.GetVideoEncoderConfigurationOptions(request)
        return [(res.Width, res.Height) for res in config.H264.ResolutionsAvailable]

    def get_frame_rate_range(self) -> int:
        """Find the frame rate range of camera.

        Returns:
            int: FPS min.
            int: FPS max.
        """
        request = self.camera_media.create_type('GetVideoEncoderConfigurationOptions')
        request.ProfileToken = self.camera_media_profile.token
        config = self.camera_media.GetVideoEncoderConfigurationOptions(request)
        return config.H264.FrameRateRange.Min, config.H264.FrameRateRange.Max

    def get_date(self) -> str:
        """Find date configured on camera.

        Returns:
            str: Date in string.
        """
        datetime = self.mycam.devicemgmt.GetSystemDateAndTime()
        return datetime.UTCDateTime.Date

    def get_time(self) -> str:
        """Find local hour configured on camera.

        Returns:
            str: Hour in string.
        """
        datetime = self.mycam.devicemgmt.GetSystemDateAndTime()
        return datetime.UTCDateTime.Time

    def is_ptz(self) -> bool:
        """Check if camera is PTZ or not.

        Returns:
            bool: Is PTZ or not.
        """
        resp = self.mycam.devicemgmt.GetCapabilities()
        return bool(resp.PTZ)

    def get_rtsp(self):
        obj = self.camera_media.create_type('GetStreamUri')
        obj.StreamSetup = {'Stream': 'RTP-Unicast', 'Transport': {'Protocol': 'RTSP'}}
        obj.ProfileToken = self.camera_media_profile.token
        res_uri = self.camera_media.GetStreamUri(obj)['Uri']
        return res_uri


if __name__ == '__main__':
    # print(CameraDiscovery.ws_discovery('192.168.199.1'))
    # cam_list =ws_discovery()
    # print(cam_list)
    # mycam = ONVIFCamera('192.168.199.189', 2000, 'admin', 'Test123', no_cache = True)
    cam = CameraONVIF('192.168.199.189', 'admin', 'Test123', 2000)
    cam.camera_start()
    print(cam.get_rtsp())
