"""
(Docstring for exercise)
TODO: 格式化当前时间。
"""
import time
def main():
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

if __name__ == '__main__':
    main()