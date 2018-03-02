import urllib
import json

from checks import AgentCheck

def _is_available(endpoint):
    try:
        req = urllib.urlopen(endpoint)
    except Exception as e:
        return 0
    else:
        if req.getcode() == 200:
            return 1
        else:
            return 0

def _get_status(nodes, path):
    quorum = round(len(nodes)/float(2))
    healthy_nodes = 0
    for node_id in nodes:
        node = nodes[node_id]
        addr, port = node['addr'].split(':')
        http_port = str(int(port) + 1000)
        endpoint = 'http://' + addr + ':' + http_port + path
        healthy_nodes += _is_available(endpoint)
    
    if healthy_nodes < quorum:
        return 0
    else:
        if healthy_nodes - quorum > 0:
            return 2
        else:
            return 1

def _get_health(endpoint):
    try:
        req = urllib.urlopen(endpoint)
    except Exception as e:
        raise Exception(e)
    else:
        body = req.read()
        obj = json.loads(body)
        groups = obj['groups']
        zeros = obj['zeros']

        results = []
        # check groups
        for group_id in groups:
            members = groups[group_id]['members']
            results.append(_get_status(members, '/health'))

        # check zeros
        results.append(_get_status(zeros, '/state'))

        if 0 in results:
            return 0
        elif 1 in results:
            return 1
        else:
            return 2

class DgraphCheck(AgentCheck):
    def __init__(self, name, init_config, agentConfig, instances=None):
        AgentCheck.__init__(self, name, init_config, agentConfig, instances)
    def check(self, instance):
        url = instance.get('url')
        if url is None:
            raise Exception('url must be specified in the instance.')

        health = _get_health(url)
        self.service_check('dgraph.cluster_health', health)
