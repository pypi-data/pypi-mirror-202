import os

class WonderSdkConfig:
    def __init__(self, environment=None, project_id=None, subscription_name=None,) -> None:
        self.environment = environment if environment else os.environ.get('ENVIRONMENT', 'staging')

        self.project_id = project_id if project_id else os.environ.get('PROJECT_ID', default=None)
        
        self.subscription_name = subscription_name if subscription_name else os.environ.get('SUBSCRIPTION_NAME', default=None)