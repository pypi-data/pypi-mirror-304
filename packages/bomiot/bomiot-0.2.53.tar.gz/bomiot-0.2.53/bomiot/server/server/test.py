import sys
import site

# 获取当前Python解释器导入模块时搜索的路径列表
paths = sys.path

# 虚拟环境路径通常位于paths列表的第一个位置
# 通过site.getsitepackages()函数也可以获取到site-packages的路径
# 这里我们选用sys.path的第一个元素作为虚拟环境的路径
venv_path = paths[0] if paths else None

print(f"当前虚拟环境路径为: {venv_path}")