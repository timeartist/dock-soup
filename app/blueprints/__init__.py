from json import loads, dumps

from flask import request


def get(ids, data):
    print ids, data
    if ',' in ids:
        print 'multiple'
        _ids = ids.split(',')
        print _ids
        resp_data = data.get_multi(_ids)
        print resp_data
        if any(resp_data):
            return dumps(resp_data), 200
    else:
        print 'singular'
        resp_data = data.get(ids)
        print resp_data
        if resp_data:
            return dumps(resp_data), 200 
    
    ##error
    return jsonify({'error':'ids not found'}), 404


def post(data, validation):
    req = loads(request.data) if request.data else {}
    errors = validation(req)
    if errors:
        print '\n'.join(errors)
        return dumps({'error':'\n'.join(errors)}), 400
    
    data.set(req['id'], req)
    
    req['success'] = True
    
    return dumps(req), 200


def put(_id, data):
    req = loads(request.data) if request.data else {}
    resp_data = data.get(_id)
    
    if not resp_data:
        return dumps({'error':'%s not found'%data.name}), 404
    
    resp_data.update(req)
    data.set(_id, resp_data)
    
    resp_data['success'] = True
    
    return dumps(resp_data), 200

