import sys 
if __name__ == '__main__':
    argv = sys.argv[1:] # 移除了 python 和 monitor.py 后面再添加
    if not argv:
        print('Usage: ./monitor your-script.py')
        exit(0)
    if argv[0] != 'python':
        argv.insert(0, 'python')
    command = argv
    print( command )