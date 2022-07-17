from minio import Minio

client = Minio(
        "host.docker.internal:9000",
        access_key="minio",
        secret_key="minio123",
        secure=False
    )