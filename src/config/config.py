import yaml
import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()
        self.settings = self._load_yaml()
    
    def _load_yaml(self):
        with open('src/config/settings.yaml', 'r') as file:
            return yaml.safe_load(file)
    
    @property
    def risk_thresholds(self):
        return self.settings['risk_scoring']['thresholds']
    
    @property
    def risk_weights(self):
        return self.settings['risk_scoring']['weights']
    
    @property
    def data_paths(self):
        return self.settings['data']
    
    @property
    def model_settings(self):
        return self.settings['model']