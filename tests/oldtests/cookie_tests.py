import time, hashlib
def user2Cookie( email, passwd, max_age, secretKey ):
    expires = str( int( time.time() + max_age ) )
    s = '%s-%s-%s-%s' % ( email, passwd, expires, secretKey )
    cookie = [ email, expires, hashlib.sha1( s.encode( 'utf-8' ) ).hexdigest() ]
    return '-'.join( cookie )
    
secretKey = 'Secret'
cookie = user2Cookie( '752736341@qq.com', 'test', 86400, secretKey ) 
print( cookie )

def cookie2User( cookieStr, secretKey ):
    try:
        cookie = cookieStr.split( '-' )
        if len( cookie ) != 3 :
            return None
        
        email, expires, sha1 = cookie
        if int( expires ) < time.time():
            return None
        passwd = 'test'
        s = '%s-%s-%s-%s' % ( email, passwd, expires, secretKey )
        esha = hashlib.sha1( s.encode( 'utf-8' ) ).hexdigest()
        if sha1 != esha:
            print( 'actual %s not equal with expect %s' % ( sha1, esha ) ) 
            return None
    except Exception as e:
        print( e )
    
    return None

cookie2User( cookie, secretKey )

def authenticate( email, passwd ):
    sha = hashlib.sha1()
    # sha1.update( email )

