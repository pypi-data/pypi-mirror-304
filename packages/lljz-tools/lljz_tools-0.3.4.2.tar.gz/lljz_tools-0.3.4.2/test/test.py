# coding=utf-8

"""
@fileName       :   test.py
@data           :   2024/9/4
@author         :   jiangmenggui@hosonsoft.com
"""
from lljz_tools.console_table import ConsoleTable

if __name__ == '__main__':
    table = ConsoleTable([{'server_name': 'intelligent-platform-product', 'status': '成功', 'message': '构建成功'},{'server_name': 'intelligent-platform-product', 'status': '成功', 'message': '构建成功'}])
    img = table.to_image()
    img.save('./test.png')
    ...
