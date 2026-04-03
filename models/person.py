class Person:
    def __init__(
        self,
        name: str = '',
        license_plate: str = '',
        vehicle_type: str = '',
        remarks: str = '',
        dirty_data: bool = False,
    ):
        self.name = name
        self.license_plate = license_plate
        self.vehicle_type = vehicle_type
        self.remarks = remarks
        self._dirty_data = dirty_data

    def is_empty(self) -> bool:
        return not self.license_plate and not self.vehicle_type

    def has_no_license_plate(self) -> bool:
        return not self.license_plate

    def is_dirty_data(self) -> bool:
        return self._dirty_data

    def set_dirty_data(self, value: bool):
        self._dirty_data = value
