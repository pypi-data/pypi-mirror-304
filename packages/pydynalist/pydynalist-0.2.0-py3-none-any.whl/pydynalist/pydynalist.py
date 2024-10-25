import asyncio
import logging
from typing import Any, Callable, Coroutine, Dict, List, Optional, Union

import requests

logger = logging.getLogger(__name__)

try:
    import aiohttp
except ImportError:
    logger.debug("No async support, 'aiohttp' not installed.")


class Dynalist:
    HOST_API = "https://dynalist.io/api/v1"

    def __init__(self, token: str):
        self.token = token

    @staticmethod
    def _request(url: str, json: Dict, callback: Callable) -> Union[Any, Coroutine[None, None, Any]]:
        """
        Perform either a synchronous or asynchronous HTTP request depending on the event loop's state.
        """

        async def _async_request() -> Any:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(url, json=json) as resp:
                        data = await resp.json()
                        return callback(data)
            except Exception as e:
                logger.error(f"Async request failed: {e}")
                return callback(None)

        def _sync_request() -> Any:
            try:
                resp = requests.post(url, json=json)
                data = resp.json()
                return callback(data)
            except Exception as e:
                logger.error(f"Sync request failed: {e}")
                return callback(None)

        try:
            loop = asyncio.get_running_loop()
            if loop.is_running():
                return _async_request()
        except RuntimeError:
            pass

        return _sync_request()

    @classmethod
    def validate_token(cls, token: Optional[str]) -> Union[bool, Coroutine[None, None, bool]]:
        """
        Validate the provided API token. Returns True if the token is valid, otherwise False.
        """

        def callback(data: Optional[Dict] = None) -> bool:
            return data is not None and data.get("_code") == "Ok"

        url = f"{cls.HOST_API}/file/list"
        json = {"token": token}
        return cls._request(url, json, callback)

    @property
    def docs(self) -> Union[List[Dict], Coroutine[None, None, List[Dict]]]:
        """
        Retrieve all documents accessible with the API token.
        """

        def callback(data: Optional[Dict] = None) -> List[Dict]:
            if data and data.get("_code") == "Ok":
                return [item for item in data["files"] if item["type"] == "document"]
            logger.error(f"Failed to retrieve docs: {data}")
            return []

        url = f"{self.HOST_API}/file/list"
        json = {"token": self.token}
        return self._request(url, json, callback)

    @property
    def folders(self) -> Union[List[Dict], Coroutine[None, None, List[Dict]]]:
        """
        Retrieve all folders accessible with the API token.
        """

        def callback(data: Optional[Dict] = None) -> List[Dict]:
            if data and data.get("_code") == "Ok":
                return [item for item in data["files"] if item["type"] == "folder"]
            logger.error(f"Failed to retrieve folders: {data}")
            return []

        url = f"{self.HOST_API}/file/list"
        json = {"token": self.token}
        return self._request(url, json, callback)

    def get_doc(self, doc_id: str) -> Union[Dict, Coroutine[None, None, Dict]]:
        """
        Retrieve the content of a specific document by its ID.
        """

        def callback(data: Optional[Dict] = None) -> Dict:
            if data and data.get("_code") == "Ok":
                return {node["id"]: node for node in data["nodes"]}
            logger.error(f"Failed to retrieve doc {doc_id}: {data}")
            return {}

        url = f"{self.HOST_API}/doc/read"
        json = {"token": self.token, "file_id": doc_id}
        return self._request(url, json, callback)

    def get_doc_id(self, name: str) -> Optional[str]:
        """
        Get the ID of a document by its name.
        """
        titles, ids = self.get_docs_titles_and_ids()
        for title, doc_id in zip(titles, ids):
            if title == name:
                return doc_id
        return None

    def get_doc_title(self, doc_id: str) -> Optional[str]:
        """
        Get the title of a document by its ID.
        """
        titles, ids = self.get_docs_titles_and_ids()
        for title, id in zip(titles, ids):
            if id == doc_id:
                return title
        return None

    def get_docs_titles_and_ids(self) -> List[List[str]]:
        """
        Retrieve the titles and IDs of all documents.
        """
        docs = self.docs
        titles = [doc.get("title", "") for doc in docs]
        ids = [doc.get("id", "") for doc in docs]
        return titles, ids

    def send_to_inbox(self, content: str = "", note: str = "") -> Union[bool, Coroutine[None, None, bool]]:
        """
        Send a message to the user's inbox.
        """

        def callback(data: Optional[Dict] = None) -> bool:
            return data is not None and data.get("_code") == "Ok"

        url = f"{self.HOST_API}/inbox/add"
        json = {"token": self.token, "index": None, "content": content, "note": note}
        return self._request(url, json, callback)

    def edit_doc(self, file_id: str, changes: List[Dict]) -> Union[Dict, Coroutine[None, None, Dict]]:
        """
        Apply changes to a specific document.
        """

        def callback(data: Optional[Dict] = None) -> Dict:
            return data or {}

        url = f"{self.HOST_API}/doc/edit"
        json = {"token": self.token, "file_id": file_id, "changes": changes}
        return self._request(url, json, callback)

    @staticmethod
    def prepare_changes(action: str, changes: List[Dict] = [], **kwargs) -> List[Dict]:
        """
        Prepare a list of changes to apply to a document.
        content:
        note:
        node_id:
        parent_id:
        index:
        checkbox:
        checked:
        heading:
        color:
        """
        change = {"action": action}
        change.update({k: v for k, v in kwargs.items() if v is not None})
        changes.append(change)
        return changes

    @staticmethod
    def recursively_analyze_doc(doc: Dict, func: Callable, *args, **kwargs):
        """
        Recursively analyze a document and apply a function to its nodes.
        """
        children = doc.get("root", {}).get("children", ["root"])
        for child_id in children:
            Dynalist._recursively_analyze_node(doc, child_id, 0, func, *args, **kwargs)

    @staticmethod
    def _recursively_analyze_node(doc: Dict, node_id: str, tab: int, func: Callable, *args, **kwargs):
        """
        Helper method for recursive document analysis.
        """
        node = doc.get(node_id)
        if not node:
            return

        func(doc=doc, id=node_id, nest=node, tab=tab, *args, **kwargs)
        for child_id in node.get("children", []):
            Dynalist._recursively_analyze_node(doc, child_id, tab + 1, func, *args, **kwargs)

    @staticmethod
    def parse_node_to_dict(nest: Dict, **kwargs):
        """
        Parse a node into a dictionary.
        """
        dictionary = kwargs.get("dictionary")
        if dictionary is None:
            raise ValueError("Missing 'dictionary' in kwargs.")

        node_data = {
            "content": nest.get("content"),
            "note": nest.get("note"),
            "tab": kwargs.get("tab"),
            "checkbox": nest.get("checkbox"),
            "checked": nest.get("checked"),
            "heading": nest.get("heading"),
            "color": nest.get("color"),
        }
        dictionary[nest.get("id")] = node_data
