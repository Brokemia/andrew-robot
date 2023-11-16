import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element

class PipetteSlot:
    vertical_offset: int = None
    start_position: (int, int, int) = None
    grab_position: (int, int, int) = None
    release_position: (int, int, int) = None

    def __init__(self,
                 vertical_offset: int,
                 start_position: (int, int, int),
                 grab_position: (int, int, int),
                 release_position: (int, int, int)) -> None:
        self.vertical_offset = vertical_offset
        self.start_position = start_position
        self.grab_position = grab_position
        self.release_position = release_position

    def __repr__(self) -> str:
        return f'PipetteSlot(vertical_offset={self.vertical_offset}, start_position={self.start_position}, grab_position={self.grab_position}, release_position={self.release_position})'


class AndrewConfig:
    def __init__(self, xml_path):
        self.tree = ET.parse(xml_path)
        self.root = self.tree.getroot()
        
        self._load()

    def _load(self):
        # TODO most of these are not yet implemented
        # Add them as they are needed
        self._load_linear_movement(self.root.find('linearMovement'))
        self._load_camera_focus(self.root.find('cameraFocus'))
        self._load_hand_camera_focus_offset(self.root.find('handCameraFocusOffset'))
        self._load_barcode_fit(self.root.find('barcodeFit'))
        self._load_set_volume(self.root.find('setVolume'))
        self._load_camera_geometry(self.root.find('cameraGeometry'))
        self._load_pipette_geometry(self.root.find('pipetteGeometry'))
        self._load_optical_nest(self.root.find('opticalNest'))
        self._load_pipette_grab_and_release(self.root.find('pipetteGrabAndRelease'))
        self._load_twister(self.root.find('twister'))
        self._load_additional_consumable_offset(self.root.find('additionalConsumableOffset'))
        self._load_thumb(self.root.find('thumb'))
        self._load_tool(self.root.find('tool'))
        self._load_hardware_version(self.root.find('hardwareVersion'))
        self._load_tip_geometry_offset(self.root.find('tipGeometryOffset'))
        self._load_image_processor(self.root.find('imageProcessor'))
        self._load_camera(self.root.find('camera'))
        self._load_arm_deflection(self.root.find('armDeflection'))

    def _load_linear_movement(self, element):
        pass

    def _load_camera_focus(self, element):
        pass

    def _load_hand_camera_focus_offset(self, element):
        pass

    def _load_barcode_fit(self, element):
        pass

    def _load_set_volume(self, element):
        pass

    def _load_camera_geometry(self, element):
        pass

    def _load_pipette_geometry(self, element):
        pass

    def _load_optical_nest(self, element):
        pass

    def _load_pipette_grab_and_release(self, element: Element):
        self.pipette_height = element.find('height').text
        self.pipette_pre_release_height = element.find('preReleaseHeight').text

        self.pipette_slots = {}
        for e in element:
            if e.tag.startswith('slot'):
                self.pipette_slots[e.tag] = self._load_pipette_slot(e)

    def _load_pipette_slot(self, element: Element) -> PipetteSlot:
        return PipetteSlot(
            int(element.find('verticalOffset').text),
            self._load_arm_thetas(element.find('startPosition')),
            self._load_arm_thetas(element.find('grabPosition')),
            self._load_arm_thetas(element.find('releasePosition')),
        )

    def _load_arm_thetas(self, element: Element) -> (int, int, int):
        return (
            int(element.find('th1').text),
            int(element.find('th2').text),
            int(element.find('th3').text),
        )

    def _load_twister(self, element):
        pass

    def _load_additional_consumable_offset(self, element):
        pass

    def _load_thumb(self, element):
        pass

    def _load_tool(self, element):
        pass

    def _load_hardware_version(self, element):
        pass

    def _load_tip_geometry_offset(self, element):
        pass

    def _load_image_processor(self, element):
        pass

    def _load_camera(self, element):
        pass

    def _load_arm_deflection(self, element):
        pass

def main():
    config = AndrewConfig('D:\\Resources\\andrew.xml')
    print(config.tree)
    print(config.root)
    print(config.root.tag)
    print(config.root.attrib)
    print(config.pipette_slots)

if __name__ == '__main__':
    main()