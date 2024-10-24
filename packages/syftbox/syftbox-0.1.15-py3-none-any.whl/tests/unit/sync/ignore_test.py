from pathlib import Path

from syftbox.client.plugins.sync.sync import DatasiteState
from syftbox.client.utils.dir_tree import create_dir_tree
from syftbox.client.utils.display import display_file_tree
from syftbox.lib.ignore import IGNORE_FILENAME, filter_ignored_paths
from syftbox.lib.lib import Client

ignore_file = """
# Exlude alice datasite
/alice@example.com

# exclude all occurrences bob@example.com
bob@example.com

# Exclude all "large" folders under any datasite
*/large/*

# Include important_file.pdf under excluded folder
!/john@example.com/large/important_file.pdf

# General excludes
*.tmp
_.syftignore
*.py[cod]
"""

paths_with_result = [
    # Should be ignored
    ("alice@example.com/file1.txt", True),
    ("john@example.com/results/bob@example.com/file1.txt", True),
    ("john@example.com/large/file1.txt", True),
    ("john@example.com/docs/file1.tmp", True),
    ("script.pyc", True),
    # Should not be ignored
    ("john@example.com/results/alice@example.com/file1.txt", False),
    ("john@example.com/large/important_file.pdf", False),
    ("john@example.com/docs/file3.pdf", False),
    ("script.py", False),
]


def test_ignore_file(datasite_1: Client):
    # without ignore file
    ignore_path = Path(datasite_1.sync_folder) / IGNORE_FILENAME
    ignore_path.unlink(missing_ok=True)

    paths, results = zip(*paths_with_result)
    paths = [Path(p) for p in paths]
    filtered_paths = filter_ignored_paths(datasite_1, paths)
    assert filtered_paths == paths

    # with ignore file
    ignore_path.write_text(ignore_file)

    expected_result = [p for p, r in zip(paths, results) if r is False]
    filtered_paths = filter_ignored_paths(datasite_1, paths)
    assert filtered_paths == expected_result


def test_ignore_datasite(datasite_1: Client, datasite_2: Client) -> None:
    datasite_2_files = {
        datasite_2.email: {
            "visible_file.txt": "content",
            "ignored_file.pyc": "content",
        }
    }
    num_files = 2
    num_visible_files = 1
    create_dir_tree(Path(datasite_1.sync_folder), datasite_2_files)
    display_file_tree(Path(datasite_1.sync_folder))

    # ds1 gets their local state of ds2
    datasite_state = DatasiteState(client=datasite_1, email=datasite_2.email)
    _, local_changes = datasite_state.get_out_of_sync_files()

    assert len(local_changes) == num_visible_files
    assert local_changes[0].path == Path(datasite_2.email) / "visible_file.txt"

    # ds1 ignores ds2
    ignore_path = Path(datasite_1.sync_folder) / IGNORE_FILENAME
    with ignore_path.open("a") as f:
        # /datasite_2/
        f.write(f"\n/{datasite_2.email}\n")

    # ds1 gets their local state of ds2
    _, local_changes = datasite_state.get_out_of_sync_files()
    assert len(local_changes) == 0

    # remove ignore file
    ignore_path.unlink()
    _, local_changes = datasite_state.get_out_of_sync_files()
    assert len(local_changes) == num_files
