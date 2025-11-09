from client.grpc_client import GrpcClient


class BaseProcessor:
    def __init__(self, url: str, max_tokens: int, model_name: str) -> None:
        self.grpc_client = GrpcClient(url=url, max_tokens=max_tokens, model_name=model_name)
