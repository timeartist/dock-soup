from json import loads

from flask import jsonify, request


def get(ids, data):
    print ids, data
    if ',' in ids:
        print 'multiple'
        _ids = ids.split(',')
        resp_data = data.get_metadata_multi(_ids)
        print resp_data
        if any(resp_data):
            return jsonify(resp_data)
    else:
        print 'singular'
        resp_data = data.get_metadata(ids)
        print resp_data
        if resp_data:
            return jsonify(resp_data)   
    
    ##error
    return jsonify({'error':'ids not found'}), 404


def post(data, validation):
    req = loads(request.data) if request.data else {}
    errors = validation(req)
    if errors:
        print '\n'.join(errors)
        return jsonify({'error':'\n'.join(errors)}), 400
    
    data.set_metadata(req['id'], req)
    
    req['success'] = True
    
    return jsonify(req)


def put(_id, data):
    req = loads(request.data) if request.data else {}
    resp_data = data.get_metadata(_id)
    
    if not resp_data:
        return jsonify({'error':'video not found'}), 404
    
    resp_data.update(req)
    data.set_metadata(_id, resp_data)
    
    resp_data['success'] = True
    
    return jsonify(resp_data)

