from typer.testing import CliRunner

from drclient.__main__ import app

runner = CliRunner()


def test_pull():
    result = runner.invoke(app, ["pull", "busybox"])
    assert (
        "Contents of registry-1.docker.io/library/busybox:latest extracted to"
        in result.stdout
    )
    assert result.exit_code == 0
