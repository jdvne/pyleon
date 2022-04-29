import os 
import time  

class PyLeon:
    def __init__(self, silent = False, leon_path = './leon/leon'):
        self.silent = silent
        self.leon_path = leon_path
        code = os.system(leon_path + ' >/dev/null 2>&1')
        if code != 0:
            print("Error: please make sure the LEON executable exists at " + leon_path)
            raise FileNotFoundError

    def compress(self, file, kmer_size = None, abundance = None, nb_cores = None, lossless = False, seq_only = False, noheader = False, noqual = False):
        '''
            Compress a fastq/fasta file.
            :param file:        File to compress
            :param kmer_size:   kmer size (default 31), currently should be <32
            :param abundance:   minimal abundance threshold for solid kmers (default: automatic)
            :param nb_cores:    number of cores (default is the maximum available number of cores)
            :param lossless:    switch to lossless compression for qualities (default is lossy. lossy has much higher compression rate, and the loss is in fact a gain. lossy is better!)
            :param seq_only:    store dna sequence only, header and qualities are discarded, will decompress to fasta (same as -noheader -noqual)
            :param noheader:    discard header
            :param noqual:      discard quality scores
        '''
        command = ['-c']
        if kmer_size is not None: command.append('-kmer-size ' + str(kmer_size))
        if abundance is not None: command.append('-abundance ' + str(abundance))
        if nb_cores is not None: command.append('-nb-cores ' + str(nb_cores))
        if lossless: command.append('-lossless')
        if seq_only: command.append('-seq-only')
        if noheader: command.append('-noheader')
        if noqual: command.append('-noqual')
        return self._execute(file, command)

    def decompress(self, file, nb_cores = -1):
        '''
            Decompress a leon file.
            :param file:        File to decompress
            :param nb_cores:    number of cores (default is the maximum available number of cores)
        '''
        command = ['-d']
        if nb_cores != -1: command.append('-nb-cores ' + str(nb_cores))
        return self._execute(file, command)

    def _execute(self, filename, args):
        timestamp = ''.join(str(time.time()).split('.'))
        directory = '/'.join(filename.split('/')[:-1])
        timestamp_file = directory + '/' + timestamp + filename.split('/')[-1]
        print(timestamp)
        print(f'cp {filename} {timestamp_file}')
        print(f"{self.leon_path} -file {timestamp_file} {' '.join(args)} {' >/dev/null' if self.silent else ''}")
        os.system(f'cp {filename} {timestamp_file}')
        os.system(f"{self.leon_path} -file {timestamp_file} {' '.join(args)} {' >/dev/null' if self.silent else ''}")
        outfile = None 
        for file in os.listdir('/'.join(filename.split('/')[:-1])):
            if timestamp in file:
                outfile = directory + '/' + ''.join(file.split(timestamp))
                os.system('cp ' + directory + '/' + file + ' ' + outfile)
                os.system('rm ' + directory + '/' + file)
                break
        os.system('rm ' + timestamp_file)
        return outfile 