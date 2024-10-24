"""
  DownloadFromSmartSheet
  Download an Excel file from SmartSheet.
"""
import asyncio
from collections.abc import Callable
from typing import Dict
import aiofiles
from ..exceptions import ComponentError, FileNotFound
from .DownloadFrom import DownloadFromBase


class DownloadFromSmartSheet(DownloadFromBase):
    """
    DownloadFromSmartSheet

    Overview

        Download an Excel file or CSV file from SmartSheet.

    Properties (inherited from DownloadFromBase)

    .. table:: Properties
        :widths: auto

        +--------------------+----------+-----------+----------------------------------------------------------------------+
        | Name               | Required | Summary                                                                          |
        +--------------------+----------+-----------+----------------------------------------------------------------------+
        | credentials        |   Yes    | Credentials to establish connection with SharePoint site (username and password) |
        |                    |          | get credentials from environment if null.                                        |
        +--------------------+----------+-----------+----------------------------------------------------------------------+
        | create_destination |   No     | Boolean flag indicating whether to create the destination directory if it        |
        |                    |          | doesn't exist (default: True).                                                   |
        +--------------------+----------+-----------+----------------------------------------------------------------------+
        | api_key            |   No     | The SmartSheet API key (can be provided as an environment variable or directly   |
        |                    |          | set as a property). If not provided, tries to use the `SMARTSHEET_API_KEY`       |
        |                    |          | environment variable.                                                            |
        +--------------------+----------+-----------+----------------------------------------------------------------------+
        | url                |   No     | Base URL for the SmartSheet Sheets API (default:                                 |
        |                    |          | https://api.smartsheet.com/2.0/sheets/).                                         |
        +--------------------+----------+-----------+----------------------------------------------------------------------+
        | file_id            |   Yes    | The ID of the SmartSheet file to download.                                       |
        +--------------------+----------+-----------+----------------------------------------------------------------------+
        | file_format        |   No     | The desired file format for the downloaded data (default:                        |
        |                    |          | "application/vnd.ms-excel"). Supported formats are:                              |
        |                    |          | * "application/vnd.ms-excel" (Excel)                                             |
        |                    |          | * "text/csv" (CSV)                                                               |
        +--------------------+----------+-----------+----------------------------------------------------------------------+
        | filename           |   Yes    | The filename to use for the downloaded file.                                     |
        +--------------------+----------+-----------+----------------------------------------------------------------------+

        Save the downloaded files on the new destination.

    """  # noqa
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        self.file_format: str = "application/vnd.ms-excel"
        self.url: str = "https://api.smartsheet.com/2.0/sheets/"
        self._credentials: Dict = {"token": str, "scheme": str}
        DownloadFromBase.__init__(self, loop=loop, job=job, stat=stat, **kwargs)
        self.create_destination: bool = True  # by default

    async def start(self, **kwargs):
        if hasattr(self, "api_key"):
            api_key = self.get_env_value(self.api_key)
            if not api_key:
                raise ComponentError(
                    f"SmartSheet: Invalid API Key name {self.api_key}"
                )
        else:
            api_key = self.get_env_value("SMARTSHEET_API_KEY")
        self.credentials = {"token": api_key, "scheme": "Bearer"}
        self.url = f"{self.url}{self.file_id}"
        if self.file_format not in ["application/vnd.ms-excel", "text/csv"]:
            # only supported
            raise ComponentError(
                f"SmartSheet: Format {self.file_format} is not suported"
            )
        try:
            self.accept = (
                "text/csv" if self.file_format == "dataframe" else self.file_format
            )
        except Exception as err:
            print(err)
        await super(DownloadFromSmartSheet, self).start(**kwargs)
        return True

    async def close(self):
        pass

    async def http_response(self, response):
        # getting aiohttp response:
        if response.status == 200:
            try:
                async with aiofiles.open(self.filename, mode="wb") as fp:
                    await fp.write(await response.read())
                return True
            except Exception as err:
                self.exception(f"Error saving File {err!s}")
        else:
            raise ComponentError(
                f"DownloadFromSmartSheet: Wrong response from Smartsheet: {response!s}"
            )
        return response

    async def run(self):
        self._result = None
        try:
            if await self.http_session(self.url, method="get"):
                self._filenames = [str(self.filename)]
                self._result = self._filenames
                self.add_metric("SMARTSHEET_FILE", self.filename)
            return self._result
        except ComponentError as err:
            raise FileNotFound(f"DownloadFromSmartSheet Error: {err}") from err
        except Exception as err:
            raise ComponentError(
                f"DownloadFromSmartSheet: Unknown Error: {err}"
            ) from err
