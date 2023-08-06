import os
import socket  # 获取主机名 
from mtenv.command import set_data_account,Data_Support

__author__ = 'ziyu'
__version__ = '0.0.1'

tushare_token=os.getenv(Data_Support.TUSHARE[0], 'test') #你的tusharepro token

ifind_user =os.getenv(Data_Support.IFIND[0], 'test')
ifind_password = os.getenv(Data_Support.IFIND[1], 'test')

jq_username=os.getenv(Data_Support.JOINQUANT[0], 'test')
jq_password=os.getenv(Data_Support.JOINQUANT[1], 'test')


def mginfo():
    mongo_ip = os.getenv('MONGODB_IP', '127.0.0.1')
    mongo_port =  os.getenv('MONGODB_PORT', 27017)
    mongo_username =  os.getenv('MONGODB_USER', 'None')
    mongo_password =  os.getenv('MONGODB_PASSWORD', 'None')
    if mongo_username=='None':
        mongo_uri = 'mongodb://{}:{}'.format(mongo_ip, mongo_port)
    else:
        mongo_uri = 'mongodb://{}:{}@{}:{}'.format( mongo_username,
                                                   mongo_password,
                                                   mongo_ip, 
                                                   mongo_port)
    return mongo_ip,mongo_port,mongo_username,mongo_password,mongo_uri
mongo_ip,mongo_port,mongo_username,mongo_password,mongo_uri=mginfo()




# eventmq_ip = os.getenv('QAPUBSUB_IP', '127.0.0.1')
# eventmq_port = os.getenv('QAPUBSUB_PORT', 5672)
# eventmq_username = os.getenv('QAPUBSUB_USER', 'admin')
# eventmq_password = os.getenv('QAPUBSUB_PWD', 'admin')
# eventmq_amqp = 'pyamqp://{}:{}@{}:{}//'.format(
#     eventmq_username, eventmq_password, eventmq_ip, eventmq_port)



# clickhouse_ip =  os.getenv('CLICKHOUSE_IP', '127.0.0.1')
# clickhouse_port =  os.getenv('CLICKHOUSE_PORT', 9001)
# clickhouse_user =  os.getenv('CLICKHOUSE_USER', 'admin')
# clickhouse_password =  os.getenv('CLICKHOUSE_PASSWORD', 'admin')

# redis_ip = os.getenv('REDIS_IP', '127.0.0.1')