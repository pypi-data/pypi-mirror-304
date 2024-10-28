from pulsar import Client, ConsumerType, AuthenticationToken, CryptoKeyReader
from junoaccessmanager.src.settings import settings

tenant = 'test-tenant'
namespace = 'test-namespace'
topic = 'test-topic'
subscription = 'test-subscription'
mq_token = ''
abc = 'eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJhYmMifQ.GlqLtZg4wYc5_47MZ3i-FGQuSAxRjYGDkeqNMTbiivmuHq-4CAGo2C_2zbZUgo4Tu93pFj9dLTIUkrG6sKprLTvn9inxBhlTTcU0ZxpvoPHsgw5tE-_vr_ezDkzW3hfRqjj6Svpe3qXx7q7dyfuYAGYSOk_kfCGbJZFRqsFjME-xh_YwUKxu2SAtJNdTAMyWjEk1PHdEr90oFjJgTYTDUZIO81wjJn19iCUbYm2UiRDl28__IfMqajFwwbtXBQzEhgbn4agdeHubLKr6W5OAuWyQYTTM2VO7NVSu8T3i24zQEp2z_tlr3-aCR3SywsoX92OgHkTctJpwkjiZDqZHFg'



# 创建 Pulsar 客户端
client = Client(
    service_url=settings.PULSAR_HOST,
    authentication=AuthenticationToken(abc)
)

# key_reader = CryptoKeyReader(
#     public_key_path='rsa_public_key.pem',
#     private_key_path='rsa_private_key.pem'
# )

# 创建消费者
consumer = client.subscribe(
    topic=f'persistent://{tenant}/{namespace}/{topic}',
    subscription_name=subscription,
    consumer_type=ConsumerType.Shared,
    # crypto_key_reader=key_reader
)

# 接收消息
while True:
    msg = consumer.receive()
    try:
        print("Received message: '%s'" % msg.data())
        # 确认消息已被消费
        consumer.acknowledge(msg)
    except Exception as e:
        # 如果处理消息失败，可以选择不确认
        consumer.negative_acknowledge(msg)

    # if msg.value() == b'finish':
    #     break

# 关闭客户端
# client.close()
