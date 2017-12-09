from enumfields import Enum


class RackOrientation(Enum):
    FRONT = 1
    REAR = 2

    class Labels:
        FRONT = 'Front-facing'
        REAR = 'Rear-facing'


class SwitchSpeed(Enum):
    TEN = 10
    ONE_HUNDRED = 100
    GIGABIT = 1000
    TEN_GIGABIT = 10000
    FORTY_GIGABIT = 40000

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
    QUARTER = 1
    HALF = 2
    THREE_QUARTER = 3
    FULL = 4

    class Labels:
        QUARTER = 'Quarter depth'
        HALF = 'Half depth'
        THREE_QUARTER = 'Three-quarter depth'
        FULL = 'Full depth'


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
        OTHER = 'other'


class CabinetAttachmentMethod(Enum):
    CAGE_NUT_95 = 1
    DIRECT_ATTACH = 2

    class Labels:
        CAGE_NUT_95 = '9.5mm cage nut'
        DIRECT_ATTACH = 'direct attachment'


class CabinetFastener(Enum):
    UNF_10_32 = 1
    UNC_12_24 = 2
    M5 = 5
    M6 = 6
    OTHER = 9

    class Labels:
        UNF_10_32 = 'UNF 10-32'
        UNC_12_24 = 'UNC 12-24'
        M5 = 'M5'
        M6 = 'M6'
        OTHER = 'other'
