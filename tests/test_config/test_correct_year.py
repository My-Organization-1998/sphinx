"""Test copyright year adjustment"""

import time

import pytest

from sphinx.config import Config, correct_copyright_year

LT = time.localtime()
LT_NEW = (2009, *LT[1:], LT.tm_zone, LT.tm_gmtoff)
LOCALTIME_2009 = type(LT)(LT_NEW)


@pytest.fixture(
    params=[
        # test with SOURCE_DATE_EPOCH unset: no modification
        (None, ''),
        # test with SOURCE_DATE_EPOCH set: copyright year should be updated
        ('1293840000', '2011'),
        ('1293839999', '2010'),
        ('1199145600', '2008'),
        ('1199145599', '2007'),
    ],
)
def expect_date(request, monkeypatch):
    sde, expect = request.param
    with monkeypatch.context() as m:
        m.setattr(time, 'localtime', lambda *a: LOCALTIME_2009)
        if sde:
            m.setenv('SOURCE_DATE_EPOCH', sde)
        else:
            m.delenv('SOURCE_DATE_EPOCH', raising=False)
        yield expect


def test_correct_year(expect_date):
    # test that copyright is substituted
    copyright_date = '2006-2009, Alice'
    cfg = Config({'copyright': copyright_date}, {})
    assert cfg.copyright == copyright_date
    correct_copyright_year(None, cfg)  # type: ignore[arg-type]
    if expect_date:
        assert cfg.copyright == f'2006-{expect_date}, Alice'
    else:
        assert cfg.copyright == copyright_date


def test_correct_year_space(expect_date):
    # test that copyright is substituted
    copyright_date = '2006-2009 Alice'
    cfg = Config({'copyright': copyright_date}, {})
    assert cfg.copyright == copyright_date
    correct_copyright_year(None, cfg)  # type: ignore[arg-type]
    if expect_date:
        assert cfg.copyright == f'2006-{expect_date} Alice'
    else:
        assert cfg.copyright == copyright_date


def test_correct_year_no_author(expect_date):
    # test that copyright is substituted
    copyright_date = '2006-2009'
    cfg = Config({'copyright': copyright_date}, {})
    assert cfg.copyright == copyright_date
    correct_copyright_year(None, cfg)  # type: ignore[arg-type]
    if expect_date:
        assert cfg.copyright == f'2006-{expect_date}'
    else:
        assert cfg.copyright == copyright_date


def test_correct_year_single(expect_date):
    # test that copyright is substituted
    copyright_date = '2009, Alice'
    cfg = Config({'copyright': copyright_date}, {})
    assert cfg.copyright == copyright_date
    correct_copyright_year(None, cfg)  # type: ignore[arg-type]
    if expect_date:
        assert cfg.copyright == f'{expect_date}, Alice'
    else:
        assert cfg.copyright == copyright_date


def test_correct_year_single_space(expect_date):
    # test that copyright is substituted
    copyright_date = '2009 Alice'
    cfg = Config({'copyright': copyright_date}, {})
    assert cfg.copyright == copyright_date
    correct_copyright_year(None, cfg)  # type: ignore[arg-type]
    if expect_date:
        assert cfg.copyright == f'{expect_date} Alice'
    else:
        assert cfg.copyright == copyright_date


def test_correct_year_single_no_author(expect_date):
    # test that copyright is substituted
    copyright_date = '2009'
    cfg = Config({'copyright': copyright_date}, {})
    assert cfg.copyright == copyright_date
    correct_copyright_year(None, cfg)  # type: ignore[arg-type]
    if expect_date:
        assert cfg.copyright == f'{expect_date}'
    else:
        assert cfg.copyright == copyright_date


def test_correct_year_multi_line(expect_date):
    # test that copyright is substituted
    copyright_dates = (
        '2006',
        '2006-2009, Alice',
        '2010-2013, Bob',
        '2014-2017, Charlie',
        '2018-2021, David',
        '2022-2025, Eve',
    )
    cfg = Config({'copyright': copyright_dates}, {})
    assert cfg.copyright == copyright_dates
    correct_copyright_year(None, cfg)  # type: ignore[arg-type]
    if expect_date:
        assert cfg.copyright == (
            f'{expect_date}',
            f'2006-{expect_date}, Alice',
            f'2010-{expect_date}, Bob',
            f'2014-{expect_date}, Charlie',
            f'2018-{expect_date}, David',
            f'2022-{expect_date}, Eve',
        )
    else:
        assert cfg.copyright == copyright_dates


def test_correct_year_multi_line_all_formats(expect_date):
    # test that copyright is substituted
    copyright_dates = (
        '2009',
        '2009 Alice',
        '2009, Bob',
        '2006-2009',
        '2006-2009 Charlie',
        '2006-2009, David',
    )
    cfg = Config({'copyright': copyright_dates}, {})
    assert cfg.copyright == copyright_dates
    correct_copyright_year(None, cfg)  # type: ignore[arg-type]
    if expect_date:
        assert cfg.copyright == (
            f'{expect_date}',
            f'{expect_date} Alice',
            f'{expect_date}, Bob',
            f'2006-{expect_date}',
            f'2006-{expect_date} Charlie',
            f'2006-{expect_date}, David',
        )
    else:
        assert cfg.copyright == copyright_dates


def test_correct_year_app(expect_date, tmp_path, make_app):
    # integration test
    copyright_date = '2006-2009, Alice'
    (tmp_path / 'conf.py').touch()
    app = make_app(
        'dummy',
        srcdir=tmp_path,
        confoverrides={'copyright': copyright_date},
    )
    if expect_date:
        assert app.config.copyright == f'2006-{expect_date}, Alice'
    else:
        assert app.config.copyright == copyright_date
