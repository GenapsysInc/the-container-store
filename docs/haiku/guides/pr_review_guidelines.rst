PR Review Guidelines
***************************

Purpose
=======
The purpose of this document is to provide guidelines for the developer and the reviewers of pull requests in the pipeline.

To this end, first a high level set of coding requirements are spelled out for all developers to closely follow and all reviewers to carefully look for. Second, a primary, secondary, and sometimes tertiary owner is defined for each module of the pipeline who will be reviewing each other’s and any code change in those modules. Third, a checklist of all important items are listed for each module as a guideline for the developers to know how their code will be evaluated and for the developer to go through and check.

Coding Requirements
==========================

See the coding guidelines document - :doc:`coding_guidelines`


How to keep working branch up to date
=====================================

After every branch checkout all the submodules and package requirements should be updated to make sure the code is running with the packages and libraries that are mentioned in the branch. An example would be updating the local dev branch after some PRs are merged to dev.
The process starts with checking out a branch; make sure submodules are also checked out without any issues.

.. code-block:: bash

   git submodule sync
   git submodule update



Useful tips and links
=====================

Internal Links
--------------

The Readme.md file on the Github page has instructions for setting up a fork, installing a local environment, and tips on keeping your dev code up-to-date, and how to manage pull requests.

When you have finished coding and need to submit a pull request to QA, here are the mechanics for doing this in a way that will keep our process running smoothly: Pull Request Submission and Test

If you are Modifying a submodule, you will want to review the Submitting PRs to Submodules document with extensive information about how to navigate the added complex of modifying a and one of it’s submodules

Additionally, if you are submitting a issue for others to work on withing the git issues page of eureka, consult this document for the proper information to include: Issue Submission Guidances

External Links
--------------

Please note the bullet points above have precedence in cases the links might differ from the points above. These are provided as useful points and good practices to help with the concepts.

Python Best Practices – Every Python Developer Must Know

PEP8, there might be slight differences with the coding requirements but generally in agreement.

Python Anti-Patterns - It’s good to know what not to do.

Reviewer - Module Matrix
========================

.. include:: module_approvers.rst


Reviewer’s Checklist
====================

Reviewing every PR diff results the missing files should be taken very seriously. In other words, in algorithmic changes no difference in the name and number of files is expected and a difference could be an indication of chaine effect. Module X is changed and some process from module X is used elsewhere that results in mis behaviour.
If a method within one module is changed, make sure other functionalities/methods of the same module are not affected unexpectedly and are functional.
In cases of changes to the output results, make sure the proper change is made to all the users of the results and indeed the change in the results format is necessary.

Sensor ID
---------
The following items must be checked by the reviewer every time there is a change in the sensor_id code. The changes should be monitored from the first figure and proceed. If the first figure is zero diff the rest would be fine.

  * Step_2 - Active Sensors Detection By Reads.png
  * Step_2 - Active Sensors Detection By Reads - HP Summary.png
  * Step_0 - GAIN Histogram - HP Summary.png
  * Verify beadless / with bead sensor_id paths are functional and any differences are expected

Sign Filter
-----------

The following items must be checked by the reviewer every time there is a change in the sign_filter code.
jumps_mean.png plot, the number of sensors and the values
Active_sensors_boxplot.png,
Check the limits, the box_plots at different flows, median, 25%, 75%, variation from the beginning of the run to the end to be similar with the baseline.
Reference_sensors_boxplot.png
Check the limits, the box_plots at different flows, median, 25%, 75%, variation from the beginning of the run to the end to be similar with the baseline.
If adding / modifying filters, make sure to maintain the current API
Verify functionality of “jumps_filters_list” and “filters_list” in config.
Make sure that all sign_filter features work with context_generator, and context_generator is able to make sign_filter contexts.

HP Caller / Binary Caller
-------------------------
The following items must be checked by the reviewer every time there is a change in the hp_caller code.

All data extraction in populate_data_dict is functional and “data_to_load” lists for each feature in networks/features/ have the same data/key names.
Check nucleotide ratio and baseball length for no unexpected results.

Quality Caller
--------------
The following items must be checked by the reviewer every time there is a change in the quality_caller code.

Be aware of the current state of implementation of Options for Full G4 analysis, it may affect what functionality needs to be in QC or BO
Many of the tools needed in quality_caller live in analysis/quality/ folder. Many of those routines have been converted to Cython for speed purposes, and in some cases there are python implementations of the cython code, good for debugging and development.
There are two routes that need to work: one for production and one for quality training. These are controlled by the generate_phred_training_data and fast_route flags. When generating phred training data, fast_route should be false, and the code will generate data for all the predictors. In production, it uses Cython code for speed, and only generates the predictors for the current phred model.
Verify that get_summary_json() function works


Basecall Optimizer
------------------
The following items must be checked by the reviewer every time there is a change in the basecall_optimizer code.

Everything, all the processing, including pos_processing of BO is on the top-level.
If you are making a major significant change that may involve new files or expensive processing, these should likely be moved to karect. Discuss with manager and/or head of software.
We don’t want to have intermediate files other than the final fastq.
Be aware of the current state of implementation of Options for Full G4 analysis, it may affect whether we need to split data at the end of post_process so it can be processed separately for each segment (or on each pod). This will go away once we have rahpbo from the top-level.
Make sure the coverage calculation is working and verify the binning is functioning properly.
We are running BO in different PODs, all from top level (but a batch of sensors got corrected in each POD) and concatenate all results in the post process of BO. we have to make sure this POD process does not break.


Karect
------
The following items must be checked by the reviewer every time there is a change in the Karect code.

We need to make sure karect works in both Verbose=0 and 1 modes.
Karect must work for executable & library before get released to Eureka,
both must give same results with same config settings
Filtering and qscore correction must work in karect
Segmentation must work


Eval Quality
------------
The following items must be checked by the reviewer every time there is a change in the eval_quality code.
Eval quality typically calls the function convert_bam_files_to_h5, within the file alignment_util.py. This will create h5 files in the read_aligners (_hp, _hp_qc, _hp_bo). This is non-intuitive and sometimes tricky logic to follow, but good to be aware of.
Eval quality is also used as part of the quality_training path, and the generation of predictor_alignments.h5. This is generated from predictor.h5 file from quality_caller and alignments.h5 from read_aligner_hp. The dimensions of these two files need to be compatible or this will fail.


Quality Trainer
---------------
The following items must be checked by the reviewer every time there is a change in the quality_trainer code.
As an intermediate result, the code should bring together all segment level predictor_alignments.h5 and merge them into a predictors_alignments_combo.h5.
The following five output files should be created, analysis_config.json,  model_analysis.json,  predictor_bins.json,  q_model_grids.h5,  &q_model.json.


EORR
----
The following items must be checked by the reviewer every time there is a change in the end_or_run_report.py code:

  * Did you add your new parameter to capture to the KEY_DICT; and is the aggregation value across segments correct.
  * This code loops over analyses, and within each analysis it loops over samples (for demux runs) and over the two paired end reads (for PE runs). Within each of these if loops over modules. If your new parameter is calculated from data within another module, or sub-section of the current module, did you capture it in the auxiliary_dict for later use?
  * Did you test that the code successfully can generate data for a G3 run, a G4 run, a demux run, and a PE run?


tensor_flow_model
-----------------
The following items must be checked by the reviewer every time there is a change in the tensor_flow_model code.

All curation/re_curation methods remain functional and can perform valid transformations. Inheritance and signatures match.
Signature and shape handoffs in tensor_flow_model.predict() are valid.
Shapes and signatures must be consistent with hp_trainer
New curation/recuration methods can be supported without changing the modified code.
TruncateKey can find the info and properly perform the truncation and remapping, in recurate methods.


tensor_flow_model_tf_2
----------------------
The following items must be checked by the reviewer every time there is a change in the tensor_flow_model_tf_2 code. Check tensor_flow_model inheritance is valid.

All curation/re_curation methods remain functional and can perform valid transformations.
Signature and shape handoffs in tensor_flow_model.predict() are valid.
Shapes and signatures must be consistent with hp_trainer around model prediction and data_curation.
New curation/re_curation methods can be supported without changing the modified code.
Networks/features
The following items must be checked by the reviewer every time there is a change in the networks/features code.
All methods accessing dataset classes are valid.
The feature should be compatible with all models using them, in case of a modification, compatibility should be verified.
Jumps.py does padding, ensuring any use of flow order respects the run and model.
Features that are tied to flow order or chip types should be handled appropriately.
TruncateKey should be feature 0, normalization should be before jumps, and jumps should come after. Jumps should be before other downstream features.

XYZ_invariant
-------------

The following items must be checked by the reviewer every time there is a change in the XYZ_invatiant code.
All curation/re_curation methods remain functional and can perform valid transformations.
Signature and shape handoffs in tensor_flow_model.predict() are valid.
Shapes and signatures must be consistent with hp_trainer around model prediction and data_curation.
New curation/recuration methods can be supported without changing the modified code.

XYZ
---
The following items must be checked by the reviewer every time there is a change in analysis/basecallers/networks/XYZ.py.
Make sure the input features are passed to the model in the same order as in the features_list in model config, their sizes should be correct and robust to changes in chip type, flow order length, protocol, etc.
Both training and testing using XYZ model should run with no error
Check if model_training_path/hp_trainer_tf2/model_diagram.png matches the expectation. This plot is only generated when training from scratch.

Hp_labeler
----------
The following items must be checked by the reviewer every time there is a change in hp_labeler.
Number of labels in summary.json shouldn’t be much smaller than baseline
Flows before alignment, correlation clipping and shearing at the beginning and end are handled properly
Large homopolymers that span multiple flows should be handled properly. For example, they should be distributed into the correct flows
Make sure the paths to Correct bed file is used to filter out sensors touching ambiguous regions. Exome runs should also use correct variants.json file to filter out sensors touching mutation regions. For example, if it’s a NA12878 run, it should use the variants.json file in NA12878 folder.
Data signatures saved in hp_labeler.h5 should be respected by data_collector
Check signal_distribution.png to make sure signals from different labels are in distinctive distributions.

Data Collector
--------------
The following items must be checked by the reviewer every time there is a change in data_collector.
Check hp_trainer_tf2 can load the data correctly into the correct signatures.
Check networks/features to make sure expected key-names are available.
Ensure the file paths are valid in the get_sample() method.
Ensure index selection from data collection results in accurate (one to one) mappings when adding new data. For example: selecting labeled sensors.

Hp_trainer_tf2
--------------

Signatures with data_collector are respected
Signatures with basecaller methods are respected.

Multinary
---------

The following items must be checked by the reviewer every time there is a change in multinary.
Multinary/separator_params/min_err_params config should be the same as binary_caller/min_err_params
Check if the basecalls and signal strengths make sense in aggregated_jumps_per_flow_per_class/Jumps_median_per_class.png
Check the number of sensors labeled as all zeros or all large numbers, it shouldn’t be much more than the baseline

Read Aligner
------------
The following items must be checked by the reviewer every time there is a change in read aligner, read aligner hp/qc/bo.

Number of reads aligned and error rates (total/mismatch/insertion/deletion) in alignment_error_plot_unfiltered.png are unchanged.
alignment_histograms.png is should be unchanged unless the code was to fix a bug.
Heatmap values in read_aligner_error_heatmap_unfiltered.png are unchanged.
The expected plots and csvs are all present (the list is a bit long but can be enumerated if it helps).
Only .bam and .bai alignment files are ever saved to disk, everything else must be streamed (.sam file generation is currently supported in special cases but we should phase this out). In general, we should avoid saving any intermediate files to disk that are able to be streamed as part of a pipeline.

Demux
-----

The following items must be checked by the reviewer every time there is a change in demux:
Manifest barcodes correspond to the number of samples and the correct sample config.
The order of samples read from the manifest is kept the same.
Different demuxers are inherited from the baseclass.
Predict API signature is kept consistent.
Confidence and distance score are meaningful metrics coming back from the demuxers. Distance score, the lower the better. Confidence between 0 and 1.
Abundance plots are generated per index and sample
Eval demux is functional and confusion matrices are showing proper information. Samples are not mixed or miss-assigned.

Quality_analyzer
----------------

The following items must be checked by the reviewer every time there is a change in the quality_analyzer.
Check if alignments.h5 is diff 0 (unless a change is expected).  If this file is diff 0, it is likely that all subsequent error plots / csv files are also diff 0.  Make sure alignments.h5 API is unchanged.
Creation of extended bam file is operational and valid.  If this is valid, check that all alignment metrics vs GC content figures are diff 0 (unless a change is expected)
Make sure after alignment.h5 file is created, bam/extended bam is not reopened again.  This should be done in one-shot when alignment.h5 is originally created.
Verify figures are created as expected

variant_caller_hp
-----------------

The following items must be checked by the reviewer every time there is a change in varinat_caller_hp:
Check files variant_caller_hp/variants_unfiltered_output.vcf, variant_caller_hp/variants_unfiltered_output_snp.vcf, and variant_caller_hp/variants_unfiltered_output_indel.vcf are created as expected.
If a new variant calling tool is added, a corresponding new static method should be added to run the new variant calling tool.

Variant_filter
--------------

The following items must be checked by the reviewer every time there is a change in varinat_filter:
Check files variant_filter/variants.sorted.normalized.filtered.vcf, variant_filter/snp_variants.sorted.normalized.filtered.vcf, and  variant_filter/indel_variants.sorted.normalized.filtered.vcf are created as expected.
If a new variant calling tool is added, a corresponding new static method should be added to filter the vcf file created by the new variant calling tool.
If comparing to ground truth is enabled, check figures variant_filter/compare_with_ground_truth_summary.png, variant_filter/compare_with_ground_truth_base_change.png, and variant_filter/compare_with_ground_truth_homopolymer.png are created as expected.
If creating summary report is enabled, check files variant_filter/sequencing_report.pdf, and variant_filter/sequencing_report_log_scale.pdf are created as expected.

Rna_seq
-------

The following items must be checked by the reviewer every time there is a change in rna_seq:
Check file rna_seq/rna_quant_unfiltered.csv is created as expected. If STAR is used as the rna seq tool, also check files rna_seq/results_binary_unfiltered.sorted.bam and rna_seq/results_binary_unfiltered.sorted.bam.bai are created as expected.
If a new rna seq tool is added, a corresponding new static method should be added to run the new rna seq tool.

Rna_seq_filter
--------------

The following items must be checked by the reviewer every time there is a change in rna_seq_filter:
Check file rna_seq_filter/rna_quant_filtered.csv is created as expected.
If comparing to ground truth is enabled, check figure rna_seq_filter/compare_to_ground_truth.png is created as expected.

Eval_Calls
----------
The following items must be checked by the reviewer every time there is a change in eval_calls:
Check indexes can accurately compare labels with basecalls
This module is inactive and this check list may not be complete.

Context_Generator
-----------------
The following items must be checked by the reviewer every time there is a change in CG:
Verify two paths of creating or copying sample folders
Verify sample folder for sign_filter, must have sign_filer.h5, plot_data.h5 and summary.json, also the post_process mean jump plots must be valid
hp_caller step of sample must have valid h5 file & fasta file
In case of quality_caller run before CG, sample QC must have both filtered and unfiltered fastq files, summary file and quality_caller.h5 file; also top level plots should be available for each sample
Any step, sign_filter, hp_caller, etc. for samples must be under correct sample and read


Paired_end_analysis
-------------------

The following items must be checked by the reviewer every time there is a change in paired_end_analysis:
Verify that the calculation of the sensor classification matrix is valid for all aligners (read_aligner, read_aligner_hp, read_aligner_hp_qc, read_aligner_hp_bo) and their PE/ joint alignments (ie., PE/read_aligner, PE/read_aligner_hp, PE/read_aligner_hp_qc, PE/read_aligner_hp_bo).
Spot check certain values and verify that they match the summary.json values from the read_aligners.  For example, aligned-aligned number in the classification matrix should match “n_sensors_aligned” in read_aligner, and aligned-aligned (joint) should match “n_reads_properly_paired” in read_aligner
Summary json keys are respected (EORR depends on these names)
Verify that EORR keys relating to PE/ are calculated correctly.  E.g., ra*_depth_percent_x_base_y calculations are relative to the number of common sensors in the fastq between R1 and R2.

Slide builder
-------------

The following items must be checked by the reviewer every time there is a change in paired_end_analysis:

  * Slide builder works fine for R1, R2, and PE
  * It can pull figures from different modules
  * Access to paths should be through data_path class and not a direct access

Umi_extractor
-------------

The following items must be checked by the reviewer every time there is a change in umi_extractor:

  * Check files umi_extractor/umi_extractor.fastq, umi_extractor/umi_extractor.h5 are created as expected.
  * Check plots are created as expected.

Read_grouper
------------

The following items must be checked by the reviewer every time there is a change in read_grouper:

  * Check files read_grouper/read_grouper.h5 are created as expected.
  * Check plots are created as expected.

Consensus_caller
----------------

The following items must be checked by the reviewer every time there is a change in read_grouper:
Check files consensus_caller/consensus_unfiltered.fastq and consensus_caller/variants_consensus_stats.h5 are created as expected.
Check consensus_caller/consensus_unfiltered_fastqc.html to see if the quality of the fastq file is expected.

Revision History
================

.. list-table::
   :header-rows: 1

   * - Author
     - Rev number
     - Date
     - Explanation
   * - Ali Nabi, Hooman Nezamfar, Eric LoPrete, David Todd
     - 0.1
     -
     - Initial draft with high level coding requirements, module owers, and example checklists for sign_filter, hp_caller, quality_caller
   * - Mohammad Fallahi, Bin Dong
     - 0.2
     - 02/18/2021
     - Added the secondary analysis steps
   * - David Todd
     - 0.3
     - 02/23/2021
     - Contributed to coding requirements. Added new module content incorporating input Ali N. and Ali M.
   * - David Todd
     - 0.4
     - 05/17/2021
     - Divided Links and Tips section into internal and external. Added links to Pull Request Submission and Test, Submodule information,  and Github  page into the new internal section.
   * - Mohammad Fallahi
     - 0.5
     - 08/08/21
     - Add ctDNA pipeline modules









