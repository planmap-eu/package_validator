def pytest_addoption(parser):
    parser.addoption("--pkgpath", action="store", default="path/to/PMID")
    parser.addoption("--schema", action="store", default="planmap")
