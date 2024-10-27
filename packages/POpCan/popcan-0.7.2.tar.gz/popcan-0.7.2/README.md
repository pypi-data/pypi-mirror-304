[![License](https://img.shields.io/badge/License-BSD\%202--Clause-orange.svg)](https://opensource.org/licenses/BSD-2-Clause)

# POpCan

Tool for analysing the extent of overlap between various cancers including user-defined sub categories.

**Input File Pre-requisites**
* The input file should be a .csv file with "specific" column headers as a combination of 3 words separated by the character "_".
* 1 word for the main category and 2 words for subsequent sub-categories.
* The absence of sub-categories is accounted for in the calculations. Hence, if there are no sub-categories that the user wishes to specify, this can be replaced with a space between the character "_"

**Column Header Example**
* Main-category: A 4-letter acronym (such as 'STAD' for Stomach Adenocarcinoma). The length of the 4-letter acronym cannot be changed, but, it can be replaced with an equivalent 4-letter acronym as per user requirement for any other cancer type or disease type.
* First subcategory: Can be stage or a different user-defined variable (Ex. STAD_StageI).
* Second subcategory: Can be gene expression pattern or a different user-defined variable (Ex. STAD_StageI_Downregulated).
* If sub-categories were to be absent in the above example; STAD_StageI_Downregulated would be replaced with STAD_[Empty space]_[Empty space]

**Available Parameters**
* Input_Path : [string] path to the input file
* Condition : [string] either 'Between' or 'Within'. Between will find overlap only between two or more cancer types / disease conditions including their sub-categories but not for sub-categories within the same cancer type / disease condition. Within will compare the overlap between the sub-categories of same cancer type / disease condition as well.
* Output_Path : [string] path to the output file

**Output Files**
* Reports the extent of overlap as a percentage, the number of entries that overlap and the entries that overlap.

**Installation**
```
pip install POpCan
```

**Use Case**
```
#=============================Example===========================#
from POpCan import load_example_data_path, get_output_path, Find_Overlap
example_data = load_example_data_path()         #Input Path to Example File
example_output = get_output_path()              #Output Path to Example Output, Saves the output into Downloads directory


#Find_Overlap(Path_to_InputFile, "Between", Path_to_OutputFile)
Find_Overlap(example_data, "Between", example_output)
```

COPYRIGHT

Copyright (c) 2024, Pravallika Govada All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

CONTACT INFORMATION

Please address any queries or bug reports to Pravallika Govada at pravallika.govada2018@vitstudent.ac.in or pravallika2606g@gmail.com
