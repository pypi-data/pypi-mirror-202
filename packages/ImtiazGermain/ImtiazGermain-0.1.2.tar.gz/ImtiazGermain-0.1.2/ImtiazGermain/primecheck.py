from sympy import isprime

class primecheck:
    @staticmethod
    def isgermainprime(n):
        # Check if n is a prime number
        if not isprime(n):
            return False
        
        # Check if 2n + 1 is also a prime number
        return isprime(2*n + 1)
    
    @staticmethod
    def isimtiazgermainprime(n):
        # Check if n is a Sophie Germain prime
        p = (n - 1) / 2
        if not isprime(n) or not isprime(p) or not isprime(2*p + 1):
            return False
        
        # Check if 2p + 1 is composite
        m = 2 * p + 1
        if isprime(m):
            return False
        
        # Check if 2(2p + 1) + 1 is prime
        q = 2 * m + 1
        return isprime(q)
