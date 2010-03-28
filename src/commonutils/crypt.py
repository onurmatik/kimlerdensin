from django.conf import settings
import django.contrib.contenttypes.models
from django.contrib import contenttypes
from Crypto.Cipher import Blowfish
from base64 import *
import random
import sha

# Caches of content types/models
_model_cache = {}
_model_name_cache = {}
_content_type_cache = {}
_content_type_rec_cache = {}


def verify_objref_hash( content_type_id, object_id, hash ):
    hash_match = sha.new("%s/%s" % (content_type_id, object_id) + settings.SECRET_KEY).hexdigest()
    if hash == hash_match:
        return True
    else:
        return False

def cryptString( plain ):
    obj=Blowfish.new( settings.SECRET_KEY, Blowfish.MODE_ECB)
    randstring = open("/dev/urandom").read(12)
    split = random.randrange(10)+1
    s = randstring[:split] +  ':valid:' + plain +':valid:'+ randstring[split:]
    length = len(s)

    l = length + 8 - ( length % 8 )
    padded = s +  " " * ( 8 - length % 8)

    ciph=obj.encrypt(padded[:l])
    try:
        return b32encode(ciph)
    except NameError:
        return encodestring(ciph)

def decryptString( cipher ):
    obj=Blowfish.new( settings.SECRET_KEY, Blowfish.MODE_ECB)
    try:
        ciph = b32decode( cipher )
    except NameError:
        ciph = decodestring(cipher )
    
    plaintext = obj.decrypt(ciph)
    try:
        (c1, email,c2) = plaintext.split(":valid:")
    except ValueError:
        return None
    return email

def get_object(content_type_id, pk_val):
    """Gets an object from the content type id and a primary key"""
    return get_model(content_type_id)._default_manager.get(pk=pk_val)

def get_model(content_type_id):
    """Gets a model class for a given content_type_id"""
    try:
        return _model_cache[content_type_id]
    except KeyError:
        try:
            ct = contenttypes.models.ContentType.objects.get(pk=content_type_id)
        except contenttypes.models.ContentType.DoesNotExist:
            return None
        model = ct.model_class()
        if model is None:
            return None

        _model_cache[content_type_id] = model
        db = model._meta.db_table
        _content_type_cache[db] = content_type_id
        _content_type_rec_cache[db] = ct
        return model

def get_content_type_id(model):
    """Gets a content type id for a given model"""
    try:
        db = model._meta.db_table
        return _content_type_cache[db]
    except:
        ct = contenttypes.models.ContentType.objects.get_for_model(model)
        model = ct.model_class()
        _model_cache[ct.id] = model
        db = model._meta.db_table
        _content_type_cache[db] = ct.id
        _content_type_rec_cache[db] = ct
        return ct.id

def get_content_type(model):
    """Gets a content type record for a given model"""
    try:
        db = model._meta.db_table
        return _content_type_rec_cache[db]
    except:
        ct = contenttypes.models.ContentType.objects.get_for_model(model)
        model = ct.model_class()
        _model_cache[ct.id] = model
        db = model._meta.db_table
        _content_type_cache[db] = ct.id
        _content_type_rec_cache[db] = ct
        return ct

def get_content_type_id_by_modelname(modelname):
    """Gets a content type record for a given modelname"""
    try:
        return _model_name_cache[modelname]
    except:
        ct = contenttypes.models.ContentType.objects.get(model=modelname)
        _model_name_cache[modelname] = ct.id
        return ct.id
