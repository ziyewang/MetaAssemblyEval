# -*- coding: utf-8 -*-
# @Author  : ziye Wang
# @FileName: metaAssemblyEval.py
import os
import argparse
import sys
import logging

logger = logging.getLogger('metaAssemblyEval')

logger.setLevel(logging.INFO)

# logging
formatter = logging.Formatter('%(asctime)s - %(message)s')

console_hdr = logging.StreamHandler()
console_hdr.setFormatter(formatter)

logger.addHandler(console_hdr)


def arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('--r1', type=str, help=("File with forward reads of real metagenome."))
    parser.add_argument('--r2', type=str, help=("File with reverse reads of real metagenome."))
    parser.add_argument('--sequencing_depth', type=int,
                        help="Specify the sequencing depth of simulated genomes.")
    parser.add_argument('--read_length', default=101, type=int,
                        help="Specify the read length. It is default value is 101.")
    parser.add_argument('--genome_sequence_dir', type=str, help=(
        "The input dir where the sequence of the genomes to be added in the real metagenome locates，ending with '/'."))
    parser.add_argument('--output', type=str, help="The output dir, storing the statistics results of the assembly, ending with '/'.")

    args = parser.parse_args()

    if not (args.r1 and args.r2 and args.output and args.sequencing_depth and args.genome_sequence_dir ):
        parser.error(
            "Data is missing, add file(s) using --r1 <read_file> and/or --r2 <read_file> and/or genome_sequence_dir <dir>-- and/or --output <out_dir>")
        sys.exit(0)
    return args


def process_file(reader):
    '''Open, read,and print a file'''
    names = []
    dict = {}
    for line in reader:
        if line.startswith('>'):
            names.append(line)
            name = line[:-1]
            seq = ''
        else:
            seq += line[:-1]
            dict[name] = seq
    return dict


def simualtion(genome_path, sequence_depth, read_length, out_dir):
    files = os.listdir(genome_path)
    for file in files:
        if not os.path.isdir(genome_path + file):
            if file[-5:] == 'fasta':
                input_file = open(genome_path + file, "r")
                reader = input_file.readlines()
                items = process_file(reader)
                length = int(len(str(items.values())))
                n = length * sequence_depth / (2 * read_length)
                os.system('mason_simulator --illumina-read-length %d -ir %s%s -n %d -o %s%s_1.fq -or %s%s_2.fq' % ( read_length, genome_path, file, n, out_dir, file, out_dir, file))
    logger.info("Simulation finished.")


def running_assemblers(out_dir, r1, r2, read_length):
    os.system('cat %s*_1.fq %s >> %smerge_1.fq' % (out_dir, r1, out_dir))
    os.system('cat %s*_2.fq %s >> %smerge_2.fq' % (out_dir, r2, out_dir))
    fq2fa_url = os.path.join(os.getcwd(), 'auxiliary', 'idba-1.1.1', 'bin',
                             'fq2fa') 
    fq2fa_cmd = fq2fa_url + " --merge --filter " + out_dir + 'merge_1.fq ' + out_dir + 'merge_2.fq ' + out_dir + 'merge.fa '
    os.system(fq2fa_cmd)
    megahit_cmd = '/home/wzy/tools/assembly_tool/megahit/megahit ' + '-1 ' + out_dir + 'merge_1.fq ' + '-2 ' + out_dir + 'merge_2.fq ' + '-o ' + out_dir + 'megahit_contig'
    os.system(megahit_cmd)
    metaspades_cmd = '/home/wzy/tools/assembly_tool/SPAdes-3.12.0-Linux/bin/spades.py' + ' --meta' + ' -1 ' + out_dir + 'merge_1.fq ' + '-2 ' + out_dir + 'merge_2.fq ' + '-o ' + out_dir + 'metaspades_contig'
    os.system(metaspades_cmd)
    idba_ud_url = os.path.join(os.getcwd(), 'auxiliary', 'idba-1.1.1', 'bin', 'idba_ud')
    idba_ud_cmd = idba_ud_url + ' --pre_correction' + ' -r ' + out_dir + 'merge.fa ' + '-o ' + out_dir + 'idba_contig'
    os.system(idba_ud_cmd)
    ntcard_cmd = 'ntcard -t 10 -k31 -p ' + out_dir + 'ntcard_result ' + out_dir + 'merge.fa'
    os.system(ntcard_cmd)
    ntcard_result = open(out_dir + 'ntcard_result_k31.hist', 'r')
    line = ntcard_result.readlines()
    second_line = line[1]
    t = second_line.index("\t")
    F0 = second_line[t + 1:-1]
    third_line = line[2]
    t = third_line.index("\t")
    f1 = third_line[t + 1:-1]
    os.makedirs(out_dir + 'faucet_contig')
    faucet_cmd = '/mnt/data2/wzy/assembly/Faucet-master/src/faucet' + ' -read_load_file ' + out_dir + 'merge.fa' + ' -read_scan_file ' + out_dir + 'merge.fa' + ' --paired_ends -size_kmer 31 -max_read_length ' + str(
        read_length) + ' -estimated_kmers ' + F0 + ' -singletons ' + f1 + ' -file_prefix ' + out_dir + 'faucet_contig/faucet'
    os.system(faucet_cmd)
    logger.info("Assembly finished.")


def evaluation(out_dir, genome_path):
    files = os.listdir(genome_path)
    genome_name = []
    for file in files:
        if file[-5:] == 'fasta':
            genome_name.append(file)
    reference = ''
    genome_num = len(genome_name)
    i = 0
    for genome in genome_name:
        reference = reference + genome_path + genome
        i += 1
        if i <= genome_num - 1:
            reference = reference + ','

    quast_cmd = 'metaquast.py ' + out_dir + 'megahit_contig/final.contigs.fa ' + out_dir + 'metaspades_contig/contigs.fasta ' + out_dir + 'idba_contig/contig.fa ' + out_dir + 'faucet_contig/faucet.cleaned_contigs.fasta'+' -r '+reference+ ' -1 '+out_dir+ 'merge_1.fq'+ ' -2 '+out_dir+ 'merge_2.fq'+' -o '+out_dir+'quast_output'+' --space-efficient -l MEGAHIT,metaSPAdes,IDBA-UD,Faucet'
    os.system(quast_cmd)
    logger.info("Evaluation finished.")

if __name__ == '__main__':
    args = arguments()
    genome_path = args.genome_sequence_dir
    sequence_depth = args.sequencing_depth
    out_dir = args.output
    read_length = args.read_length
    r1 = args.r1
    r2 = args.r2
    logger.info("Simulation begin.")
    simualtion(genome_path, sequence_depth, read_length, out_dir)
    logger.info("Assembly begin.")
    running_assemblers(out_dir, r1, r2, read_length)
    logger.info("Evaluation begin.")
    evaluation(out_dir, genome_path)
    logger.info("Thank you for using metaAssemblyEval!")




