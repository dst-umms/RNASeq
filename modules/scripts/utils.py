#!/usr/bin/env python

# vim: syntax=python tabstop=4 expandtab
# coding: utf-8

#-----------------------------------
# @author: Mahesh Vangala
# @email: vangalamaheshh@gmail.com
# @date: July, 1st, 2016
#-----------------------------------

def getTargetInfo(config):
    targetFiles = []
    targetFiles.extend([_getSTARcounts(config),
                        _convertSJoutToBed(config),
                        _getCuffCounts(config), 
                        _getCuffIsoCounts(config), 
                        _fusionOutput(config), 
                        _insertSizeOutput(config), 
                        _rRNAmetrics(config), 
                        _readQC(config), 
                        _bw(config),
                        _SNP(config),
                        _DE(config),
                        _cluster(config),
                        _pathway(config),
                        _VirusSeq(config),
                        _immunology(config),
                        _copyMetaFiles(config),
                        _CDR3(config)])
    return targetFiles

## Returns proper count files for with and without batch effect correction
def _getSTARcounts(config):
    STAR_out_files = ["analysis/" + config["token"] + "/STAR/batch_corrected_STAR_Gene_Counts.csv"] if config["batch_effect_removal"] == True else ["analysis/" + config["token"] + "/STAR/STAR_Gene_Counts.csv"]
    return STAR_out_files

def _convertSJoutToBed(config):
    ls = ["analysis/STAR/"+sample+"/"+sample+".junctions.bed" for sample in config['ordered_sample_list']]
    return ls

def _getCuffCounts(config):
    cuff_files = ["analysis/" + config["token"] + "/plots/gene_counts.fpkm.png"]
    if config["batch_effect_removal"] == True:
        cuff_files.append("analysis/" + config["token"] + "/cufflinks/batch_corrected_Cuff_Gene_Counts.csv")
    else:
        cuff_files.append("analysis/" + config["token"] + "/cufflinks/Cuff_Gene_Counts.csv")
    return cuff_files

def _getCuffIsoCounts(config):
    cuff_files = ["analysis/" + config["token"] + "/cufflinks/Cuff_Isoform_Counts.csv"]
    return cuff_files

def _getProcessedCuffCounts(config):
    return "analysis/" + config["token"] + "/cufflinks/Cuff_Gene_Counts.filtered.csv"

def _fusionOutput(config):
    fusion_out = []
    if len(config["samples"][config["ordered_sample_list"][0]]) == 2:
        fusion_out.append("analysis/" + config["token"] + "/STAR_Fusion/STAR_Fusion_Report.png")
    return fusion_out

def _insertSizeOutput(config):
    insert_size_out_files = []
    if len(config["samples"][config["ordered_sample_list"][0]]) == 2:
        for sample in config["ordered_sample_list"]:
            insert_size_out_files.append( "analysis/RSeQC/insert_size/" + sample + "/" + sample + ".histogram.pdf" )
    return insert_size_out_files

def _rRNAmetrics(config):
    if config["star_rRNA_index"] is not None:
        return "analysis/" + config["token"] + "/STAR_rRNA/STAR_rRNA_Align_Report.csv"
    else:
        return []

def _cluster(config):
    cluster_files = ["analysis/" + config["token"] + "/plots/pca_plot.pdf",
                    "analysis/" + config["token"] + "/plots/heatmapSS_plot.pdf",
                    "analysis/" + config["token"] + "/plots/heatmapSF_plot.pdf"]
    return cluster_files

def _DE(config):
    de_list = []
    if config["comparisons"]:
        de_list.append("analysis/" + config["token"] + "/diffexp/de_summary.png")
        de_list.extend([["analysis/" + config["token"] + "/diffexp/" + comp + "/" + comp + "_volcano.pdf",
                        "analysis/" + config["token"] + "/diffexp/" + comp + "/deseq_limma_fc_corr.png"]
            if len(config['comps'][comp]['control']) > 1 and len(config['comps'][comp]['treat']) > 1 else
            ["analysis/" + config["token"] + "/diffexp/" + comp + "/" + comp + "_volcano.pdf"] for comp in config["comparisons"]])
    return de_list

def _SNP(config):
    snp_files = ["analysis/" + config["token"] + "/plots/sampleSNPcorr_plot.hla.png"]
    if ('snp_scan_genome' in config and config['snp_scan_genome'] == True):
        snp_files.extend([["analysis/snp/" + sample + "/" + sample + ".snp.genome.vcf", 
            "analysis/snp/" + sample + "/" + sample + ".snpEff.annot.vcf"] for sample in config["ordered_sample_list"]])
    return snp_files

def _readQC(config):
    qc_files = []
    qc_files.append("analysis/" + config["token"] + "/RSeQC/read_distrib/read_distrib.png")
    qc_files.append("analysis/" + config["token"] + "/RSeQC/gene_body_cvg/geneBodyCoverage.heatMap.png")
    qc_files.extend(["analysis/RSeQC/junction_saturation/" + sample + "/" + sample + ".junctionSaturation_plot.pdf" 
        for sample in config["ordered_sample_list"]])
    return qc_files


def _bw(config):
    bw_files = []
    bw_files.extend(["analysis/bam2bw/" + sample + "/" + sample + ".bw" for sample in config["ordered_sample_list"]])
    return bw_files


def _pathway(config):
    path_files = []
    path_files.extend([["analysis/" + config["token"] + "/diffexp/" + comp + "/" + comp + ".goterm.done",
                        "analysis/" + config["token"] + "/diffexp/" + comp + "/" + comp + ".kegg.done"] 
        for comp in config["comparisons"]])
    return path_files

def _VirusSeq(config):
    virus_seq_targets = []
    if ('virus_dna_scan' in config and config['virus_dna_scan'] == True and config['reference'] == 'hg19'):
        virus_seq_targets = ["analysis/" + config["token"] + "/virusseq/virusseq_summary.csv"]
        virus_seq_targets.extend(["analysis/" + config["token"] + "/virusseq/virusseq_Cuff_Isoform_Counts.csv"])
        virus_seq_targets.extend(["analysis/virusseq/" + sample + "/" + sample + ".virusseq.filtered.gtf" for sample in config["ordered_sample_list"]])
        virus_seq_targets.extend(["analysis/virusseq/"+sample+"/STAR/"+sample+".virus.Aligned.sortedByCoord.out.bw" for sample in config['ordered_sample_list']])
        virus_seq_targets.extend(["analysis/virusseq/"+sample+"/STAR/"+sample+".virus.junctions.bed" for sample in config['ordered_sample_list']])
    return virus_seq_targets

def _immunology(config):
    targets = []
    #NOTE: cancer_type must be a valid string that is NOT 'FALSE'
    if ('cancer_type' in config) and (config["cancer_type"].upper() !='FALSE'):
        targets = ["analysis/" + config["token"] + "/immunology/relative_abundance.txt",
                   "analysis/" + config["token"] + "/immunology/output.pdf",
                   "analysis/" + config["token"] + "/immunology/TIMER_results.pdf"]
    return targets

def _copyMetaFiles(config):
    return ["analysis/" + config["token"] + "/" + config["token"] + '.config.yaml',
            "analysis/" + config["token"] + "/" + config["token"] + '.metasheet.csv']

def _CDR3(config):
    cdr3_targets = []
    if ('cdr3_analysis' in config and config['cdr3_analysis'] == True and config['reference'] == 'hg19'):
        #LEN: Do we need to tokenize these results??--can bams be reanalyzed?
        cdr3_targets = ["analysis/cdr3/"+sample+"/"+sample+".sorted.bam.fa" for sample in config["ordered_sample_list"]]
        cdr3_targets.extend(["analysis/cdr3/"+sample+"/"+sample+".sorted.bam-Locs.bam" for sample in config["ordered_sample_list"]])
        cdr3_targets.extend(["analysis/cdr3/"+sample+"/"+sample+".sorted.bam-unmapped.bam" for sample in config["ordered_sample_list"]])

    return cdr3_targets
