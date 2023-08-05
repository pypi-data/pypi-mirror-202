import os
from pathlib import Path
from core.constants import USER_REPO_DATA_DIRNAME


def get_project_dir(repo_full_name: str) -> str:
    # Look for __project_root__.py inside repo dir to get the project dir
    local_repo_path = (Path(USER_REPO_DATA_DIRNAME) / repo_full_name).as_posix()
    files = [str(p) for p in list(Path(local_repo_path).glob("**/__project_root__.py"))]
    if len(files) > 0:
        return files[0].replace("/__project_root__.py", "")
    else:
        return ""
