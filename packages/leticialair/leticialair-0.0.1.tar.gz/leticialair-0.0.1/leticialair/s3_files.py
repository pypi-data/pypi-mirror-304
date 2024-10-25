import io
import os
import pandas as pd
from pandas import DataFrame
from s3_actions import S3
from typing import Literal


class Object:

    def __init__(self, aws_public_key: str, aws_secret_key: str, aws_session):
        self.aws_public_key = aws_public_key
        self.aws_secret_key = aws_secret_key
        self.aws_session = aws_session

    def _get_binary(self, bucket_origin: str, key: str):
        s3 = self.aws_session.resource("s3")
        object = s3.Object(
            bucket_origin,
            key,
        )

        return object

    def _get_text(self, bucket_origin: str, key: str):
        response_object = S3(self.aws_public_key, self.aws_secret_key).get_object(
            Bucket=bucket_origin, Key=key
        )
        return response_object


class Parquet(Object):

    def __init__(self, pa_schema=None):
        super().__init__()
        self.pa_schema = pa_schema

    def get(self, bucket_origin: str, key: str, engine="pyarrow", **kwargs):
        buffer = io.BytesIO()
        object_parquet = self._get_binary(bucket_origin, key)
        object_parquet.download_fileobj(buffer)
        df_parquet = pd.read_parquet(buffer, engine=engine, **kwargs)
        return df_parquet

    def put(
        self,
        df_parquet: DataFrame,
        bucket_destination: str,
        key: str,
        file_name: str,
        aws_access_key_id: str,
        aws_secret_access_key: str,
    ):
        S3(aws_access_key_id, aws_secret_access_key).put_dataframe_parquet(
            df_parquet,
            bucket_destination,
            key,
            file_name,
            schema=self.pa_schema,
        )


class CSV(Object):

    def __init__(
        self, encoding: str, sep: Literal[",", ";"] = ",", errors: str = "strict"
    ):
        super().__init__()
        self.encoding = encoding
        self.sep = sep
        self.errors = errors

    def get(
        self, bucket_origin: str, key: str, dtype=str, skip_blank_lines=True, **kwargs
    ):
        object_csv = self._get_text(bucket_origin, key)
        df_csv = pd.read_csv(
            object_csv.get("Body"),
            dtype=dtype,
            sep=self.sep,
            encoding=self.encoding,
            skip_blank_lines=skip_blank_lines,
            **kwargs,
        )
        return df_csv

    def put(
        self,
        df_csv: DataFrame,
        bucket_destination: str,
        key: str,
        file_name: str,
        aws_access_key_id: str,
        aws_secret_access_key: str,
    ):
        S3(aws_access_key_id, aws_secret_access_key).put_dataframe_csv(
            df_csv,
            bucket_destination,
            key,
            file_name,
            encoding=self.encoding,
            errors=self.errors,
        )


class XLSX(Object):

    def __init__(self, header: int = 0, sheet_name: str = None):
        super().__init__()
        self.header = header
        self.sheet_name = sheet_name

    def get(self, bucket_origin: str, key: str, **kwargs):
        buffer = io.BytesIO()
        object_xlsx = self._get_binary(bucket_origin, key)
        object_xlsx.download_fileobj(buffer)
        if self.sheet_name != None:
            df_xlsx = pd.read_excel(
                buffer,
                engine="openpyxl",
                header=self.header,
                sheet_name=self.sheet_name,
                **kwargs,
            )
            return df_xlsx
        df_xlsx = pd.read_excel(buffer, engine="openpyxl", header=self.header, **kwargs)
        return df_xlsx

    def put(
        self,
        df_xlsx: DataFrame,
        bucket_destination: str,
        key: str,
        file_name: str,
        aws_public_key: str,
        aws_secret_key: str,
        sheet_name: str = "Planilha1",
    ):
        key = f"{key}/{file_name}"
        with io.BytesIO() as output:
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                df_xlsx.to_excel(writer, sheet_name, index=False)
            data = output.getvalue()
        S3(aws_public_key, aws_secret_key).put_object(
            Bucket=bucket_destination, Key=key, Body=data
        )


class HTML(Object):
    def __init__(self):
        super().__init__()

    def get(self, bucket_origin: str, key: str):
        object_html = self._get_text(bucket_origin, key)
        df_html = pd.read_html(object_html.get("Body"))[0]
        return df_html


class XLS(Object):
    def __init__(self):
        super().__init__()

    def get(self, bucket_origin: str, key: str):
        object_xls = self._get_text(bucket_origin, key)
        df_xls = pd.read_excel(object_xls.get("Body"), engine="xlrd")[0]
        return df_xls
