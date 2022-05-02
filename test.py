from pyleon import PyLeon
import os, hashlib

# via https://stackoverflow.com/a/22058673
def hash_file(filename):
    BUF_SIZE = 65536
    md5 = hashlib.md5()

    with open(filename, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)
    
    return md5.hexdigest()


def test_file(filepath, lossless):
    pyleon = PyLeon(silent=True)
    print(f'\nTEST filepath:      {filepath}')

    leon_file = pyleon.compress(filepath, lossless=lossless)
    d_file = pyleon.decompress(leon_file)
    print(f'original filesize:  {os.path.getsize(filepath)} bytes')
    print(f'leon filesize:      {os.path.getsize(leon_file)} bytes')

    match = str(hash_file(filepath)) == str(hash_file(d_file))
    
    print(f'lossless:           {lossless}')
    print(f'hashes match:       {match}')

    # os.remove(leon_file)
    os.remove(d_file)


def test_dir_files(dirname, absolute=False, lossless=True):
    for file in os.listdir(dirname):
        if file.split('.')[-1] not in ['fastq', 'fasta']:
            continue
        
        filepath = f'{dirname}/{file}'
        if absolute: filepath = os.path.abspath(filepath)

        test_file(filepath, lossless)


test_dir_files('./fasta', lossless=True)
# test_dir_files('./fastq')
# test_dir_files('./fastq', absolute=True)
test_dir_files('./fastq', lossless=True)