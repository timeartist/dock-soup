from redis import StrictRedis

class Base(object):
    def __init__(self, key_base=None, **kwargs):
        self.r = StrictRedis(**kwargs)
        
        self.key_base = key_base or 'NAMESPACE:%s'  ##Should probably be subclassed
        self._get_meta_key = lambda x: self.key_base%x


    def set(self, key, dict_val):
        self.r.hmset(self._get_meta_key(key), dict_val)
        
    def get(self, key ):
        return self.r.hgetall(self._get_meta_key(key))
    
    def get_multi(self, ids):
        assert isinstance(ids, (tuple, list, set))
        
        pipe = self.r.pipeline()
        for _id in ids:
            pipe.hgetall(self._get_meta_key(_id))
            
        return pipe.execute()
        
    
    def delete(self, key):
        return self.r.delete(self._get_meta_key(key))
    
    