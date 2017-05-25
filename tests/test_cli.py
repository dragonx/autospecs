import pytest
import json
from click.testing import CliRunner
from autospecs import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_cli(runner):
    result = runner.invoke(cli.main)
    assert result.exit_code == 2
    assert result.exception
    assert result.output.startswith('Usage:')


def test_cli_make_model(runner):
    result = runner.invoke(cli.main, ['subaru', 'legacy'])
    assert not result.exception
    assert result.exit_code == 0
    assert result.output.strip() == '- Legacy-Sedan\n- Legacy-Station-Wagon'


def test_cli_make_model_style(runner):
    result = runner.invoke(cli.main, ['subaru', 'legacy', 'Legacy-Sedan'])
    assert result.exit_code == 0
    assert not result.exception
    assert result.output.startswith("2016 Legacy 2.5i: '379078'")


def test_cli_make_model_style_year_trim(runner):
    result = runner.invoke(cli.main, ['subaru', 'legacy', 'Legacy-Sedan', '2018', '379078'])
    assert result.exit_code == 0
    assert not result.exception
    assert json.loads(result.output)["make"] == "subaru"


def test_cli_make_model_style_year_trim_listfields(runner):
    result = runner.invoke(cli.main, ['--listfields', 'subaru', 'legacy',
                                      'Legacy-Sedan', '2018', '379078'])
    assert result.exit_code == 0
    assert not result.exception
    assert len(json.loads(result.output)) == 100
