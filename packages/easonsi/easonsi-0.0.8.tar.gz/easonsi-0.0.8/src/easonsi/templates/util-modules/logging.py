import time

import logging

# 假设已经调用过了
logging.info("first logg")

# 在 basicConfig, 如果已经调用过 logging 了, 需要先关闭后再设置 basicConfig
logging.root.handlers = []
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.INFO,
    # filename=f'log/{time.strftime("%Y%m%d-%H:%M:%S", time.localtime())}.log',
    # 设置输出到文件和控制台
    handlers=[
        logging.FileHandler(f"log/debug.log"),
        logging.StreamHandler()
    ]
)
# logging.basicConfig(level=logging.DEBUG,
#     format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

logging.info("info here")
logging.debug("debug here")
logging.error("error here")

