import logging
import os
from typing import Any, Dict, List, Tuple

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


def gather_tests() -> Dict[str, List[Dict[str, Any]]]:
    """Read the agent.yaml file from each agent subdirectory and return a dictionary mapping
    from agent name to a list of tests."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    agents_dir = os.path.join(current_dir, "..", "agents")
    tests = {}
    for agent_dir in os.listdir(agents_dir):
        agent_config_file = os.path.join(agents_dir, agent_dir, "agent.yaml")
        if os.path.exists(agent_config_file):
            with open(agent_config_file, "r") as infile:
                agent_config = yaml.load(infile, Loader=yaml.Loader)
                handle = agent_config["handle"]
                if "tests" in agent_config:
                    tests[handle] = agent_config["tests"]
    return tests


def list_tests() -> List[Tuple[str, str, str]]:
    """Flatten the list of tests into a single list of (handle, query, expected) tuples."""
    all_tests = gather_tests()
    return [
        (f"fixie/{handle}", testspec["query"], testspec["expected"])
        for handle in all_tests.keys()
        for testspec in all_tests[handle]
    ]


@pytest.fixture
def agents() -> List[str]:
    return [f"fixie/{agent}" for agent in gather_tests().keys()]


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


@pytest.mark.parametrize("agent, query, expected", list_tests())
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
