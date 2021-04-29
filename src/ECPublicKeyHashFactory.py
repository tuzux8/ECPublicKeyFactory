import sys, getopt
import hashlib
from ecdsa.keys import VerifyingKey
from ecdsa.curves import NIST256p


def get_public_key_fingerprint(curve, temp_public_key):
    """
    Validate the public key if it is related to the given EC curve and
    formats the public key to a uncompressed byte string.
    Afterwards the function create a hash value of the uncompressed public key value

    :param curve: currently is only NIST256p supported
    :param temp_public_key: public key in hex format
    :return: SHA-256 hash value of the uncompressed public key string
    """

    vk = VerifyingKey.from_string(bytes.fromhex(temp_public_key), curve=curve)

    uncompressed_pub_key = vk.to_string('uncompressed')

    pub_key_hash_fingerprint = hashlib.sha256(uncompressed_pub_key)

    return pub_key_hash_fingerprint.hexdigest()


def format_public_key(unformated_pk):
    """
    Raised when the paramter -u is given
    :param unformated_pk: unformated public key value with ':'character
    :return: the unformated public key value without ':' character
    """
    return unformated_pk.replace(':', '')


def main(argv):
    public_key_string = ""
    try:
        opts, args = getopt.getopt(argv, "k:u:")
    except getopt.GetoptError:
        print("Used parameter is not valid")
        sys.exit(2)
    for opt, arg in opts:
        if opt in("-k", "--key"):
            if len(str(arg)) == 130:
                public_key_string = arg
            else:
                print("Value is not valid, expected length is 130 bytes")
                sys.exit(2)
        elif opt in ("-u", "--unformatedkey"):
            if len(str(arg)) == 194:
                public_key_string = format_public_key(arg)
            else:
                print("Value is not valid, expected length is 194 bytes")
                sys.exit(2)
        else:
            print("Used parameter is not valid")
            sys.exit(2)

    return public_key_string


if __name__ == "__main__":
    """
    Main function which process the given input
    """
    EC_CURVE = NIST256p

    temp_pk = main(sys.argv[1:])

    # Print Hash Value
    print("EC Public Key Hash Fingerprint: ", get_public_key_fingerprint(EC_CURVE, temp_pk))
