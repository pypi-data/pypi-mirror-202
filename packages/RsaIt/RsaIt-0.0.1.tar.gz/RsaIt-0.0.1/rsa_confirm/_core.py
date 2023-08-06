
__all__ = ['rc']


class RsaConfirm:
    publish_key = 'abc'

    def __int__(self):
        print('构建')

    def print_key(self):
        print(RsaConfirm.publish_key)


rc = RsaConfirm()
