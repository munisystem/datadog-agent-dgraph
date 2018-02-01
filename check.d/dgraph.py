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

def _get_status(nodes, port, path):
    quorum = round(len(nodes)/float(2))
    healthy_nodes = 0
    for node_id in nodes:
        node = nodes[node_id]
        addr = node['addr'].split(':')[0]
        endpoint = 'http://' + addr + ':' + port + path
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
            results.append(_get_status(members, '8080', '/health'))

        # check zeros
        results.append(_get_status(zeros, '6080', '/state'))

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
        addr = instance.get('addr')
        if addr is None:
            raise Exception("addr must be specified in the instance.")

        endpoint = addr + "/state"
        health = _get_health(endpoint)
        self.gauge('dgraph.cluster_health', health)
