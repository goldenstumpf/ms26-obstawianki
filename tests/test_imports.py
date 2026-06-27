def test_package_imports() -> None:
    # Package-safe imports should work regardless of working directory
    import app  # noqa: F401
    import app.main  # noqa: F401
    import app.worker.worker  # noqa: F401
