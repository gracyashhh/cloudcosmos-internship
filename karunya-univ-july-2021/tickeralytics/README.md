# Requirements
* Python 3.9
* Virtual environment

# Dev environment

## Mac instructions

### conda

```
conda create -p conda-venv python
conda activate conda-venv
conda install --file requirements.txt

# conda does not have twint
pip install twint
# need the latest twint
pip install --upgrade "git+https://github.com/twintproject/twint.git@origin/master#egg=twint"
```

## Windows instructions

# Running project

## Gather tweets
```
cd twitter
python tweets_gather.py
cd ..
```

## Run stramlit app
```
streamlit run streamlit_app.py
```

## Twint ElasticSearch

### Download and create index in ElasticSearch

```
# Delete index
curl -X DELETE "localhost:9200/twinttweets"

# Create index
curl -X PUT "localhost:9200/twinttweets"

# Get mappings
curl -X GET "localhsot:9200/twinttweets?pretty"

# Add mappings
curl -X PUT "localhost:9200/twinttweets/_mappings?pretty" -H 'Content-Type: application/json' -d'
{
  "properties" : {
        "cashtags" : {
          "type" : "keyword"
        },
        "conversation_id" : {
          "type" : "long"
        },
        "created_at" : {
          "type" : "text"
        },
        "date" : {
          "type" : "date",
          "format" : "yyyy-MM-dd HH:mm:ss"
        },
        "day" : {
          "type" : "integer"
        },
        "essid" : {
          "type" : "keyword"
        },
        "geo_near" : {
          "type" : "geo_point"
        },
        "geo_tweet" : {
          "type" : "geo_point"
        },
        "hashtags" : {
          "type" : "keyword"
        },
        "hour" : {
          "type" : "integer"
        },
        "id" : {
          "type" : "long"
        },
        "lang" : {
          "type" : "keyword"
        },
        "language" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "link" : {
          "type" : "text"
        },
        "location" : {
          "type" : "keyword"
        },
        "mentions" : {
          "type" : "nested",
          "properties" : {
            "id" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword",
                  "ignore_above" : 256
                }
              }
            },
            "name" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword",
                  "ignore_above" : 256
                }
              }
            },
            "screen_name" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword",
                  "ignore_above" : 256
                }
              }
            }
          }
        },
        "name" : {
          "type" : "text"
        },
        "near" : {
          "type" : "text"
        },
        "nlikes" : {
          "type" : "integer"
        },
        "nreplies" : {
          "type" : "integer"
        },
        "nretweets" : {
          "type" : "integer"
        },
        "photos" : {
          "type" : "text"
        },
        "place" : {
          "type" : "keyword"
        },
        "profile_image_url" : {
          "type" : "text"
        },
        "quote_url" : {
          "type" : "text"
        },
        "reply_to" : {
          "type" : "nested",
          "properties" : {
            "id" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword",
                  "ignore_above" : 256
                }
              }
            },
            "name" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword",
                  "ignore_above" : 256
                }
              }
            },
            "screen_name" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword",
                  "ignore_above" : 256
                }
              }
            },
            "user_id" : {
              "type" : "keyword"
            },
            "username" : {
              "type" : "keyword"
            }
          }
        },
        "retweet" : {
          "type" : "text"
        },
        "retweet_date" : {
          "type" : "date",
          "format" : "yyyy-MM-dd HH:mm:ss",
          "ignore_malformed" : true
        },
        "retweet_id" : {
          "type" : "keyword"
        },
        "search" : {
          "type" : "text"
        },
        "source" : {
          "type" : "keyword"
        },
        "thumbnail" : {
          "type" : "text"
        },
        "timezone" : {
          "type" : "keyword"
        },
        "trans_dest" : {
          "type" : "keyword"
        },
        "trans_src" : {
          "type" : "keyword"
        },
        "translate" : {
          "type" : "text"
        },
        "tweet" : {
          "type" : "text"
        },
        "urls" : {
          "type" : "keyword"
        },
        "user_id_str" : {
          "type" : "keyword"
        },
        "user_rt" : {
          "type" : "keyword"
        },
        "user_rt_id" : {
          "type" : "keyword"
        },
        "username" : {
          "type" : "keyword"
        },
        "video" : {
          "type" : "integer"
        }
  }
}'
```

### Load tweets from twint into ES

```
twint -u spacguru --elasticsearch localhost:9200
```

### Fetch tweets (example)

```
cd twitter
python es.py

```