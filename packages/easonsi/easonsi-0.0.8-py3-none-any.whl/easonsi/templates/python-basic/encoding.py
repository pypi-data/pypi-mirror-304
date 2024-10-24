# 字符编码与 Python 中的 bytes
"""
阮一峰的 [字符编码笔记：ASCII，Unicode 和 UTF-8](http://www.ruanyifeng.com/blog/2007/10/ascii_unicode_and_utf-8.html) 介绍了这些 ANSI, ASCII, Unicode, UTF-8 这些编码的区别。
而廖雪峰的 [字符串和编码](https://www.liaoxuefeng.com/wiki/1016959663602400/1017075323632896) 一节用实例来讲更为清晰简洁：Unicode 规定了各个字符的数字，理论上可以用定长的编码方式来实现；但考虑编码成本和网络传输，变成的 UTF-8 作为 Unicode 的一种实现更为常用。在编辑器/Python 中采用定长表示更快，而存储和传输则转化为 UTF-8 格式。
"""
ord('中')       # 20013
chr(25991)      # 文

'中文test'.encode('utf-8')  # b'\xe4\xb8\xad\xe6\x96\x87test'