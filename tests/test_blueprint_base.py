from json import loads, dumps

from mock import patch
from mockredis import mock_strict_redis_client

from app import app
from app.blueprints import get, post, put
from app.data import Base

def test(monkeypatch):
    
    ##Test error handling
    with app.test_request_context(data='{"foo": "bar"}'):
        def return_error_test(data):
            return ('banana',)
        
        error_result = post(None, return_error_test)
        assert {u'error': u'banana'} == loads(error_result[0])
        assert error_result[1] == 400
        
    ##Test add/get
    with patch('redis.StrictRedis', mock_strict_redis_client):
        
        ##Setup data
        data0 = {'id':'foo', 'foo':'bar'}
        data0_json = dumps(data0)
        data1 = {'id':'bar', 'bar':'foo'}
        data1_json = dumps(data1)
        data_model = Base(key_base='unittest')
        
        ##Do calls
        with app.test_request_context(data=data0_json):
            post_resp = post(data_model, lambda x: False)
            get_resp = get(data0['id'], data_model)
        with app.test_request_context(data=data1_json):
            post(data_model, lambda x: False)
            ids_str = ','.join((data0['id'], data1['id']))
            get_multi_resp = get(ids_str, data_model)
            
    ##Test Results  
    assert loads(get_resp[0]) == data0 and get_resp[1] == 200
    assert loads(get_multi_resp[0]) == [data0, data1] and get_multi_resp[1] == 200
    data0.update({'success':True})
    assert loads(post_resp[0]) == data0 and post_resp[1] == 200
           