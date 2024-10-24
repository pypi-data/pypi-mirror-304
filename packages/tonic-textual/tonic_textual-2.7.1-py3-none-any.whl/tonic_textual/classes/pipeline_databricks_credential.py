from tonic_textual.classes.enums.file_source import FileSource


class PipelineDatabricksCredential(dict):

    def __init__(self, url: str, access_token: str):
        self.file_source=FileSource.databricks
        self.url=url
        self.access_token=access_token

        dict.__init__(
            self,
            url=url,
            accessToken=access_token
        )

    def to_dict(self):
        return {
            'url': self.url,
            'accessToken': self.access_token
        }