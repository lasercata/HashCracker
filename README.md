# HashCracker

Multithreaded hash cracker.

## Usage
### Setup
Get the code :
```
git clone --depth=1 https://github.com/lasercata/HashCracker.git
cd HashCracker
```

Make the main file executable :
```
chmod u+x HashCracker.py
```

### Run

```
$ ./HashCracker.py -h
usage: HashCracker [-h] [-V] [-s] [-A ALGORITHM] [-a ALPHABET] [-t NB_THREADS] [-l LIMIT] hash

Multithreaded hash cracker

positional arguments:
  hash                  the hash to crack

options:
  -h, --help            show this help message and exit
  -V, --version         show version and exit
  -s, --silent          only print the password and nothing else
  -A, --algorithm ALGORITHM
                        the hash algorithm. Defaults to "md5".
  -a, --alphabet ALPHABET
                        the alphabet to use. Can be [0-9], [a-z], [a-z0-9], [a-zA-Z], [a-zA-Z0-9], or directly the raw alphabet
  -t, --nb-threads NB_THREADS
                        Specify the number of threads to use. If not set, it gets the number of thread available on the current machine
  -l, --limit LIMIT     If used, limit the length of words to LIMIT

Examples :
	./main.py [hash]
	./main.py -a 0123456789 [hash]
	./main.py -a 0123456789 -A sha256 [hash]
	./main.py -t 12 [hash]
```

## Licence
This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
