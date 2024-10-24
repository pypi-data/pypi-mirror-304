import collections
import sys
sys.path = ['../src'] + sys.path
from easonsi import utils

class TestUtils(object):
    def test_freq_dict(self):
        a = collections.Counter([1,1,2,3] + list(range(10)))
        print(utils.FreqDict2List(a))
    def test_merge_files(self):
        utils.MergeFiles(".", "merged", ".*json.*")

    def test_tokenlist(self):
        token_list = utils.TokenList(
            file="tmp/token_list.csv",
            source="a b c a a b".split(),
            func=lambda x: x,
            save_low_freq=2,
            special_marks=["[SEPCIAL1]", "[SEPCIAL2]"]
        )
        print(token_list.get_id("[SEPCIAL1]"), token_list.get_id("<PAD>"))
        print(token_list.get_num())
        
    def test_chinese_cutsent(self):
        sent = """BERT-whitening在常见英文数据集上的测试，基本上已经对齐了BERT-flow的设置。
        测试半角标点. model_type: 模型大小，必须是['base', 'large', 'base-nli', 'large-nli']之一；之一。
        """
        print(f"{sent}\n\n{utils.ChineseCutSent(sent)}")

test = TestUtils()
# test.test_merge_files()
# test.test_tokenlist()
test.test_chinese_cutsent()
