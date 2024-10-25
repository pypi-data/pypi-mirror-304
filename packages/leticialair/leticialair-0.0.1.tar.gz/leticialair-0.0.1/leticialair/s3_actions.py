import boto3
import botocore
import io
import logging
from datetime import datetime
from pandas import DataFrame


class AuthAws:

    def __init__(self, aws_server_public_key: str, aws_server_secret_key: str):
        self.AWS_SERVER_PUBLIC_KEY = aws_server_public_key
        self.AWS_SERVER_SECRET_KEY = aws_server_secret_key
        self.AWS_CONFIG_CLIENT = botocore.config.Config(
            read_timeout=1800, connect_timeout=1800, retries={"max_attempts": 1}
        )

    def session(self) -> object:
        """
        Metódo session inicia uma sessão na aws utilizando public e secret key

        ---

        Parâmetros:
            None

        Doc:https://boto3.amazonaws.com/v1/documentation/api/latest/guide/session.html

        """
        try:
            session = boto3.Session(
                aws_access_key_id=self.AWS_SERVER_PUBLIC_KEY,
                aws_secret_access_key=self.AWS_SERVER_SECRET_KEY,
            )
            return session
        except Exception as err:
            logging.error(f"Houve um erro na autenticação da session: {err}")

    def client(self, service: str) -> object:
        """
        Cria um client low-level para acessar serviços aws a partir de uma sessão.

        ---

        Parâmetros:
            - service [required]: str -> Nome do serviço AWS que será acessado.

        Doc: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/clients.html


        """

        session = self.session()

        try:
            client = session.client(service, config=self.AWS_CONFIG_CLIENT)
            return client

        except Exception as err:
            logging.error(f"Houve um erro na criação do cliente: {err}")


class S3:

    def __init__(self, aws_access_key_id: str, aws_secret_access_key: str):
        self.aws_access_key_id: str
        self.aws_secret_access_key: str
        self.data_hoje = datetime.now().date().strftime(format="%Y.%m.%d")
        self.auth_aws = AuthAws(aws_access_key_id, aws_secret_access_key)
        self.client = self.auth_aws.client("s3")
        self.session = self.auth_aws.session()

    def list_buckets(self) -> list:
        """
        Método que retorna uma lista com os nomes de todos os buckets s3 existentes na conta.

        ---

        Parâmetros:
            None

        Retorna:
            list -> Lista de strings

        ---


        Doc: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html
        """
        try:
            session_resource_s3 = self.session.resource("s3")

            list = [bucket.name for bucket in session_resource_s3.buckets.all()]

            return list

        except Exception as err:
            raise logging.ERROR(f"Houve um erro ao gerar a lista de Buckets: {err}")

    def list_objects(self, **kwargs) -> dict:
        """
        Método para retornar uma lista de objetos de um bucket s3 selecionado.

        Atenção!! Atualmente utilizando a versão dois da list_objects (ainda não totalmente implementada)

        São retornados no máximo 1000 blocos no request. Caso seja necessário retornar mais que isso
        deve-se usar o método de paginação.

        ---

        Parâmetros aceitos no kwargs
        ----------------------------
            Bucket [required]: String
                Nome do bucket selecionado
            Delimiter: String
                Um delimitador utilizado para group keys
            EncodingType: String
                Tipo de encoding utilizado pelo S3 para encodar chaves de objetos na response
            MaxKeys: Integer
                Define o número máximo de keys retornadas na response. Default 1000.
                Pode conter menos mas nunca mais de 1000.
            Prefix: String
                Limita o response por um prefixo específico.
            ContinuationToken: String
                Se o continuationToken for incluído é enviado junto da request
            FetchOwner: Bool

            StartAfter: String

            RequestPayer: String(requester)

            ExpectedBucketOwner: String


        ---

        Doc: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/list_objects_v2.html

        """
        try:
            response = self.client.list_objects_v2(**kwargs)

            return response

        except Exception as err:
            raise logging.error(f"Houve um erro ao fazer o list dos objects: {err}")

    def get_object(self, **kwargs) -> object:
        """
        Método para leitura de um objeto dentro de um bucket

        ---

        Parâmetros aceitos no kwargs
        ----------------------------

        Bucket [Required]: String
            Nome do bucket
        IfMatch: String

        IfModifiedSince: Datetime(2015, 1, 1)

        IfNoneMatch: String

        IfUnmodifiedSince: Datetime(2015, 1, 1)

        Key: String
            Key identificadora do objeto

        Range: String

        ResponseCacheControl: String

        ResponseContentDisposition: String

        ResponseContentEncoding: String

        ResponseContentLanguage: String

        ResponseContentType: String

        ResponseExpires: Datetime(2015, 1, 1)

        VersionId: String

        SSECustomerAlgorithm: String

        SSECustomerKey: String

        RequestPayer: String ['requester'],

        PartNumber: Integer

        ExpectedBucketOwner: String

        ChecksumMode: String ['ENABLED']

        ---

        Doc: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/get_object.html


        """

        try:
            response = self.client.get_object(**kwargs)

            return response

        except Exception as err:
            raise logging.error(f"Houve um erro ao fazer o get no object: {err}")

    def put_object(self, **kwargs) -> object:
        """

        Método para input de objects no bucket

        ---

        Parâmetros aceitos no kwargs
        ----------------------------

        ACL: String ['private'|'public-read'|'public-read-write'|'authenticated-read'|'aws-exec-read'|'bucket-owner-read'|'bucket-owner-full-control']
        Body: b'bytes'|file
        Bucket: String
        CacheControl: String
        ContentDisposition: String
        ContentEncoding: String
        ContentLanguage: String
        ContentLength: Integer
        ContentMD5: String
        ContentType: String
        ChecksumAlgorithm: String ['CRC32'|'CRC32C'|'SHA1'|'SHA256']
        ChecksumCRC32: String
        ChecksumCRC32C: String
        ChecksumSHA1: String
        ChecksumSHA256: String
        Expires: Datetime(2015, 1, 1)
        GrantFullControl: String
        GrantRead: String
        GrantReadACP: String
        GrantWriteACP: String
        Key: String
        Metadata: Dict {'string': 'string'}
        ServerSideEncryption: String ['AES256'|'aws:kms'|'aws:kms:dsse']
        StorageClass: String ['STANDARD'|'REDUCED_REDUNDANCY'|'STANDARD_IA'|'ONEZONE_IA'|'INTELLIGENT_TIERING'|'GLACIER'|'DEEP_ARCHIVE'|'OUTPOSTS'|'GLACIER_IR'|'SNOW']
        WebsiteRedirectLocation: String
        SSECustomerAlgorithm: String
        SSECustomerKey: String
        SSEKMSKeyId: String
        SSEKMSEncryptionContext: String
        BucketKeyEnabled: Bool
        RequestPayer: String ['requester']
        Tagging: String
        ObjectLockMode: String ['GOVERNANCE'|'COMPLIANCE']
        ObjectLockRetainUntilDate: Datetime(2015, 1, 1)
        ObjectLockLegalHoldStatus: String ['ON'|'OFF']
        ExpectedBucketOwner: String


        Retorna:
            object: Retorna um objeto de streaming via body

        ---

        Doc: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/put_object.html

        """
        try:
            response = self.client.put_object(**kwargs)

            return response

        except Exception as err:
            raise logging.ERROR(f"Houve um erro ao dar put no object: {err}")

    def put_dataframe_csv(
        self,
        df: DataFrame,
        bucket_aws: str,
        path_aws_s3: str,
        nome_arquivo: str,
        encoding: str = "latin-1",
        errors="replace",
        sep=";",
    ) -> str:
        try:
            with io.BytesIO() as csv_buffer:
                df.to_csv(
                    csv_buffer,
                    index=False,
                    sep=sep,
                    encoding=encoding,
                    errors=errors,
                )

                response = self.put_object(
                    ACL="private",
                    Body=csv_buffer.getvalue(),
                    Bucket=bucket_aws,
                    Key=f"{path_aws_s3}/{nome_arquivo}.csv",
                )

                return response["ETag"]

        except Exception as err:
            raise logging.error(f"Houve um erro no upload do arquivo csv: {err}")

    def put_dataframe_parquet(
        self,
        df: DataFrame,
        bucket_aws: str,
        path_aws_s3: str,
        nome_arquivo: str,
        schema: str,
        compression: str = "gzip",
    ) -> None:
        try:
            with io.BytesIO() as parquet_buffer:
                df.to_parquet(
                    parquet_buffer,
                    engine="pyarrow",
                    index=False,
                    compression=compression,
                    schema=schema,
                )

                response = self.put_object(
                    ACL="private",
                    Body=parquet_buffer.getvalue(),
                    Bucket=bucket_aws,
                    Key=f"{path_aws_s3}/{nome_arquivo}.parquet",
                )

                return response["ETag"]

        except Exception as err:
            raise ValueError(f"Houve um erro no upload do arquivo parquet: {err}")

    def put_file_bpt(
        self, binary_bpt: str, bucket_aws: str, path_aws_s3: str, nome_arquivo: str
    ) -> None:
        try:
            with io.BytesIO() as buffer:
                buffer.write(binary_bpt)
                buffer.seek(0)
                self.put_object(
                    ACL="private",
                    Body=buffer.getvalue(),
                    Bucket=bucket_aws,
                    Key=f"{path_aws_s3}/{nome_arquivo}.bpt",
                )

        except Exception as err:
            raise ValueError(f"Houve um erro no upload do arquivo bpt: {err}")
