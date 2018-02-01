import urllib2
import json

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
        endpoint = members[node_id]['addr'] + path
        healthy_nodes += _is_available(endpoint)
    
    if quorum > healthy_nodes:
        return 0
    else:
        if quorum - healthy_nodes > 0:
            return 2
        else:
            return 1

if __name__ == '__main__':
    url = 'http://localhost:6080/state'
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
            print('red')
        elif 1 in results:
            print('yellow')
        else:
            print('green')
