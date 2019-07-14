import pytest

from caches import Cache
from caches.importer import ImportFromStringError, import_from_string


def test_importer_imports_specified_class():
    cls = import_from_string("caches.core:Cache")
    assert cls is Cache


def test_importer_raises_error_is_module_path_is_missing():
    with pytest.raises(ImportFromStringError):
        import_from_string(":Cache")


def test_importer_raises_error_is_attribute_is_missing():
    with pytest.raises(ImportFromStringError):
        import_from_string("caches.core")


def test_importer_raises_error_is_module_cant_be_imported():
    with pytest.raises(ImportFromStringError):
        import_from_string("not_existing_d76a8:Cache")


def test_importer_raises_error_is_attributecant_be_imported():
    with pytest.raises(ImportFromStringError):
        import_from_string("caches.core:Undefined")
