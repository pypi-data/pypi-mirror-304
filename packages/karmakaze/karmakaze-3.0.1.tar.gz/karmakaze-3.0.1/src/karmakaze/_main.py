from types import SimpleNamespace
from typing import Union, List, Dict

__all__ = ["SanitiseAndParse"]


class SanitiseAndParse:
    """
    A class to sanitise and parse Reddit API response data, converting it into a
    SimpleNamespace format for easier attribute-based access.
    """

    def __init__(self):
        """
        Initialises SanitiseAndParse.
        """
        pass

    def _to_namespace_object(
        self, obj: Union[List[Dict], Dict]
    ) -> Union[List[SimpleNamespace], SimpleNamespace, List[Dict], Dict]:
        """
        Recursively converts dictionaries and lists of dictionaries into SimpleNamespace objects.

        :param obj: The object to convert, either a dictionary or a list of dictionaries.
        :type obj: Union[List[Dict], Dict]
        :return: A SimpleNamespace object or list of SimpleNamespace objects.
        :rtype: Union[List[SimpleNamespace], SimpleNamespace, None]
        """
        if isinstance(obj, Dict):
            return SimpleNamespace(
                **{
                    key: self._to_namespace_object(obj=value)
                    for key, value in obj.items()
                }
            )
        elif isinstance(obj, List):
            return [self._to_namespace_object(obj=item) for item in obj]
        else:
            return obj

    def comment(self, response: Dict) -> SimpleNamespace:
        """
        Converts a single comment response to a SimpleNamespace object.

        :param response: The dictionary representing the comment.
        :type response: Dict
        :return: A SimpleNamespace object for the comment.
        :rtype: SimpleNamespace
        """
        if isinstance(response, Dict):
            return self._to_namespace_object(obj=response)

    def comments(
        self, response: Union[List[Dict], Dict]
    ) -> Union[List[SimpleNamespace], SimpleNamespace]:
        """
        Converts a list of comments or a single comment to SimpleNamespace objects.

        :param response: A list of dictionaries, each representing a comment, or a single dictionary.
        :type response: Union[List[Dict], Dict]
        :return: A list of SimpleNamespace objects or a single SimpleNamespace object.
        :rtype: Union[List[SimpleNamespace], SimpleNamespace]
        """
        if isinstance(response, List) and all(
            isinstance(comment, Dict) for comment in response
        ):
            return [self.comment(response=raw_comment) for raw_comment in response]
        elif isinstance(response, Dict):
            return self._to_namespace_object(obj=response.get("data", {}))

    def post(self, response: List[Dict]) -> SimpleNamespace:
        """
        Converts a single post response to a SimpleNamespace object.

        :param response: A list containing dictionaries with post data.
        :type response: List[Dict]
        :return: A SimpleNamespace object representing the post.
        :rtype: SimpleNamespace
        """
        if isinstance(response, List) and len(response) == 2:
            children = response[0].get("data", {}).get("children")
            return self._to_namespace_object(obj=children[0])

    def posts(self, response: Dict) -> Union[List[SimpleNamespace], SimpleNamespace]:
        """
        Converts post data to SimpleNamespace objects.

        :param response: A dictionary containing post data.
        :type response: Dict
        :return: A SimpleNamespace object or list of SimpleNamespace objects representing posts.
        :rtype: Union[List[SimpleNamespace], SimpleNamespace]
        """
        data: Dict = response.get("data", {})
        if isinstance(data, Dict):
            return self._to_namespace_object(obj=data)

    def subreddit(self, response: Dict) -> SimpleNamespace:
        """
        Converts a single subreddit response to a SimpleNamespace object.

        :param response: A dictionary containing subreddit data.
        :type response: Dict
        :return: A SimpleNamespace object for the subreddit data.
        :rtype: SimpleNamespace
        """
        if "data" in response:
            return self._to_namespace_object(obj=response)

    def subreddits(
        self, response: Dict
    ) -> Union[List[SimpleNamespace], SimpleNamespace]:
        """
        Converts subreddit data to SimpleNamespace objects.

        :param response: A dictionary containing subreddit data.
        :type response: Dict
        :return: A SimpleNamespace object or list of SimpleNamespace objects for the subreddits.
        :rtype: Union[List[SimpleNamespace], SimpleNamespace]
        """
        if "data" in response:
            return self._to_namespace_object(obj=response.get("data", {}))

    def user(self, response: Dict) -> SimpleNamespace:
        """
        Converts a single user response to a SimpleNamespace object.

        :param response: A dictionary containing user data.
        :type response: Dict
        :return: A SimpleNamespace object for the user data.
        :rtype: SimpleNamespace
        """
        if "data" in response:
            return self._to_namespace_object(obj=response)

    def users(self, response: Dict) -> Union[List[SimpleNamespace], SimpleNamespace]:
        """
        Converts user data to SimpleNamespace objects.

        :param response: A dictionary containing user data.
        :type response: Dict
        :return: A SimpleNamespace object or list of SimpleNamespace objects for the users.
        :rtype: Union[List[SimpleNamespace], SimpleNamespace]
        """
        if "data" in response:
            return self._to_namespace_object(obj=response.get("data", {}))

    def wiki_page(self, response: Dict) -> SimpleNamespace:
        """
        Converts a single wiki page response to a SimpleNamespace object.

        :param response: A dictionary containing wiki page data.
        :type response: Dict
        :return: A SimpleNamespace object for the wiki page data.
        :rtype: SimpleNamespace
        """
        if "data" in response:
            return self._to_namespace_object(obj=response)


# -------------------------------- END ----------------------------------------- #
