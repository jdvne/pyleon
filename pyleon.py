import os 
import time  

class PyLeon:
    def __init__(self, silent = False):
        self.silent = silent
        # check that leon exists

    def compress(self, file, kmer_size = None, abundance = None, nb_cores = None, lossless = False, seq_only = False, noheader = False, noqual = False):
        '''
            Compress a fastq/fasta file.
            :param file:        File to compress
            :param kmer_size:   kmer size (default 31), currently should be <32
            :param abundance:   minimal abundance threshold for solid kmers (default: automatic)
            :param nb_cores:    number of cores (default is the maximum available number of cores)
            :param lossless:    switch to lossless compression for qualities (default is lossy. lossy has much higher compression rate, and the loss is in fact a gain. lossy is better!)
            :param seq_only:    store dna sequence only, header and qualities are discarded, will decompress to fasta (same as -noheader -noqual)
            :param noheader:    
            :param noqual:      
        '''
        command = ['-file', file, '-c']
        if kmer_size is not None: command.append('-kmer-size ' + str(kmer_size))
        if abundance is not None: command.append('-abundance ' + str(abundance))
        if nb_cores is not None: command.append('-nb-cores ' + str(nb_cores))
        if lossless: command.append('-lossless')
        if seq_only: command.append('-seq-only')
        if noheader: command.append('-noheader')
        if noqual: command.append('-noqual')
        if self._execute(file, command) == 0:
            filename = file.split(".")
            while True:
                if filename[-1] in ["fastq", "fasta", "gz"]:
                    del filename[-1]
                else: break 
            return ".".join(filename) + ".leon"
        return None 

    def decompress(self, file, nb_cores = -1):
        command = ['-file', file, '-d']
        if nb_cores != -1: command.append('-nb-cores ' + str(nb_cores))
        return self._execute(file, command)

    def _execute(self, filename, args):
        timestamp = str(time.time())
        os.system('cp ' + filename + ' ' + timestamp + '_' + filename.split("/")[-1])
        ret = os.system('./leon/leon ' + ' '.join(args) + " >/dev/null" if self.silent else "")
        for file in os.listdir('./'):
