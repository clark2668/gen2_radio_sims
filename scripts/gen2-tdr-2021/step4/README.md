There are two versions of all the step 4 files.

For example, step4_job.sub, and step4_job_standardized.sub

The latter is designed to generate a json file for each energy and zenith bin.
Which can then be merged.

Note also: the standard version "cleverly" creates json files full of zeros 
(with the dummy.json file as a template), so that the result of the merging
always has the right number of energy and zenith bins, regardless of
if a file was missing or empty.



