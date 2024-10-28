from pulsar import Client, AuthenticationToken, CryptoKeyReader
from junoaccessmanager.src.settings import settings

tenant = 'test-tenant'
namespace = 'test-namespace'
topic = 'test-topic'
subscription = 'test-subscription'
mq_token = ''
abc = 'eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJhYmMifQ.GlqLtZg4wYc5_47MZ3i-FGQuSAxRjYGDkeqNMTbiivmuHq-4CAGo2C_2zbZUgo4Tu93pFj9dLTIUkrG6sKprLTvn9inxBhlTTcU0ZxpvoPHsgw5tE-_vr_ezDkzW3hfRqjj6Svpe3qXx7q7dyfuYAGYSOk_kfCGbJZFRqsFjME-xh_YwUKxu2SAtJNdTAMyWjEk1PHdEr90oFjJgTYTDUZIO81wjJn19iCUbYm2UiRDl28__IfMqajFwwbtXBQzEhgbn4agdeHubLKr6W5OAuWyQYTTM2VO7NVSu8T3i24zQEp2z_tlr3-aCR3SywsoX92OgHkTctJpwkjiZDqZHFg'


def producer(msg: str):
    # 创建 Pulsar 客户端
    client = Client(
        service_url=settings.PULSAR_HOST,
        authentication=AuthenticationToken(abc)
    )

    # key_reader = CryptoKeyReader(
    #     public_key_path='rsa_public_key.pem',
    #     private_key_path='rsa_private_key.pem'
    # )

    # 创建生产者，这会自动创建主题
    producer = client.create_producer(
        topic=f'persistent://{tenant}/{namespace}/{topic}',
        # crypto_key_reader=key_reader
    )

    print("Message sent successfully.")

    # 生产一条消息以确保创建主题
    producer.send(msg.encode('utf-8'))

    # 关闭生产者
    producer.close()
    # 关闭 Pulsar 客户端
    client.close()


if __name__ == '__main__':
    producer('test')
