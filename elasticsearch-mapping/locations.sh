curl -XPOST https://newsai:XkJRNRx2EGCd6@search.newsai.org/locations1 -d '{
    "settings": {
        "number_of_shards": 1,
        "analysis": {
            "filter": {
                "nGram_filter": {
                    "type": "nGram",
                    "min_gram": 2,
                    "max_gram": 20,
                    "token_chars": [
                        "letter",
                        "digit",
                        "punctuation",
                        "symbol"
                    ]
                }
            },
            "analyzer": {
                "nGram_analyzer": {
                    "type": "custom",
                    "tokenizer": "whitespace",
                    "filter": [
                        "lowercase",
                        "asciifolding",
                        "nGram_filter"
                    ]
                },
                "whitespace_analyzer": {
                    "type": "custom",
                    "tokenizer": "whitespace",
                    "filter": [
                        "lowercase",
                        "asciifolding"
                    ]
                }
            }
        }
    },
    "mappings": {
        "country": {
            "properties": {
                "data": {
                    "properties": {
                        "_all": {
                            "index_analyzer": "nGram_analyzer",
                            "search_analyzer": "whitespace_analyzer"
                        },
                        "countryName": {
                            "type": "string",
                            "index": "not_analyzed"
                        }
                    }
                }
            }
        },
        "state": {
            "properties": {
                "data": {
                    "properties": {
                        "_all": {
                            "index_analyzer": "nGram_analyzer",
                            "search_analyzer": "whitespace_analyzer"
                        },
                        "stateName": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "countryName": {
                            "type": "string",
                            "index": "not_analyzed"
                        }
                    }
                }
            }
        },
        "city": {
            "properties": {
                "data": {
                    "properties": {
                        "_all": {
                            "index_analyzer": "nGram_analyzer",
                            "search_analyzer": "whitespace_analyzer"
                        },
                        "cityName": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "stateName": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "countryName": {
                            "type": "string",
                            "index": "not_analyzed"
                        }
                    }
                }
            }
        }
    }
}'