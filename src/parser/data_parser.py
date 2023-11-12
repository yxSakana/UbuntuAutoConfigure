from typing import List
import platform

from data.data import RunScript
from ui.pwd_entry import PasswordEntry
from ui.checkbutton import CheckbuttonWidget
from ui.select_path_widget import SelectPathWidget


def get_github_repositories() -> List[str]:
    return [val for (option_name, val) in RunScript[platform.machine()].items() if "https://github.com" in val]


def add_package_path(need_file_path_widgets: List[SelectPathWidget]) -> None:
    """为所有需要包路径的库添加给出路径

    :param need_file_path_widgets:
    :return:
    """
    for widget in need_file_path_widgets:
        local_package_path = widget.label.cget("text")
        if not local_package_path == "None":
            RunScript[platform.machine()][widget.name] += " " + local_package_path


if __name__ == "__main__":
    print(get_github_repositories())
