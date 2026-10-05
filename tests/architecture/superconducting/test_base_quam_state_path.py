import pytest

from quam_builder.architecture.superconducting.qpu.base_quam import BaseQuam


@pytest.fixture(autouse=True)
def _reset_state_path():
    yield
    BaseQuam.state_path = None


def test_class_state_path_overrides_env_var(tmp_path, monkeypatch):
    monkeypatch.setenv("QUAM_STATE_PATH", "/bogus")
    BaseQuam.state_path = tmp_path

    serialiser = BaseQuam.get_serialiser()

    assert serialiser.state_path == tmp_path.resolve()
    assert serialiser._get_state_path() == tmp_path.resolve()


def test_unset_state_path_keeps_env_var_resolution(tmp_path, monkeypatch):
    monkeypatch.setenv("QUAM_STATE_PATH", str(tmp_path))

    serialiser = BaseQuam.get_serialiser()

    assert serialiser.state_path is None
    assert serialiser._get_state_path() == tmp_path.resolve()


@pytest.mark.parametrize(
    "module, cls_name",
    [
        ("quam_builder.architecture.quantum_dots.qpu.base_quam_qd", "BaseQuamQD"),
        ("quam_builder.architecture.nv_center.qpu.base_quam", "BaseQuamNV"),
    ],
)
def test_other_architectures_honour_state_path(module, cls_name, tmp_path, monkeypatch):
    import importlib

    cls = getattr(importlib.import_module(module), cls_name)
    monkeypatch.setenv("QUAM_STATE_PATH", "/bogus")
    monkeypatch.setattr(cls, "state_path", tmp_path)

    assert cls.get_serialiser().state_path == tmp_path.resolve()
