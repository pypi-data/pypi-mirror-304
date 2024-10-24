import base64
import hashlib
from pathlib import Path

import py_fast_rsync
import pytest
from fastapi.testclient import TestClient
from py_fast_rsync import signature

from syftbox.client.plugins.sync.endpoints import (
    SyftNotFound,
    SyftServerError,
    apply_diff,
    get_diff,
    get_metadata,
    get_remote_state,
)
from syftbox.server.sync.models import DiffResponse
from tests.unit.server.conftest import TEST_DATASITE_NAME, TEST_FILE


def test_get_all_permissions(client: TestClient):
    # TODO: filter permissions and not return everything
    response = client.post(
        "/sync/get_metadata",
        json={"path_like": "%.syftperm"},
    )

    response.raise_for_status()
    assert len(response.json())


def test_get_diff_2(client: TestClient):
    local_data = b"This is my local data"
    sig = signature.calculate(local_data)
    sig_b85 = base64.b85encode(sig).decode("utf-8")
    response = client.post(
        "/sync/get_diff",
        json={
            "path": f"{TEST_DATASITE_NAME}/{TEST_FILE}",
            "signature": sig_b85,
        },
    )

    response.raise_for_status()
    diff_response = DiffResponse.model_validate(response.json())
    remote_diff = diff_response.diff_bytes
    probably_remote_data = py_fast_rsync.apply(local_data, remote_diff)

    server_settings = client.app_state["server_settings"]
    file_server_contents = server_settings.read(f"{TEST_DATASITE_NAME}/{TEST_FILE}")
    assert file_server_contents == probably_remote_data


def file_digest(file_path, algorithm="sha256"):
    # because this doesnt work in python <=3.10, we implement it manually
    hash_func = hashlib.new(algorithm)

    with open(file_path, "rb") as file:
        # Read the file in chunks to handle large files efficiently
        for chunk in iter(lambda: file.read(4096), b""):
            hash_func.update(chunk)

    return hash_func.hexdigest()


def test_syft_client_push_flow(client: TestClient):
    response = client.post(
        "/sync/get_metadata",
        json={"path_like": f"%{TEST_DATASITE_NAME}/{TEST_FILE}"},
    )

    response.raise_for_status()
    server_signature_b85 = response.json()[0]["signature"]
    server_signature = base64.b85decode(server_signature_b85)
    assert server_signature

    local_data = b"This is my local data"
    delta = py_fast_rsync.diff(server_signature, local_data)
    delta_b85 = base64.b85encode(delta).decode("utf-8")
    expected_hash = hashlib.sha256(local_data).hexdigest()

    response = client.post(
        "/sync/apply_diff",
        json={
            "path": f"{TEST_DATASITE_NAME}/{TEST_FILE}",
            "diff": delta_b85,
            "expected_hash": expected_hash,
        },
    )

    response.raise_for_status()

    result = response.json()
    snapshot_folder = client.app_state["server_settings"].snapshot_folder
    sha256local = file_digest(f"{snapshot_folder}/{TEST_DATASITE_NAME}/{TEST_FILE}", "sha256")
    assert result["current_hash"] == expected_hash == sha256local


def test_get_remote_state(client: TestClient):
    metadata = get_remote_state(client, TEST_DATASITE_NAME, Path(TEST_DATASITE_NAME))

    assert len(metadata) == 2
    for m in metadata:
        assert m.path.parent == Path(TEST_DATASITE_NAME)


def test_get_remote_state_perms(client: TestClient):
    metadata = get_remote_state(client, "random@user.com", Path(TEST_DATASITE_NAME))
    assert not metadata


def test_get_metadata(client: TestClient):
    metadata = get_metadata(client, Path(TEST_DATASITE_NAME) / TEST_FILE)
    assert metadata.path == Path(TEST_DATASITE_NAME) / TEST_FILE

    # check serde works
    assert isinstance(metadata.hash_bytes, bytes)
    assert isinstance(metadata.signature_bytes, bytes)


def test_apply_diff(client: TestClient):
    local_data = b"This is my local data"

    remote_metadata = get_metadata(client, Path(TEST_DATASITE_NAME) / TEST_FILE)

    diff = py_fast_rsync.diff(remote_metadata.signature_bytes, local_data)
    expected_hash = hashlib.sha256(local_data).hexdigest()

    # Apply local_data to server
    response = apply_diff(client, Path(TEST_DATASITE_NAME) / TEST_FILE, diff, expected_hash)
    assert response.current_hash == expected_hash

    # check file was written correctly
    snapshot_file_path = client.app_state["server_settings"].snapshot_folder / Path(TEST_DATASITE_NAME) / TEST_FILE
    remote_data = snapshot_file_path.read_bytes()
    assert local_data == remote_data

    # another diff with incorrect hash
    remote_metadata = get_metadata(client, Path(TEST_DATASITE_NAME) / TEST_FILE)
    diff = py_fast_rsync.diff(remote_metadata.signature_bytes, local_data)
    wrong_hash = "wrong_hash"

    with pytest.raises(SyftServerError) as e:
        apply_diff(client, Path(TEST_DATASITE_NAME) / TEST_FILE, diff, wrong_hash)

    # TODO typed errors
    assert "expected_hash mismatch" in str(e.value)


def test_get_diff(client: TestClient):
    local_data = b"This is my local data"
    sig = signature.calculate(local_data)

    file_path = Path(TEST_DATASITE_NAME) / TEST_FILE
    response = get_diff(client, file_path, sig)
    assert response.path == file_path

    # apply and check hash
    new_data = py_fast_rsync.apply(local_data, base64.b85decode(response.diff))
    new_hash = hashlib.sha256(new_data).hexdigest()

    assert new_hash == response.hash

    # diff nonexistent file
    file_path = Path(TEST_DATASITE_NAME) / "nonexistent_file.txt"
    with pytest.raises(SyftServerError) as e:
        get_diff(client, file_path, sig)
    assert "path not found" in str(e.value)


def test_delete_file(client: TestClient):
    response = client.post(
        "/sync/delete",
        json={"path": f"{TEST_DATASITE_NAME}/{TEST_FILE}"},
    )

    response.raise_for_status()
    snapshot_folder = client.app_state["server_settings"].snapshot_folder
    path = Path(f"{snapshot_folder}/{TEST_DATASITE_NAME}/{TEST_FILE}")
    assert not path.exists()

    with pytest.raises(SyftNotFound):
        get_metadata(client, Path(TEST_DATASITE_NAME) / TEST_FILE)


def test_create_file(client: TestClient):
    snapshot_folder = client.app_state["server_settings"].snapshot_folder
    new_fname = "new.txt"
    contents = b"Some content"
    path = Path(f"{snapshot_folder}/{TEST_DATASITE_NAME}/{new_fname}")
    assert not path.exists()

    with open(path, "wb") as f:
        f.write(contents)

    with open(path, "rb") as f:
        files = {"file": (f"{TEST_DATASITE_NAME}/{new_fname}", f.read())}
        response = client.post("/sync/create", files=files)
    response.raise_for_status()
    assert path.exists()


def test_list_datasites(client: TestClient):
    response = client.post("/sync/datasites")

    response.raise_for_status()
