import urllib2
import json

from checks import AgentCheck

class DgraphCheck(AgentCheck):
    def __init__(self, name, init_config, agentConfig, instances=None):
        AgentCheck.__init__(self, name, init_config, agentConfig, instances)

    def _is_available(endpoint):
        try:
            req = urllib2.urlopen(url)
        except urllib2.HTTPError as e:
            return 0
        else:
            if req.getcode() == 200:
                return 1
            else:
                return 0

    # groups['1']['members']
    def _get_status(nodes, path):
        quorum = round(len(nodes)/2, 1)
        healthy_nodes = 0
        for node_id in nodes:
            node = nodes[node_id]
            endpoint = node['addr'] + path
            healthy_nodes += _is_available(endpoint)
        
        if quorum > healthy_nodes:
            return 0
        else:
            if quorum - healthy_nodes > 0:
                return 2
            else:
                return 1

    def _get_health(url):
        try:
            req = urllib2.urlopen(url)
        except urllib2.HTTPError as e:
            print(e)
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
    def check(self, instance):
        addr = instance.get('addr')
        if target is None:
            raise Exception("addr must be specified in the instance.")

        url = addr + "/state"
        health = _get_health(url)
        self.gauge('dgraph.cluster_health', health)
