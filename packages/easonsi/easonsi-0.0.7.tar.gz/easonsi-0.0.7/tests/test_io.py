import sys
sys.path = ['../src'] + sys.path

from easonsi import utils

# import bert4keras

class TestIO:
    def __init__(self) -> None:
        pass
    
    def test_list(self):
        """ SaveList: 元素为 str """
        a = "af"
        l = [a, "sdf", "sdff", "sdfa"]
        utils.SaveList(l, "tmp/test.txt")
        l_load = utils.LoadList("tmp/test.txt")
        assert l == l_load, "list not equal"
        
    def test_jsonl(self):
        """ 注意 tuple 将转为 list"""
        a = "af"
        l = [
            1, [1,2], a, {a: "tmp/test"}, (1,2),
        ]
        # l = ["sdf", "sdff", "sdfa"]
        utils.SaveJsonl(l, "tmp/test.jsonl")
        l_load = utils.LoadJsonl("tmp/test.jsonl")
        assert l[:-1] == l_load[:-1], "list not equal"
        
    def test_dict(self):
        """注意 key, value 都会转为 str  """
        a = "key_a"
        d = {
            a: "value_a",
            12: "value_12",
        }
        utils.SaveDict(d, "tmp/test.dict")
        d_load = utils.LoadDict("tmp/test.dict")
        assert d[a] == d_load[a], "dict not equal"

    def test_csv(self):
        """ 二维数组 """
        ll = [list(range(10)), list(range(10, -10, -1))]
        utils.SaveCSV(ll, "tmp/test.csv")
        ll_load = utils.LoadCSV("tmp/test.csv")
        assert ll == [[eval(i) for i in l] for l in ll_load], "csv not equal"
        
    def test_json(self):
        a = "key_a"
        j = {
            a: "value_a",
            "lr": "0.1",
        }
        utils.SaveJson(j, "tmp/test.json", indent=2)
        j_load = utils.LoadJson("tmp/test.json")
        assert j==j_load, "json not equal"

test = TestIO()
test.test_list()
test.test_json()
test.test_dict()
test.test_csv()
test.test_jsonl()