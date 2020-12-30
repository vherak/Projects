# NAME: Vhera Kaey Vijayaraj
# STUDENT ID: 28903013

import random
import math
import sys

def modular_exponientiation(number,exponent,mod):
    """
    This function performs modular exponentiation by using repeated squaring.
    :param number: number that we are using
    :param exponent: exponent of number
    :param mod: what we are dividing by to get the remainder
    :return: returns the number after we do modular exponientiation
    """

    # converts the exponent into binary
    exp_bin = "{0:b}".format(exponent)

    rev = exp_bin[::-1]
    positions =[]
    values = [0]*len(exp_bin)

    # getting the positions of '1' in the binary string
    for i in range(len(rev)-1,-1,-1):
        if rev[i] == '1':
            positions.append(i)


    previous = number % mod
    values[0] = previous
    # performing repeated squaring by squaring the previous value
    for i in range(1,len(exp_bin)):
        result = previous**2 % mod
        previous = result
        values[i] = result

    # multiplying the values where the binary value was '1' from the exponent
    positions = positions[::-1]
    prev = values[positions[0]]
    for i in range(1,len(positions)):
        current = values[positions[i]]
        prev = current * prev % mod

    # returns the number after performing modular exponentiation
    return prev


def millerRabin(n,k):
    """
    This function performs Miller Rabins Primality testing on a random number n with k amount
    of times
    :param n: random number to test on
    :param k: number of times we are testing the random number. this determines how accurate our test is
    :return: returns true if the number is probably prime, and false if it is definitely composite
    """

    # if it is an even number or a negative number, we dont need to test it
    if n % 2 == 0 or n <= 1:
        return False

    # base cases: 2 and 3 are prime
    elif n == 2 or n == 3:
        return True
    else:
        # Factor n-1 as 2^s.t where t is odd
        s = 0
        t = n-1
        while t % 2 == 0:
            s += 1
            t //= 2
        # we will perform k random tests
        for _ in range(k):
            # generate a random number
            a = random.randrange(2,n-1)
            exp = pow(a,n-1,n)

            # if the remainder is not 1, we know it is a composite number
            if exp != 1:
                return False
            else:
                previous =  modular_exponientiation(a,pow(2,0)*t,n)
                for i in range(1,s+1):
                    exp = modular_exponientiation(a,pow(2,i)*t,n) # a^(2^i*t) mod n
                    # if the current remainder is 1 and the previous remainder is not 1 and not -1,
                    # we know that the number is a composite number
                    if exp == 1 and (previous != n-1 and previous != 1):
                        return False
                    previous = exp
        return True


def generatePrimes(k):
    """
    This function generate a random prime number that is k bits long. It will randomly pick a k
    bit number and then tests its primality using Miller Rabins primality testing. It will loop using
    the prime number distribution function and if we generate a prime number, it will print to the terminal.
    If no prime number is generated in the number of times we loop, there will be no output
    :param k: k bits of the number we want to test
    :return:
    """
    n = pow(2,k)-1
    n2 = pow(2,k-1)

    # uses the prime number distribution function pi(x) to get the number of prime numbers
    # in that range. We will loop this amount of times.
    approx = math.ceil(n/(math.log(n)))
    approx2 = math.ceil(n2/(math.log(n2)))
    primes_within_range = approx-approx2

    for i in range(primes_within_range):
        # generates a random prime number between the range
        number = random.randrange(pow(2, k - 1), pow(2, k) - 1)
        result = millerRabin(number,128)

        # if it is a prime number, we will output it to the terminal
        if result == True:
            print(number)
            break


if __name__ == '__main__':
    argument_0 = sys.argv[0]
    argument_1 = sys.argv[1]

    k = int(argument_1)
    generatePrimes(k)