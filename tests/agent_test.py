import logging
from typing import Any, Dict, List

import pytest
import yaml
from fixieai import FixieClient


@pytest.fixture
def client():
    client = FixieClient()
    return client


@pytest.fixture
def session(client):
    session = client.create_session()
    return session


def read_spec() -> Dict[str, List[Dict[str, Any]]]:
    # The queries.yaml file consists of a set of docs, separated by "---". Each doc is a list
    # of queries, where each list entry is a dict with two keys -- "query" and "valid_responses".
    # Each doc is executed in its own Session to ensure that state is not carried forward
    # across the queries in a given doc.
    with open("tests/agent_tests.yaml", "r") as infile:
        test_spec = yaml.load(infile, Loader=yaml.Loader)
        #        assert type(test_spec) == dict
        assert "tests" in test_spec
        return test_spec["tests"]


@pytest.fixture
def agents() -> List[str]:
    return [test["agent"] for test in read_spec()]


def test_get_agents(client, agents):
    # A test that the agents are returned.
    all_agents = client.get_agents()
    for agent in agents:
        assert agent in all_agents


def test_session_time(session):
    # A smoke test that a basic query returns a result.
    assert session.session_id
    assert session.session_url
    response = session.query("@fixie/time What time is it?")
    assert "It is currently" in response


@pytest.mark.parametrize(
    "agent, query, expected",
    [
        [testspec["agent"], testspec["query"], testspec["expected"]]
        for testspec in read_spec()
    ],
)
def test_queries(client, agent, query, expected):
    try:
        logging.info(f"Testing agent {agent}...")
        session = client.create_session()
        sent = f'@mdw/tester Test {agent} with the query: "{query}". {expected}'
        logging.info(f"Query: {sent}")
        got = session.query(sent)
        logging.info(f"Response: {got}")
        assert (
            "test passed" in got
        ), f"The response {got!r} did not contain the required substring 'test passed'"
    finally:
        session.delete_session()
