import pytest
from click.testing import CliRunner
from gitignore_cli.cli import cli

@pytest.fixture
def runner():
    """Fixture to create a CliRunner for testing the CLI."""
    return CliRunner()

def test_generate_command_with_single_template(runner, tmpdir):
    """Test the 'generate' command with a single template."""
    output_file = tmpdir.join('.gitignore')
    result = runner.invoke(cli, ['generate', 'Python', '--output', str(output_file), '--no-header'])

    # Assert that the command was successful
    assert result.exit_code == 0
    assert 'successfully generated' in result.output

    # Check if the file was created
    assert output_file.exists()

    # Check the content of the file
    with open(str(output_file), 'r') as f:
        content = f.read()
    assert 'Python' in content

def test_generate_command_with_multiple_templates(runner, tmpdir):
    """Test the 'generate' command with multiple templates."""
    output_file = tmpdir.join('.gitignore')
    result = runner.invoke
