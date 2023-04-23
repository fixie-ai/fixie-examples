# This is a very basic Agent that queries DataDog logs. It is meant to be an example of how
# to use an existing external API source to build an Agent, but it would need to be extended
# to cover all of the broader things that DataDog could do.

import fixieai
from datadog_api_client import ApiClient
from datadog_api_client import Configuration
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.model.logs_list_request import LogsListRequest
from datadog_api_client.v2.model.logs_list_request_page import LogsListRequestPage
from datadog_api_client.v2.model.logs_query_filter import LogsQueryFilter
from datadog_api_client.v2.model.logs_sort import LogsSort

configuration = Configuration()


BASE_PROMPT = """I'm an agent that can communicate with Datadog."""
FEW_SHOTS = """
Q: Find logs that match the query "source:gcp.cloud.run.revision stars"
Ask Func[query_logs]: source:gcp.cloud.run.revision stars
Func[query_logs] says: I found 2 log entries matching your query.
2023-04-21 11:32:04: The Chinese flag has five stars.
2023-04-21 11:32:03: How many stars are on the Chinese flag?
A: I found 2 log entries matching your query.
2023-04-21 11:32:04: The Chinese flag has five stars.
2023-04-21 11:32:03: How many stars are on the Chinese flag?

Q: Show me logs that match the term peanuts
Ask Func[query_logs]: peanuts
Func[query_logs] says: I found 3 log entries matching your query.
2023-02-14 05:44:01: This log entry contains peanuts.
2023-02-14 05:44:01: Another log entry contains peanuts.
2023-02-14 05:44:00: There are many people for whom peanuts are a food allergy.
A: I found 3 log entries matching your query.
2023-02-14 05:44:01: This log entry contains peanuts.
2023-02-14 05:44:01: Another log entry contains peanuts.
2023-02-14 05:44:00: There are many people for whom peanuts are a food allergy.
"""
agent = fixieai.CodeShotAgent(BASE_PROMPT, FEW_SHOTS)


@agent.register_func
def query_logs(query: fixieai.Message) -> str:
    print(f"Got query: {query.text}")
    result = ""
    with ApiClient(configuration) as api_client:
        body = LogsListRequest(
            filter=LogsQueryFilter(
                query=query.text,
            ),
            sort=LogsSort.TIMESTAMP_DESCENDING,
            page=LogsListRequestPage(
                limit=20,
            ),
        )
        api_instance = LogsApi(api_client)
        response = api_instance.list_logs(body=body)
        print(f"Found {len(response.data)} log entries.")
        result = f"I found {len(response.data)} log entries matching your query.\n"
        for log in response.data:
            result += process_log_entry(log)
    return result or "No results found."


def process_log_entry(log) -> str:
    publish_time = log.attributes.attributes.get("publish_time", None) or "<unknown>"
    timestamp = publish_time.strftime("%Y-%m-%d %H:%M:%S")
    message = log.attributes.message or "<no message>"
    return f"{timestamp}: {message}\n"
