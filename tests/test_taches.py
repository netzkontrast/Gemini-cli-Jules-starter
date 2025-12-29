from click.testing import CliRunner
from taches.cli import cli
import os

def test_consider_pareto():
    runner = CliRunner()
    result = runner.invoke(cli, ['consider', 'pareto', 'testing context'])
    assert result.exit_code == 0
    assert "Apply Pareto's principle to testing context" in result.output

def test_blueprint_workflow():
    runner = CliRunner()
    with runner.isolated_filesystem():
        # 1. Plan
        result = runner.invoke(cli, ['blueprint', 'plan', 'Test Goal'])
        assert result.exit_code == 0
        assert os.path.exists('PLAN.md')
        assert "Test Goal" in open('PLAN.md').read()

        # 2. Define
        result = runner.invoke(cli, ['blueprint', 'define'])
        assert result.exit_code == 0
        assert os.path.exists('TODO.md')

        # 3. Implement
        result = runner.invoke(cli, ['blueprint', 'implement', 'Task 1'])
        assert result.exit_code == 0
        assert os.path.exists('ACT.md')
        assert "Task 1" in open('ACT.md').read()

        # 4. Test
        result = runner.invoke(cli, ['blueprint', 'test'])
        assert result.exit_code == 0
        assert "✅ ACT.md found" in result.output
