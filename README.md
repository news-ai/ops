`curl -XPUT https://newsai:@search1.newsai.org/_cluster/settings -d '{"persistent" : {"threadpool.bulk.queue_size" : 100000}}'`

`curl -XPUT "https://newsai:@search1.newsai.org/contacts/_settings" -d '{"index" : {"max_result_window" : 500000 }}'`
