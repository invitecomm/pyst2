import pytest

from asterisk.config import Line, Category, Item, Config, ParseError

########### test Category Class ##############

#test whether there are rackets [] for getting module name in line.
def test_category_get_line_isnot_rackets():
    exception_str = "Missing '[' or ']' in category definition"
    line_str = 'audiobuffers=32                 ; The number of 20ms audio buffers to be used'
    with pytest.raises(ParseError) as e:
        result = Category(line_str, 3, "")
        assert exception_str in e.value

#test whether there isn't module name in rackets [] of line.
def test_category_get_line_isnot_modulename():
    exception_str = "Must provide name or line representing a category"
    line_str = ''
    with pytest.raises(Exception, match=exception_str) as e:
        result = Category(line_str, 4, "")
        assert exception_str in e.value

#test whether there isn't comment in line of module name.
def test_category_get_line_with_empty_comment():
    line_str = '[intro]'
    assert Category(line_str, 5, "moudule").get_line() == line_str

#test whether there is comment in line of module name.
def test_category_get_line_with_comment():
    line_str = '; This configuration file is read every time you  call app meetme()'
    result = Category(line_str, 6, "module")
    assert result.get_line() == '[module]\t; This configuration file is read every time you  call app meetme()'

# test append, remove function of category class.
def test_category_append_an_item():
    line_str = '; This configuration file is read every time you  call app meetme()'
    result = Category(line_str, 7, "module")
    # test appen
    result.append('item')
    assert result.items.__contains__('item')
    # test remove
    result.remove('item')
    assert result.items.__contains__('item') is False

# test insert, pop function of category class.
def test_category_insert_an_item_at_an_index():
    line_str = '; This configuration file is read every time you call app meetme()'
    result = Category(line_str, 8, "key")
    # test insert
    result.insert(5, 'item5')
    assert result.items.__getitem__(0) == 'item5'
    # test pop
    result.pop(0)
    assert result.items.__contains__('item5') is False

######### test Line Class ##########

# test whether there is a comment on the line.
def test_get_line_is_comment():
    line = Line('; Sample ADSI Configuration file', 1)
    assert line.get_line() == '; Sample ADSI Configuration file'

# test whether there isn't a comment on the line.
def test_get_line_isnot_comment():
    line = Line('alignment = center', 2)
    assert line.get_line() == 'alignment = center'

#test is to split the string to remove spaces and join the line ff there is a comment on the line.
def test_get_line():
    line = Line('audiobuffers=32					; The number of 20ms audio buffers to be used', 3)
    assert line.get_line() == 'audiobuffers=32	; The number of 20ms audio buffers to be used'

########## test Item Class #############

# test whether there is pair(name, value) in line of item
def test_item_get_line_with_name_value():
    line_str = '; This configuration file is read every time you call app meetme()'
    result = Item(line_str, 9, "key", 'value')
    assert result.get_line() == 'key = value	; This configuration file is read every time you call app meetme()'

# test whether there is comment in line of item
def test_item_get_line_with_comment():
    line_str = 'conf => 2345,9938'
    result = Item(line_str, 10, "key", 'value')
    assert result.get_line() == 'conf => 2345,9938'

# test whether there is missing name or value in line of item
def test_item_get_line_with_exception(exception_str='Must provide name or value representing an item'):
    line_str = '; the participants be warned?'
    with pytest.raises(Exception, match=exception_str) as e:
        result = Item(line_str, 11, '', '')

# test parse by => symbol.(split by '=' and get ']')
def test_item_parse_with_parse_error():
    exception_string = "Category name missing '['"
    line_str = '[intro]'
    with pytest.raises(ParseError) as e:
        result = Item(line_str, 12, "key", 'value')
        assert exception_string in e.value

# test parse by => symbol.(split by '=' and get ']')
def test_item_parse_with_parse_error_name_value_pair():
    exception_str = "Item must be in name = value pairs"
    line_str = '[intro'
    with pytest.raises(ParseError) as e:
        result = Item(line_str, 13, '', '')
        assert exception_str in e.value

# test parse name, value
def test_item_parse_with_key_value():
    line_str = 'greeting => Asterisk'
    result = Item(line_str, 14, '', '')
    assert result.name == 'greeting'
    assert result.value == 'Asterisk'

########### test Config Class ###########
def test_config():

    config = Config("./test/conf/test.conf")
    assert config.categories[0].line == '[intro]'
    assert config.filename == './test/conf/test.conf'
    assert len(config.lines) == 8

def test_common():
    raw_lines= open('./test/conf/test.conf').readlines()
    num = 0
    catergory = None
    lines = []
    categories = []

    for line in raw_lines:
        num += 1
        line = line.strip()
        if not line or line[0] == ';':
            item = Line(line or '', num)
            lines.append(item)
            if catergory:
                catergory.comments.append(item)
            continue
        elif line[0] == '[':
            catergory = Category(line, num)
            lines.append(catergory)
            categories.append(catergory)

            continue
        else:
            item = Item(line, num)
            lines.append(item)
            if catergory:
                print(item)
                catergory.append(item)
                # catergory.insert(num,catergory)
                # catergory.pop(num)
                # catergory.remove(catergory)
            continue
