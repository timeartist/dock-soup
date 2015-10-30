from os import environ

from mock import patch
from mockredis import mock_strict_redis_client

from app.data import Base


def test_base(monkeypatch):
    
    ##Setup
    key_base = 'unittest'
    test_data = {'bar':'baz', 'asdf':'fdaz'}
    test_key = 'foo'
    with patch('redis.StrictRedis', mock_strict_redis_client):
        base = Base(key_base=key_base)
        r = base.r
        r.flushdb()
        
        ##Actual Tests
        base.set(test_key, test_data)
        assert r.hget(key_base+ ':%s'%test_key, 'bar') == 'baz'
        assert r.hget(key_base+ ':%s'%test_key, 'asdf') == 'fdaz'
        
        assert base.get(test_key) == test_data
        
        base.delete(test_key)
        assert r.get(key_base + ':%s'%test_key) is None
        
        keys = ('foo', 'bar')
        data0, data1 = {'foo':'bar'}, {'baz':'foo'}
        
        base.set(keys[0], data0)
        base.set(keys[1], data1)
        
        assert [data0, data1] == base.get_multi(keys)
        
        ##Cleanup
        r.flushdb()
    

    