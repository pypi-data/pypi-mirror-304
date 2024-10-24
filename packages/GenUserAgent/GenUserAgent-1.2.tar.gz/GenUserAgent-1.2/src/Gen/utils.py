import random
from typing import List

class UserAgentGenerator:
    def __init__(self):
        # Khởi tạo các thuộc tính với dữ liệu cần thiết
        self.app_version = 'FBAV/486.0.0.55.70'  # Phiên bản ứng dụng cố định
        self.build_version = 'FBBV/652720741'   # Phiên bản build cố định
        self.languages = ['vi_VN', 'en_US', 'en_GB']
        self.carriers = [
            'Viettel', 'Verizon', 'O2', 'MobiFone', 
            'T-Mobile', 'Vinaphone', 'Sprint', 'EE'
        ]
        self.device_models = {
                                'samsung': ['SM-G988B', 'SM-G988U', 'SM-G988W', 
                                            'SM-G988F', 'SM-G988N', 'SM-S908N', 
                                            'SM-S901N', 'SM-S906N', 'SM-G977N', 
                                            'SM-G973N', 'SM-G975N', 'SM-N976N'],
                                
                                'OPPO': ['CPH2401', 'CPH2307', 'CPH2173', 
                                        'CPH2025', 'PFEM10', 'PEEM00', 
                                        'PEEM10', 'PENM00', 'PFJM10', 'PHJM10', 'PFPM00'],

                                'Xiaomi': ['23049RAD8C', '2210132C', '2210132G', 
                                        '2107113SG', '2201122C', '2112123AC', 
                                        '2109119DG', 'M2102K1AC', 'M2011J18C', 
                                        'M2007J3SC', 'M2007J1SC']
                            }

        self.android_versions = [f'FBSV/{version}' for version in ['11', '12', '13']]
        self.optimization_profiles = [f'FBOP/{i}' for i in range(1, 5)]
        self.manufacturer = random.choice(['samsung','OPPO','Xiaomi'])
        self.brand = self.manufacturer.lower() if self.manufacturer == 'Xiaomi' else self.manufacturer


    def generate_display_metrics(self) -> str:
        """Generate random display metrics."""
        density = round(random.uniform(2.0, 3.5), 1)  # Density between 2.0 and 3.5
        screen_sizes = {
            'Xiaomi': [
                {'width': 1080, 'height': 2400},  # Xiaomi Mi 11, Redmi Note 10
                {'width': 1080, 'height': 2340},  # Xiaomi Mi 9, Redmi Note 8
                {'width': 1440, 'height': 3200},  # Xiaomi Mi 11 Ultra
                {'width': 720,  'height': 1520},  # Redmi 7A
                {'width': 1080, 'height': 2160}   # Xiaomi Mi Mix 2
            ],
            'OPPO': [
                {'width': 1080, 'height': 2400},  # Oppo Find X3 Pro
                {'width': 1080, 'height': 2340},  # Oppo Reno 5
                {'width': 720,  'height': 1600},  # Oppo A53
                {'width': 1440, 'height': 3168},  # Oppo Find X2 Pro
                {'width': 1080, 'height': 1920}   # Oppo R9s
            ],
            'samsung': [
                {'width': 1440, 'height': 3200},  # Samsung Galaxy S21 Ultra
                {'width': 1080, 'height': 2400},  # Samsung Galaxy A72
                {'width': 720,  'height': 1600},  # Samsung Galaxy A12
                {'width': 1440, 'height': 2960},  # Samsung Galaxy S9+
                {'width': 1080, 'height': 2280}   # Samsung Galaxy A50
            ]
        }

        screen_choice = random.choice(screen_sizes[self.manufacturer])
        width = screen_choice['width']
        height = screen_choice['height']
        return f'density={density},width={width},height={height}'

    def generate_user_agent(self) -> str:
        """Generate a random user-agent string."""
        user_agent_components = {
            "FBAN": "FB4A",
            "FBAV": self.app_version,
            "FBBV": self.build_version,
            "FBDM": f"{{{self.generate_display_metrics()}}}",
            "FBLC": random.choice(self.languages),
            "FBRV": "0",
            "FBCR": random.choice(self.carriers),
            "FBMF": self.manufacturer,
            "FBBD": self.brand,
            "FBPN": "com.facebook.katana",
            "FBDV": random.choice(self.device_models[self.manufacturer]),
            "FBSV": random.choice(self.android_versions),
            "FBOP": random.choice(self.optimization_profiles),
            "FBCA": "arm64-v8a"
        }

        user_agent = ";".join(f"{key}/{value}" for key, value in user_agent_components.items())
        return f"[{user_agent}]"

