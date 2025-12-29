from click.testing import CliRunner
from context_flow.main import cli
import os

def test_init():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ['init', 'test-project'])
        assert result.exit_code == 0
        assert os.path.exists('test-project')
        assert os.path.exists('test-project/skills/decomposition.md')

def test_start_fail_outside_project():
    runner = CliRunner()
    with runner.isolated_filesystem():
        # Should fail because we are not in a project
        result = runner.invoke(cli, ['start', 'Do something'])
        assert result.exit_code == 0
        assert "Error: Not a context-flow project" in result.output

def test_start_success():
    runner = CliRunner()
    with runner.isolated_filesystem():
        runner.invoke(cli, ['init', 'test-project'])
        os.chdir('test-project')
        result = runner.invoke(cli, ['start', 'Do something'])
        assert result.exit_code == 0
        assert "Created Session Prompt" in result.output
        assert os.path.exists('sessions/00_origami_decomposition.md')
