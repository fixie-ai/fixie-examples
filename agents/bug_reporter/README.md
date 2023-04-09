# Bug Reporter agent

This Agent files bug reports in GitHub. To use it, need to make the following changes:

1. Create a GitHub access token. To do this, go to your settings page on GitHub, find the
`Developer settings` section, and click on `Personal access tokens`. Then, click on `Generate new token`.
Make sure you assign the token `read/write` permissions on Issues.

2. Create a `.env` file in this directory, and add the following environment variable:

```
GITHUB_ACCESS_TOKEN=<your GitHub access token>
```

3. Edit the file `main.py` and change the value of the `REPO` variable to match the name of the
repository you want to file bug reports in. For example, if you want to file bug reports in the
`apache/tvm` repository, you would set `REPO` to `apache/tvm`.

4. Edit the `LABEL` value at the top of `main.py` to match the name of the label you would like
associated with bug reports made by the agent.

5. Run `fixie deploy` to deploy the Agent to Fixie. You can start a session with the Agent and ask
it to file bug reports in your GitHub repository.