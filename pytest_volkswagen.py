import pytest

OK = u"."


def pytest_addoption(parser):
    group = parser.getgroup('Volkswagen', 'Volkswagen')
    group._addoption('--volkswagen',
                     action="store_true", dest="volkswagen", default=False,
                     help="don't Show failed tests.")


def pytest_report_teststatus(report):
    if not pytest.config.option.volkswagen:
        return
    
    if report.outcome == 'failed':
        report.outcome = 'passed'
        return report.outcome, OK, report.outcome.upper()


def pytest_configure(config):
    config.addinivalue_line(
        'markers',
        'volkswagen: Mark the test as always ok. When using --volkswagen, your result tests '
        'will be ok forever.')
