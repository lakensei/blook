from pathlib import Path


class LocalStorage:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)

    def save_file(self, file, filename: str):
        file_path = self.base_path / filename
        with open(file_path, "wb") as f:
            f.write(file.read())
        return str(file_path)

    def delete_file(self, filename: str):
        file_path = self.base_path / filename
        if file_path.exists():
            file_path.unlink()


class OSSStorage:
    def __init__(self, access_key: str, secret_key: str, bucket_name: str, endpoint: str):
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket_name = bucket_name
        self.endpoint = endpoint

    def save_file(self, file, filename: str):
        client = AcsClient(self.access_key, self.secret_key, self.endpoint)
        request = PutObjectRequest.PutObjectRequest(self.bucket_name, filename, file.read())
        response = client.do_action_with_exception(request)
        return response

    def delete_file(self, filename: str):
        client = AcsClient(self.access_key, self.secret_key, self.endpoint)
        # 删除文件逻辑
        pass