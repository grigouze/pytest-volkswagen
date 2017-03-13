import pytest


@pytest.fixture
def volkswagen_testdir(testdir):
    testdir.tmpdir.join('test_volkswagen.py').write('''
import pytest

@pytest.mark.volkswagen
def test_success_with_volkswagen():
    assert 1

@pytest.mark.volkswagen
def test_fail_with_volkswagen():
    assert 0


def test_success_without_volkswagen():
    assert 1


def test_fail_without_volkswagen():
    assert 0
''')

    return testdir


def test_verbose_mode_no_volkswagen(volkswagen_testdir):
    result = volkswagen_testdir.runpytest('-v', '--strict')

    result.stdout.fnmatch_lines(['*test_success_with_volkswagen PASSED*'])
    result.stdout.fnmatch_lines(['*test_fail_with_volkswagen FAILED*'])
    result.stdout.fnmatch_lines(['*test_success_without_volkswagen PASSED*'])
    result.stdout.fnmatch_lines(['*test_fail_without_volkswagen FAILED*'])


def test_verbose_mode_with_volkswagen(volkswagen_testdir):
    result = volkswagen_testdir.runpytest('-v', '--volkswagen', '--strict')

    result.stdout.fnmatch_lines(['*test_success_with_volkswagen PASSED*'])
    result.stdout.fnmatch_lines(['*test_fail_with_volkswagen PASSED*'])
    result.stdout.fnmatch_lines(['*test_success_without_volkswagen PASSED*'])
    result.stdout.fnmatch_lines(['*test_fail_without_volkswagen PASSED*'])


def test_quiet_mode_no_volkswagen(volkswagen_testdir):
    result = volkswagen_testdir.runpytest('-q', '--strict')
    outcome_line = result.stdout.lines[0]

    assert outcome_line.count('.') == 2
    assert outcome_line.count('F') == 2


def test_quiet_mode_with_volkswagen(volkswagen_testdir, request):
    result = volkswagen_testdir.runpytest('-q', '--volkswagen', '--strict')
    outcome_line = result.stdout.lines[0]

    assert outcome_line.count(u'.') == 4
    assert outcome_line.count(u'F') == 0
