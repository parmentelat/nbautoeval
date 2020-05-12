from nbautoeval.storage import _storage_path, storage_save, storage_read, storage_clear

def cleanup_storage():
    storage = _storage_path()
    storage.exists() and storage.unlink()


def test_storage1():
    cleanup_storage()
    
    assert storage_read("foobar", "att", 0) == 0
    storage_save("foobar", "att", 1)
    assert storage_read("foobar", "att", 0) == 1
    assert storage_read("foobar", "att", 3) == 1


def test_storage2():
    storage_clear('foobar')
    
    assert storage_read("foobar", "att", 0) == 0
    storage_save("foobar", "att", 1)
    storage_save("foobar", "attempts", 2)
    assert storage_read("foobar", "att", None) == 1
    assert storage_read("foobar", "attempts", None) == 2
