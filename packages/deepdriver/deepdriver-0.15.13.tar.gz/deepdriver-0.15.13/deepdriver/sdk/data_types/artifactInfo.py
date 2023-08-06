from deepdriver.sdk.interface.grpc_interface_pb2 import ArtifactEntry
from typing import  List

class ArtifactInfo():
    def __init__(self, artifact_id: int, artifact_name: str, artifact_type: str,  artifact_digest: str,artifact_scope:str,artifact_mode:str, artifact_description:str,last_file_yn: str, entry_list: List[ArtifactEntry]):
        self.artifact_id = artifact_id
        self.artifact_name = artifact_name
        self.artifact_type = artifact_type
        self.artifact_digest = artifact_digest
        self.last_file_yn = last_file_yn
        self.entry_list = entry_list
        self.artifact_scope =artifact_scope
        self.artifact_description =artifact_description
        self.artifact_mode =artifact_mode
