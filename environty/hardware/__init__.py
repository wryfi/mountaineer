from enumfields import Enum


class RackOrientation(Enum):
    FRONT = 1
    REAR = 2

    class Labels:
        FRONT = 'Front-facing'
        REAR = 'Rear-facing'


class SwitchSpeed(Enum):
    TEN = 1
    ONE_HUNDRED = 2
    GIGABIT = 3
    TEN_GIGABIT = 4
    FORTY_GIGABIT = 5

    class Labels:
        TEN = '10 Mbps'
        ONE_HUNDRED = '100 Mbps'
        GIGABIT = '1 Gbps'
        TEN_GIGABIT = '10 Gbps'
        FORTY_GIGABIT = '40 Gbps'


class SwitchInterconnect(Enum):
    RJ45 = 1
    TWINAX = 2

    class Labels:
        RJ45 = 'RJ-45'
        TWINAX = 'Twinaxial'


class RackDepth(Enum):
    FULL = 1
    HALF = 2
    QUARTER = 4

    class Labels:
        FULL = 'Full depth'
        HALF = 'Half depth'
        QUARTER = 'Quarter depth'


class CpuManufacturer(Enum):
    INTEL = 1
    AMD = 2
    QUALCOMM = 3
    NVIDIA = 4
    ORACLE = 5
    OTHER = 9

    class Labels:
        INTEL = 'Intel'
        AMD = 'AMD'
        QUALCOMM = 'Qualcomm'
        NVIDIA = 'nVidia'
        ORACLE = 'Oracle'
        OTHER = 'Other'
