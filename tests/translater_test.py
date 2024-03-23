from crowdin_helper.crowdin import Translater, ParseError
import pytest

def test_list_parse():
    input1 = """
1. text1
2. text2
3. text3
"""

    input2 = """
1. ```text1```
2. ```text2```
3. ```text3```
"""
    answer = [
        "text1",
        "text2",
        "text3",
    ]

    assert Translater.list_parse(input1.strip()) == answer
    assert Translater.list_parse(input2.strip()) == answer
    with pytest.raises(ParseError):
        Translater.list_parse("xxx")

def test_json_parse():
    input1 = """[
  {
    "translation": "text1"
  },
  {
    "translation": "text2"
  },
  {
    "translation": "text3"
  }
]
"""

    input2 = """[
  {
    "translation": "```text1```"
  },
  {
    "translation": "```text2```"
  },
  {
    "translation": "```text3```"
  }
]
"""
    answer = [
        "text1",
        "text2",
        "text3",
    ]

    assert Translater.json_parse(input1.strip()) == answer
    assert Translater.json_parse(input2.strip()) == answer
    with pytest.raises(ParseError):
        Translater.json_parse("xxx")

    text3 = """
{
"translation": "text"
}
"""
    assert Translater.json_parse(text3.strip()) == ["text"]
