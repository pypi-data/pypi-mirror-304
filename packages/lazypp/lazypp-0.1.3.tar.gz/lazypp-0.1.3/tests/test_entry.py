from pathlib import Path

import pytest

from lazypp import BaseEntry, Directory, File


def test_exceptions():
    file = BaseEntry("data")

    with pytest.raises(NotImplementedError):
        file._md5_hash()

    with pytest.raises(FileNotFoundError):
        File("data/hello3.txt")

    with pytest.raises(FileNotFoundError):
        Directory("data2")

    with pytest.raises(ValueError):
        File("../lazypp/__init__.py")

    with pytest.raises(ValueError):
        File("data/hello1.txt", dest="../dest_hello.txt")


def test_hash():
    file1 = File("data/hello1.txt")
    file2 = File("data/hello2.txt")

    assert file1._md5_hash().hexdigest() != file2._md5_hash().hexdigest()

    dir1 = Directory("data/foo1")
    dir2 = Directory("data/foo2")

    assert dir1._md5_hash().hexdigest() != dir2._md5_hash().hexdigest()


def test_dest():
    file = File("data/hello1.txt")
    assert file.path == Path("data/hello1.txt")

    file = File("data/hello1.txt", dest="dest_hello.txt")
    assert file.path == Path("dest_hello.txt")

    dir = Directory("data/foo1")
    assert dir.path == Path("data/foo1")

    dir = Directory("data/foo1", dest="dest_foo")
    assert dir.path == Path("dest_foo")
