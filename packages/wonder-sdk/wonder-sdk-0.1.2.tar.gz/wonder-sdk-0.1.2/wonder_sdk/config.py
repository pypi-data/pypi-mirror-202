import os

class EnvironmentTypes:
    production = 'production'
    staging = 'staging'

class WonderSdkConfig:
    def __init__(self, environment=None, project_id=None, subscription_name=None, process_count=None) -> None:
        self.environment_types = EnvironmentTypes()

        self.environment = environment if environment else os.environ.get('ENVIRONMENT', self.environment_types.staging)

        self.project_id = project_id if project_id else os.environ.get('PROJECT_ID', default=None)
        
        self.subscription_name = subscription_name if subscription_name else os.environ.get('SUBSCRIPTION_NAME', default=None)

        self.process_count = process_count if process_count else os.environ.get('PROCESS_COUNT', default=1)