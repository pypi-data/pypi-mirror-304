from typing import Optional

class PipelineAwsCredential(dict):

    def __init__(self, aws_access_key_id:str, aws_secret_access_key: str, aws_region: str, aws_session_token: Optional[str]=None):
        self.aws_access_key=aws_access_key_id
        self.aws_secret_key=aws_secret_access_key
        self.aws_region=aws_region
        self.aws_session_token=aws_session_token
        
        dict.__init__(
                    self,
                    accessKey=aws_access_key_id,
                    secretKey=aws_secret_access_key,
                    region=aws_region,
                    sessionToken=aws_session_token,
                )

    def to_dict(self):
        return {
            'accessKey': self.aws_access_key,
            'secretKey': self.aws_secret_key,
            'region': self.aws_region,
            'sessionToken': self.aws_session_token,
        }