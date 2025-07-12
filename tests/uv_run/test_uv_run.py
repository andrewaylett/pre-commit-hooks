"""Unit tests for the uv-run hook."""

from unittest.mock import MagicMock, patch

from andrewaylett_pre_commit_hooks.uv_run import main, run_uv_command


def test_run_uv_command_no_args():
    """Test that run_uv_command returns False when no args are provided."""
    result = run_uv_command([])
    assert result is False


@patch("andrewaylett_pre_commit_hooks.uv_run.subprocess.run")
def test_run_uv_command_success(mock_run):
    """Test that run_uv_command returns True when the command succeeds."""
    # Mock the subprocess.run to return a successful result
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = "Command output"
    mock_result.stderr = ""
    mock_run.return_value = mock_result

    result = run_uv_command(["python", "-c", "print('Hello')"])

    # Check that the command was called with the correct arguments
    mock_run.assert_called_once_with(
        ["uv", "run", "python", "-c", "print('Hello')"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result is True


@patch("andrewaylett_pre_commit_hooks.uv_run.subprocess.run")
def test_run_uv_command_failure(mock_run):
    """Test that run_uv_command returns False when the command fails."""
    # Mock the subprocess.run to return a failed result
    mock_result = MagicMock()
    mock_result.returncode = 1
    mock_result.stdout = ""
    mock_result.stderr = "Error message"
    mock_run.return_value = mock_result

    result = run_uv_command(["python", "-c", "import sys; sys.exit(1)"])

    # Check that the command was called with the correct arguments
    mock_run.assert_called_once_with(
        ["uv", "run", "python", "-c", "import sys; sys.exit(1)"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result is False


@patch("andrewaylett_pre_commit_hooks.uv_run.subprocess.run")
def test_run_uv_command_exception(mock_run):
    """Test that run_uv_command returns False when an exception occurs."""
    # Mock the subprocess.run to raise an exception
    mock_run.side_effect = Exception("Command failed")

    result = run_uv_command(["python", "-c", "print('Hello')"])

    assert result is False


@patch("andrewaylett_pre_commit_hooks.uv_run.os.execvp")
def test_run_uv_command_with_exec_success(mock_execvp):
    """Test that run_uv_command with use_exec=True calls os.execvp."""
    result = run_uv_command(["python", "-c", "print('Hello')"], use_exec=True)

    # Check that os.execvp was called with the correct arguments
    mock_execvp.assert_called_once_with(
        "uv", ["uv", "run", "python", "-c", "print('Hello')"]
    )

    # Since os.execvp is mocked, the function should return True
    assert result is True


@patch("andrewaylett_pre_commit_hooks.uv_run.os.execvp")
def test_run_uv_command_with_exec_exception(mock_execvp):
    """Test that run_uv_command with use_exec=True returns False when an exception occurs."""
    # Mock os.execvp to raise an exception
    mock_execvp.side_effect = Exception("Command failed")

    result = run_uv_command(["python", "-c", "print('Hello')"], use_exec=True)

    assert result is False


@patch("andrewaylett_pre_commit_hooks.uv_run.run_uv_command")
@patch(
    "andrewaylett_pre_commit_hooks.uv_run.sys.argv",
    ["pre-commit-uv-run", "python", "-c", "print('Hello')"],
)
@patch("andrewaylett_pre_commit_hooks.uv_run.sys.exit")
def test_main_success(mock_exit, mock_run_uv_command):
    """Test that main does not exit when the command succeeds."""
    mock_run_uv_command.return_value = True

    main()

    mock_run_uv_command.assert_called_once_with(
        ["python", "-c", "print('Hello')"], use_exec=True
    )
    mock_exit.assert_not_called()


@patch("andrewaylett_pre_commit_hooks.uv_run.run_uv_command")
@patch(
    "andrewaylett_pre_commit_hooks.uv_run.sys.argv",
    ["pre-commit-uv-run", "python", "-c", "import sys; sys.exit(1)"],
)
@patch("andrewaylett_pre_commit_hooks.uv_run.sys.exit")
def test_main_failure(mock_exit, mock_run_uv_command):
    """Test that main exits with code 1 when the command fails."""
    mock_run_uv_command.return_value = False

    main()

    mock_run_uv_command.assert_called_once_with(
        ["python", "-c", "import sys; sys.exit(1)"], use_exec=True
    )
    mock_exit.assert_called_once_with(1)
