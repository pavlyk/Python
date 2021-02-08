class Ex(Exception):
    def __init__():
        print('ex----')


try:
    1/0
except Exception as e:
    print('dsada_{}'.format(e))