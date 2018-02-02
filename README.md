# Datadog Agent Check for Dgraph

Allow to monitor Dgraph cluster health with Datadog.

## Overview

This checks send Dgraph cluster health metrics like Elasticsearch.

Health are three state green(2), yellow(1) and red(0).

* green: possible to down one or more zeros and servers
* yellow: may be below raft quorum when a node down
* red: a state of below raft quorum, Dgraph is unavailable

## Installation

Copy `check.d/dgraph.py` to your Datadog Agent `checks.d` directory and add `dgraph.yaml` to `conf.d` directory.

```yml
init_config:

instances:
  - url: http://localhost:6080/state
```

## License
This project is releases under the [MIT license](http://opensource.org/licenses/MIT).
