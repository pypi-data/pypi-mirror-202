import logging
from src import iupy

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # Perform some tests where files don't exist.

    assert iupy.get_my_config("myconfig.test") is None, "File should not be found."

    # Run tests with correct subdirectory style.

    assert iupy.get_my_config("myconfig-subdir.test", subdir="test") is None, "File should not be found."

    # Run tests with incorrect leading directories.

    assert iupy.get_my_config("myconfig-subdir.tst2", subdir="/test") is None, "File should not be found."
    assert iupy.get_my_config("myconfig-subdir.tst3", subdir="test/") is None, "File should not be found."
    assert iupy.get_my_config("myconfig-subdir.tst3", subdir="/test/") is None, "File should not be found."

    # Perform a test where the file should exist if run from the tests subdirectory.

    test_file = "test.yaml"

    config = iupy.get_my_config(test_file)

    logging.debug(config)

    assert config is not None, "test.yaml should load from executing directory."
    assert len(config['data']) == 25, "config[data] should be exactly 25 characters."
    assert config['file'] == test_file, "Filename out should equal filename in."

    # All good if we have gotten this far!

    print("iupy/myconfig tests passed!")
