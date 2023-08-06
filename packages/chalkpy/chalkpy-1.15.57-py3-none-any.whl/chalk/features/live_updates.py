from typing import Any, Type

import cloudpickle

from chalk.utils import notebook

NO_CLIENT_HELPTEXT = """A Chalk client has not yet been initialized in this notebook.
This means that you can create resolvers and features and test them locally, but
they will not be synced to Chalk's servers. To create a client, run the following
in your notebook:

>>> from chalk.client import ChalkClient
>>> client = ChalkClient(branch="my_branch_name")

This will create a Chalk connection pointed at the branch of your choice. New resolvers
or features that you create will be automatically uploaded to that branch. To create a
new branch, use the Chalk CLI:

$ chalk apply --branch my_branch_name
"""

NO_BRANCH_HELPTEXT = """The Chalk client on this notebook does not have a branch set.
Modifications to resolvers or features cannot be uploaded to Chalk until a branch is
specified. You can create a new branch via the Chalk CLI by running:

$ chalk apply --branch my_branch_name

Then, in Python you can point a Chalk client at an existing branch with the following code:

>>> from chalk.client import ChalkClient
>>> client = ChalkClient(branch="my_branch_name")
"""


def deploy_update(obj: Any):
    """
    If this code is being run in a Jupyter notebook, cloudpickle this
    object's dependencies and send it to the API server.
    """
    if notebook.is_defined_in_module(obj):
        # If resolver is defined in a module that's imported by a notebook, don't deploy it.
        # This is to avoid re-deploying every feature if customer imports their existing codebase into a notebook.
        return
    pickled_obj = cloudpickle.dumps(obj)
    from chalk.client.client_impl import ChalkAPIClientImpl

    client = ChalkAPIClientImpl._latest_client
    if client is None:
        raise RuntimeError(NO_CLIENT_HELPTEXT)
    if client._config.branch is None:
        raise RuntimeError(NO_BRANCH_HELPTEXT)

    resp = client._send_updated_resolver(environment=None, pickled_resolver=pickled_obj)
    print(f"Deployed '{obj.__name__}' to branch '{client._config.branch}'")


def register_live_updates_if_in_notebook(cls: Type):
    if notebook.is_notebook():
        setattr(cls, "hook", deploy_update)
