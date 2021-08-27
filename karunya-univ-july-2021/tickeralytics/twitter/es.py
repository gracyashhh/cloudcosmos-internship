from elasticsearch import Elasticsearch, helpers

from dataclasses import dataclass
from typing import Optional

@dataclass
class ElasticConfig:
    host: object = None
    skip_certs: bool = False

class Elastic():
    def get_tweets(self, config):
        es = Elasticsearch(config.host, verify_certs=config.skip_certs)
        return es.search(index="twinttweets", body={"query": {"match_all": {}}})


if __name__ == '__main__':
    config = ElasticConfig()
    config.host = "localhost:9200"
    es = Elastic()
    tweets = es.get_tweets(config)
    print(tweets)