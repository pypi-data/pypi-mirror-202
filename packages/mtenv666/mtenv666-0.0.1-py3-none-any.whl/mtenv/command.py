import click
import os

@click.command()
@click.option('--data_support')
@click.option('--user', default='')
@click.option('--password', default='')
@click.option('--token', default='')
def set_data_account(data_support, user, password, token):
    print(data_support, user, password, token)
    data_support_param = get_data_support(data_support)
    if len(data_support_param) == 1:
        os.system("SETX {0} {1} /M".format(data_support_param[0], token))
        # os.environ.setdefault(data_support_param[0], token)
    else:
        # os.environ.setdefault(data_support_param[0], user)
        # os.environ.setdefault(data_support_param[1], password)
        os.system("SETX {0} {1} /M".format(data_support_param[0], user))
        os.system("SETX {0} {1} /M".format(data_support_param[0], password))
    print('success set environ')
    print(data_support_param[0], os.getenv(data_support_param[0]))


class Data_Support():
    TUSHARE = ['MT_TS_TOKEN']
    IFIND = ['MT_IFIND_USER', 'MT_IFIND_PASSWORD']
    JOINQUANT = ['MT_JQ_USER', 'MT_JQ_PASSWORD']
    RICEQUANT = ['MT_RQ_USER', 'MT_RQ_PASSWORD']


def get_data_support(data_support):
    data_support_param = []
    if data_support in ['tushare', 'ts', 'Tushare']:
        data_support_param = Data_Support.TUSHARE
    elif data_support in ['jq', 'joinquant', 'JQ', 'JOINQUANT']:
        data_support_param = Data_Support.JOINQUANT
    elif data_support in ['ifind', 'iFind', 'IFIND']:
        data_support_param = Data_Support.IFIND
    elif data_support in ['rq', 'ricequant', 'RQ', 'RICEQUANT']:
        data_support_param = Data_Support.RICEQUANT
    else:
        print(
            'MTENV Set Error with parameter %s is None of  ...',
            data_support)
    return data_support_param


if __name__ == '__main__':
    # set_data_account('ifind', 'bftz09999999999999', '165229')
    r = os.getenv(Data_Support.IFIND[0])
    print(Data_Support.IFIND[0], r)