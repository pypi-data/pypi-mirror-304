from typing import Dict, Any
import os
import json
import requests
from . import _utils as ut


def fetch_permissions(project: str, registry: str, url: str, force_remote: bool = False) -> Dict[str, Any]:
    """
    Fetch permissions for a project.

    Args:
        project:
            Name of a project.

        registry:
            Path to the Gobbler registry.

        url:
            URL of the REST API. Only used for remote queries.

        force_remote:
            Whether to force a remote query via ``url``, even if the
            ``registry`` is present on the current filesystem.

    Returns:
        A dictionary containing the permissions for the ``project``.  This
        contains ``owners``, a list of strings with the user IDs of the owners
        of this project; and ``uploaders``, a list of dictionaries where each
        dictionary has the following fields:

        - ``id``, string containing a user ID that is authorized to upload.
        - ``asset`` (optional), string containing the name of the asset that
          the uploader is allowed to upload to. If not present, there is no
          restriction on the uploaded asset name.
        - ``version`` (optional), string containing the name of the version
          that the uploader is allowed to upload to. If not present, there is
          no restriction on the uploaded version name.
        - ``until`` (optional), string containing the expiry date of this
          authorization in Internet Date/Time format. If not provided, the
          authorization does not expire.
        - ``trusted`` (optional), whether the uploader is trusted. If not
          provided, defaults to false.

        The top-level dictionary may also contain `global_write`, a boolean
        indicating whether global writes are supported. If true, any user may
        create a new asset in this project, and each user can upload new
        versions to any asset they created under this mode.
    """
    if os.path.exists(registry) and not force_remote:
        with open(os.path.join(registry, project, "..permissions"), "r") as f:
            perms = json.load(f)
    else:
        res = requests.get(url + "/fetch/" + project + "/..permissions")
        if res.status_code >= 300:
            raise ut.format_error(res)
        perms = res.json()
    return perms

