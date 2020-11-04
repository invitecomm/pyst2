import io
from unittest import mock

import pytest
from unittest.mock import Mock
# @pytest.fixture(scope="session", autouse=True)


# @pytest.fixture(scope="session", autouse=True)
# def execute_before_any_test():
#     print("asdasd");
import asterisk
from asterisk.config import Line, Category, ParseError, Item, Config


def test_get_line_not_line():
    line = Line('; extensions.conf - the Asterisk dial plan', 2)
    result = line.get_line()
    assert result == '; extensions.conf - the Asterisk dial plan'
    print("[test_get_line] success", line.__str__())


def test_get_line_no_comment():
    line = Line('writeprotect=no', 2)
    line.__str__();
    result = line.get_line()
    assert result == 'writeprotect=no'
    print("[test_get_line_no_comment] success: ", line.__str__())


def test_get_line():
    line = Line('IAXINFO=guest					; IAXtel username/password', 2)
    result = line.get_line()
    assert result == 'IAXINFO=guest	; IAXtel username/password'
    print("[test_get_line] success", line.__str__())


def test_category_get_line_with_parse_exception():
    exception_string = "Missing \'[\' or \']\' in category definition"
    line_text = 'IAXINFO=guest					; IAXtel username/password'
    print(exception_string)
    with pytest.raises(ParseError) as ex:
        result = Category(line_text, 2, "testName")
        assert exception_string in ex.value


def test_category_get_line_without_name_line():
    exception_string = "Must provide name or line representing a category"
    line_text = ''
    print(exception_string)
    with pytest.raises(Exception, match=exception_string) as ex:
        result = Category(line_text, 2, "")


def test_category_get_line_with_empty_comment():
    line_text = '[globals]'
    result = Category(line_text, 2, "testName")
    assert result.get_line() == line_text


def test_category_get_line_with_comment():
    line_text = '; the amount of delay is set for English; you may need to adjust this time'
    result = Category(line_text, 2, "testName")
    assert result.get_line() == '[testName]	; the amount of delay is set for English; you may need to adjust this time'


def test_category_append_an_item():
    line_text = '; the amount of delay is set for English; you may need to adjust this time'
    result = Category(line_text, 2, "testName")
    result.append('someItem')
    assert result.items.__contains__('someItem')
    result.remove('someItem')
    assert result.items.__contains__('someItem') is False


def test_category_insert_an_item_at_an_index():
    line_text = '; the amount of delay is set for English; you may need to adjust this time'
    result = Category(line_text, 2, "testName")
    result.insert(2, 'someItemAtAnIndex2')
    assert result.items.__getitem__(0) == 'someItemAtAnIndex2'
    result.pop(0)
    assert result.items.__contains__('someItemAtAnIndex2') is False


def test_item_get_line_with_name_value():
    line_text = '; the amount of delay is set for English; you may need to adjust this time'
    result_item = Item(line_text, 2, "testName", 'someValue')
    assert result_item.get_line() == 'testName = someValue	; the amount of delay is set for English; you may need to ' \
                                     'adjust this time'


def test_item_get_line_with_comment():
    line_text = 'exten => _X*X!,1,Goto(outbound-freenum2,${EXTEN},1)'
    result_item = Item(line_text, 2, "testName", 'someValue')
    assert result_item.get_line() == 'exten => _X*X!,1,Goto(outbound-freenum2,${EXTEN},1)'


def test_item_get_line_with_exception(exception_string='Must provide name or value representing an item'):
    line_text = '; the amount of delay is set for English; you may need to adjust this time'
    with pytest.raises(Exception, match=exception_string) as ex:
        result_item = Item(line_text, 2, "", '')


def test_item_parse_with_parse_error():
    exception_string = "Category name missing '['"
    line_text = '[globals]'
    with pytest.raises(ParseError) as ex:
        result_item = Item(line_text, 2, "testName", 'someValue')
        assert exception_string in ex.value


def test_item_parse_with_parse_error_name_value_pair():
    exception_string = "Item must be in name = value pairs"
    line_text = '[globals'
    with pytest.raises(ParseError) as ex:
        result_item = Item(line_text, 2, "", '')
        assert exception_string in ex.value


def test_item_parse_with_name_value_pair():
    line_text = 'include => default'
    result_item = Item(line_text, 2, "", '')
    assert result_item.name == 'include'
    assert result_item.value == 'default'


# def test_config_load():
#     line_text = 'include => default'
#     result_item = Config("../resources/test.conf")
#     assert result_item.name == 'include'
#     assert result_item.value == 'default'

def test_gen():
    # fake_file = io.StringIO("some initial text data")
    # with mock.patch('os.open', return_value=fake_file, create=True):
    result_config = Config("./tests/resources/test.conf")
    assert result_config.categories[0].line == '[dummytext]'
    assert result_config.filename == './tests/resources/test.conf'
    assert len(result_config.lines) == 6
    # self.assertEqual(result, ['<foo\n>', '<bar\n>'])


# test_gen()
