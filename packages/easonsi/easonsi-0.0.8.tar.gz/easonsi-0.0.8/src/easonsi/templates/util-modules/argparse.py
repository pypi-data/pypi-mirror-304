import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--dataname", type=str, choices=['semeval', 'meituan'], default='semeval',
                    help="semeval, meituan")
parser.add_argument("--train", default=None, action='store_true',
                    help="train or just get output")
args = parser.parse_args()

print(args.dataname, args.train)

# =========================== 手写 
class Params():
    def __init__(self):
        self.maxlen = 256
        self.bs = 8
        self.lr = 2e-5
        self.patience = 20
        self.epochs = 100
        self.saved_name = f"data0406_lr={self.lr}_bs={self.batch_size}.weights"
    
    def __str__(self) -> str:
        p = {k: v for k, v in self.__dict__.items() if not k.startswith("__")}
        return str(p)