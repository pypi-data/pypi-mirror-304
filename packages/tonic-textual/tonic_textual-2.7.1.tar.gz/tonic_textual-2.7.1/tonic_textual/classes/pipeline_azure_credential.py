from tonic_textual.classes.enums.file_source import FileSource


class PipelineAzureCredential(dict):

    def __init__(self, account_name: str, account_key: str):
        self.file_source=FileSource.azure

        self.account_name=account_name
        self.account_key=account_key

        dict.__init__(
            self,
            accountName=account_name,
            accountKey=account_key
        )

    def to_dict(self):
        return {
            'accountName': self.account_name,
            'accountKey': self.account_key
        }