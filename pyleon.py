import os 
import time

DEF_LEON_PATH = os.path.join(
    os.path.abspath(__file__).replace(os.path.basename(__file__), ''),
    'leon', 
    'leon'
)

ARG_SUPPRESS_OUTPUT = '>/dev/null 2>&1'

class PyLeon:
    def __init__(self, silent=False, leon_path=DEF_LEON_PATH):
        '''
            Return a PyLeon instance
            :param silent:      suppress output
            :param leon_path:   path to leon executable
        '''

        self.silent = silent
        self.leon_path = leon_path

        if os.name != 'posix':
            print(f"ERROR: LEON can only be run on a POSIX compliant OS.")

        if not os.path.exists(leon_path):
            print(f"ERROR: LEON executable does not exist at {leon_path}.")
            raise FileNotFoundError(leon_path)
        
        if os.system(f'{leon_path} {ARG_SUPPRESS_OUTPUT}') != 0:
            print(f"ERROR: LEON executable could not be run at {leon_path}.")
            raise RuntimeError


    def compress(self, file, kmer_size=None, abundance=None, nb_cores=None, 
        lossless=False, seq_only=False, noheader=False, noqual=False):
        '''
            Compress a fastq/fasta file.
            :param file:        File to compress
            :param kmer_size:   kmer size (default 31), currently should be <32
            :param abundance:   minimal abundance threshold for solid kmers 
                                (default: automatic)
            :param nb_cores:    number of cores (default is the maximum 
                                available number of cores)
            :param lossless:    switch to lossless compression for qualities 
                                (default is lossy. lossy has much higher 
                                compression rate, and the loss is in fact a 
                                gain. lossy is better!)
            :param seq_only:    store dna sequence only, header and qualities 
                                are discarded, will decompress to fasta (same 
                                as -noheader -noqual)
            :param noheader:    discard header
            :param noqual:      discard quality scores
        '''

        args = ['-c']
        if kmer_size is not None:   args.append(f'-kmer-size {kmer_size}')
        if abundance is not None:   args.append(f'-abundance {abundance}')
        if nb_cores is not None:    args.append(f'-nb-cores {nb_cores}')
        if lossless:                args.append('-lossless')
        if seq_only:                args.append('-seq-only')
        if noheader:                args.append('-noheader')
        if noqual:                  args.append('-noqual')
        
        return self._process(file, args)


    def decompress(self, file, nb_cores=-1):
        '''
            Decompress a leon file.
            :param file:        File to decompress
            :param nb_cores:    number of cores (default is the maximum 
                                available number of cores)
        '''

        args = ['-d']
        if nb_cores != -1:          args.append('-nb-cores ' + str(nb_cores))

        return self._process(file, args)


    def _process(self, filepath, args):
        timestamp = str(time.time_ns())
        directory = os.path.dirname(filepath)
        filename = os.path.basename(filepath)
        temppath = os.path.join(directory, timestamp + filename)
        
        if self.silent: args.append(ARG_SUPPRESS_OUTPUT)

        # copy original file to temp file for tracking purposes
        os.system(f'cp {filepath} {temppath}')
        os.system(f'{self.leon_path} -file {temppath} {" ".join(args)}')
        os.remove(temppath)

        # locate temp file and copy to final file
        for file in os.listdir(directory):
            if timestamp not in file:
                continue

            outfile = file.replace(timestamp, '')
            outpath = os.path.join(directory, outfile)
            temppath = os.path.join(directory, file)

            os.system(f'cp {temppath} {outpath}')
            os.remove(temppath)
            return outpath

        return None