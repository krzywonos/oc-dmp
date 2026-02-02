# General information
OC-DMP (Open Citations - Data Management Plan) is a generator of University of Bologna-compliant Data Management Plans for the OpenCitations research group.
The script was made as a project for the Open Science class at University of Bologna, Academic Year 2024/25.

### Running the script using CLI

python script.py --data data

The --data flag is used to specify a subfolder for the input data, without it the script will look for it in the same folder it is located in.

### Protocol

Protocol available at:

https://www.protocols.io/view/open-science-24-25-hubert-v2-hhqab35sf

# Filling the input data

## Example files
A folder *example_input* with example input files has been made available.

### Markdown files

Markdown files are loaded into the final document using the markdown package.
For more information on how Markdown works: https://daringfireball.net/projects/markdown/syntax
For the list of differences between Markdown and markdown package: https://python-markdown.github.io/#differences

### general_data.xlsx
The script creates <\h3> headers for the final document based on the cells in column A.

The consequent cells in the same row serve as values for <\p> paragraphs that are entered below the corresponding headers.

An exception is the row starting with the cell "Title of DMP". There, the first cell is used to fill the title of the final HTML document.

Fields accept natural language as input, except if specified otherwise. The following list contain the fields and their meanings:
- *Title of DMP* - Title of the Data Management Plan
- *Description* - Brief description of the Data Management Plan
- *Language* - The language of the Data Management Plan
- *Contact* - Contact information of the person responsible for the Data Management Plan
- *Researchers* - Names of people, that have produced, processed and/or analysed the research output described in the Data Management Plan
- *Organisations* - Names of organisations contributing to the creation and revision of the Data Management Plan
- *Funding organisations* - Names of organisation providing funding towards the research output described in the Data Management Plan
- *Grants* - Information about grants given towards the research output provided in the Data Management Plan
- *Project* - Information about the project the research output is a part of
- *Access Rights* - Information regarding the access of the Data Management Plan on Zenodo
- *Licence* - Information about the licence of the Data Management Plan.

### data_table.xlsx
The main data sheet is currently locked with the password "123" to avoid inputting the data in the columns that represent headings, which serve only for organisational reasons.

After unlocking the main data sheet, text can be used in the columns under these headings to provide additional information, if necessary.

Headers for the subsections of the final HTML are taken from the cells in the first row of the spreadsheet. The numbering is removed for readability reasons.

Each row corresponds to a research output. The first cell is the name of the research output. The corresponding cells in the same row represent paragraphs that will be used as paragraphs under the headings specified in the first row.

If a cell displays a value *N/A*, the subsection is entirely omitted from the final document.

There are cells where the user may choose to input *N/A* manually, this will omit the subsection from being included in the final document.

Cells may contain selectors for Yes/No values or Dataset/Software/Object values. The user may choose to manually input a different value, but it will result in conditional colour formatting of the cells to behave improperly.

Cells may contain formulas to automatically input *N/A* where applicable (e.g. if a research output is selected as a Dataset in subsection 1.3.2., then the cells in the subsection 2.3., 2.4., 2.5. and 2.6. will be automatically set to *N/A*). The user should overwrite the formulas in the applicable rows only, but may choose to overwrite them in other cells, where it will result in conditional colour formatting of the cells to behave improperly.

The following list contain the fields, their meaning, their accepted values (if applicable), if they are selector or formula cells; and if they are locked for the purposes of the final document generation:

- *1.* Your research output - locked.
- *1.1.* Contact details and responsibilities - locked.
- *1.1.1.* Contact person(s) - Contact information of the person or people responsible for the Data Management Plan of the research output. Accepts a list of people (Surname, Name \[pid:0123\]) separated by semicolons.
- *1.1.2.* Is the contact person also the research output creator - selector cell - Yes if the contact person is one of the research output creators, No otherwise.
- *1.1.3.* Research output creator(s) and contributor(s) - List of all people who have contributed towards the creation of the research output. Accepts a list of people (Surname, Name \[pid:0123\]) separated by semicolons.
- *1.1.4.* Institution(s) involved - List of all institutions involved in the creation of the research output. Accepts a list of institutions (Institution Name \[pid:0123\]) separated by semicolons.
- *1.2.* Resources for data management - locked.
- *1.2.1.* What resources will be dedicated to data management and ensuring that data will be FAIR? - Information regarding the resources dedicated to management and FAIR-ensurement of data.
- *1.3.* Identifying the research output - locked. 
- *1.3.1.* Work package and task number - Work package and task number of the research output.
- *1.3.2.* Which type of research output are you describing - Selector cell of dataset/software/object. Custom input is accepted, but the cells in the columns of section 2 have to be formatted manually.
- *2.* Summary - locked.
- *2.1.* Identification of the dataset - locked.
- *2.1.1.* Are you re-using an already existing dataset? - Selector cell - Yes if the dataset has existed before, No otherwise.
- *2.1.2.* Re-using an existing dataset: why and how - Formula cell - Explanation for and description of the re-use of an existing dataset.
- *2.1.3.* Creating a new dataset - Selector cell - Yes if the dataset is created as part of the research, No otherwise.
- *2.2.* Dataset characteristics - locked.
- *2.2.1.* Dataset name - Formula cell - Name of the dataset provided as part of the research output.
- *2.2.2.* Data types - Formula cell - Types of data provided as part of the research output.
- *2.2.3.* Data formats - Formula cell - Formats of data provided as part of the research output.
- *2.2.4.* Size of data - Formula cell - Compressed and uncompressed sizes on a storage drive of data provided as part of the research output.
- *2.2.5.* How is the data generated/collected - Formula cell - Information on the generation/collection of data provided as part of the research output.
- *2.2.6.* Why is the data generated/collected - Formula cell - Rationale for the generation/collection of data provided as part of the research output.
- *2.2.7.* Dataset description - Formula cell - Other information relating to the data provided as the research output that has not been described in the previous subsection.
- *2.3.* Identification of software - locked.
- *2.3.1.* Are you re-using already existing software - Selector cell - Yes if the software has existed before, No otherwise.
- *2.3.2.* Re-using existing software: why and how - Formula cell - Explanation for and description of the re-use of an existing software.
- *2.3.3.* Creating new software - Selector cell - Yes if the software is created as part of the research, No otherwise.
- *2.4.* Software characteristics - locked.
- *2.4.1.* Software name - Formula cell - Name of the software provided as part of the research output.
- *2.4.2.* Type of software - Formula cell - Type of software provided as part of the research output.
- *2.4.3.* Software formats - Formula cell - Formats of software provided as part of the research output.
- *2.4.4.* Size of software - Formula cell - Compressed and uncompressed sizes on a storage drive of software provided as part of the research output.
- *2.4.5.* How is software created/used - Formula cell - Information on the creation/use of software provided as part of the research output.
- *2.4.6.* Why is software created/used - Formula cell - Rationale for the creation/use of software provided as part of the research output.
- *2.4.7.* Software description - Formula cell - Other information relating to the software provided as the research output that has not been described in the previous subsection.
- *2.5.* Identification of a non-digital object - locked.
- *2.5.1.* Are you re-using an already existing object? - Selector cell - Yes if the object has existed before, No otherwise.
- *2.5.2.* Re-using an existing object: why and how - Formula cell - Explanation for and the description of the re-use of an existing object.
- *2.5.3.* Creating a new object - Selector cell - Yes if the object is created as part of the research, No otherwise.
- *2.6.* Non-digital object characteristics - locked.
- *2.6.1.* Object name - Formula cell - Name of the object provided as part of the research output.
- *2.6.2.* Type of object - Formula cell - Type of the object provided as part of the research output.
- *2.6.3.* How is the object created/used - Formula cell - Information on the creation/use of object provided as part of the research output.
- *2.6.4.* Why is the object created/used - Formula cell - Rationale for the creation/use of object provided as part of the research output.
- *3.* Ethics - locked.
- *3.1.* Personal data - locked.
- *3.1.1.* Are you handling personal data? - Selector cell - Yes if the research output has made use of personal data, No otherwise.
- *3.1.2.* Solutions adopted for handling personal data - Formula cell - Description of solutions used for handling and anonymising personal information used to create the research output.
- *3.2.* Legal aspects - locked.
- *3.2.1.* Are there any legal issues associated to your output (e.g. IPR or valorisation)? - Selector cell - Yes if there are legal issues associated to the research output, No otherwise.
- *3.2.2.* Legal issues: description and solutions - Formula cell - Description of the legal issues associated to the research output and solutions for their accommodation and mitigation.
- *3.3.* Other ethical aspects - locked.
- *3.3.1.* Are there other ethical issues associated to your output? - Selector cell - Yes if there are other ethical issues associated to the research output, No otherwise.
- *3.3.2.* Ethical issues: description and solutions - Formula cell - Description of the ethical issues associated to the research output and solutions for their accommodation and mitigation.
- *4.* Making research FAIR - locked.
- *4.1.* Long-term preservation - locked.
- *4.1.1.* Selecting what to preserve - Rationale on the selection of data/code/other things selected to be preserved as part of the research output.
- *4.1.2.* Chosen repository/ies - Repositories for the files/objects made as the research output.
- *4.1.3.* Further information on long-term preservation strategy - Other information on long-term preservation strategy of the research output.
- *4.2.* Findability - locked.
- *4.2.1.* Persistent identifier(s) - Persistent identifiers of the dataset/software/other object made as part of the research output.
- *4.2.2.* Metadata - Information on the metadata of the dataset/software/other object made as part of the research output.
- *4.2.3.* Keywords - Keywords used to facilitate searching for the dataset/software/other object made as part of the research output. Accepts a list of keywords separated by semicolons.
- *4.3.* Accessibility - locked.
- *4.3.1.* Is the research output openly accessible? - Selector cell - Yes if the research output has been made openly accessible, No otherwise.
- *4.3.2.* Controlled access - Selector and formula cell - Yes if the access to the research output is controlled, No otherwise.
- *4.3.3.* Accessing the research output - Information on how to access the research output.
- *4.3.4.* Is metadata openly accessible? - Selector cell - Yes if metadata of the research output is openly accessible, No otherwise.
- *4.3.5.* Accessing metadata - Information on how to access the research output.
- *4.4.* Interoperability - locked.
- *4.4.1.* Methodologies - Methodologies used to produce the research output.
- *4.4.2.* Vocabularies, taxonomies and other standards - Vocabularies, taxonomies and other standards used to produce the research output.
- *4.5.* Reusability - locked.
- *4.5.1.* Licencing - Licence of the research output.
- *4.5.2.* Documentation - Link to the documentation of the research output.
- *5.* Quality and security - locked.
- *5.1.* Quality of the research output - locked.
- *5.1.1.* Measures implemented to ensure quality - Information on quality assurance of the research output.
- *5.2.* Security measures - locked.
- *5.2.1.* Storage - Information on the primary storage of the research output.
- *5.2.2.* Backup - Information on the secondary storage of the research output
- *5.2.3.* Additional security - Information on the additional security of the research output.