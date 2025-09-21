Data Dictionary: Permanent National Employment Survey (EPEN)
Objective: This document serves as a guide for processing and analyzing the EPEN data. It is intended for a programming agent to correctly interpret each variable and handle the null values that arise from the survey's design.

Key Note on Nulls: The survey contains branching. This means that the answer to one question determines which questions will be asked next. Therefore, many columns will have legitimate null values because the respondent did not go through that question path. These are not errors, but rather "not applicable" data.

Module 1: Household Identification and Characteristics (Columns ANIO to C208)
These columns uniquely identify each record and describe basic demographic characteristics. They should not have nulls, except for age if it was not declared.

ANIO, MES: Year and Month of the survey.

CONGLOMERADO, MUESTRA, SELVIV, HOGAR: Geographic and housing identifiers.

REGION: Location (1: Lima Metropolitana, 2: Rest of urban, 3: Rural).

LLAVE_PANEL: Unique ID for tracking the person over time.

ESTRATO: Geographic stratum according to population size.

C201: Unique code for the person within the household.

C203: Relationship to the head of the household.

C204, C205, C206: Residency status and presence in the household.

C207: Sex (1: Male, 2: Female).

C208: Age in completed years. Important! The employment module only applies to people with C208 >= 14.

Module 2: Employment and Activity Status (Columns C300n onwards)
This is the main module and contains most of the branching.

2.1 - Main Filter Questions (Branching)
C303: Did you work last week?

Function: This is the most important branch. It separates the population into two major flows.

If the answer is "Yes" (1): The person is EMPLOYED. They are asked the questions in the block from C308 to C350 (occupation, income, hours, etc.).

If the answer is "No" (2): The person DID NOT WORK. The entire employed block is skipped, and questions C304 and C305 are asked next.

C304 / C305: Do you have a job/business to return to?

Function: Identifies the "employed but absent." Applies only if C303 is "No."

If the answer is "Yes" (1) to either: The person is considered EMPLOYED and is asked the questions from the employed block.

If the answer is "No" (2) to both: The person does not have an active employment relationship. They proceed to the next filter.

C352: Did you do anything to look for a job last week?

Function: Separates the UNEMPLOYED from the INACTIVE. Applies only to those who are not employed.

If the answer is "Yes" (1): The person is UNEMPLOYED. They are asked the questions in the block from C353 to C358 (job search).

If the answer is "No" (2): The person is INACTIVE (student, retiree, etc.). They are asked for the reason (C356).

2.2 - Conditional Question Blocks
EMPLOYED Block (C308_COD to C350):

Purpose: Details the characteristics of the job (occupation, economic sector, hours, income, etc.).

Condition for Nulls: ALL of these columns will be null if the person is not classified as "Employed" according to filters C303, C304, and C305.

UNEMPLOYED Block (C353 to C358):

Purpose: Inquires about the job search (what was done, how long they have been looking).

Condition for Nulls: ALL of these columns will be null if the person is "Employed" or "Inactive."

PREVIOUS JOB Block (C359 onwards):

Purpose: Asks about previous work experience.

Condition for Nulls: Applies only to the unemployed and inactive. It will be null for the employed.

Module 3: Insurance, Education, and Others
3.1 - Branching in Insurance and Pensions
C361_1 to C361_8: Are you affiliated with [type of health insurance]?

Function: These are checkbox-style questions.

Branch: If the answer to C361_X is "Yes," the question C362_X (who contributes?) is activated. If "No," C362_X will be null.

C364_1 to C364_4: Are you affiliated with [pension system]?

Function: Similar to the above.

Branch: If the answer to C364_X is "Yes," the question C365_X is activated. If "No," C365_X will be null.

3.2 - Descriptive Columns
C366: Highest level of education completed.

C375_1 to C375_6: Presence of permanent limitations (disability).

C376: Mother tongue learned in childhood.

C377: Ethnic self-identification.

Module 4: Calculated Variables and Expansion Factor
OCUP300: A summary variable that classifies the person (Employed, Unemployed, Inactive). It is a key indicator.

I339_1, D341_T, ... INGTOT, INGTOTP, INGTRABW: These are income variables, either reported or calculated/monthly-adjusted.

RESIDENT: Indicates if the person is a usual resident of the household.

fa_efm24 (and similar): Quarterly Expansion Factor.

Purpose: It is a weight that allows the sample results to be representative of the entire population.

Important! Each quarterly file has its own factor. When joining datasets, this factor must be handled and adjusted correctly. Data should never be analyzed without applying this factor to draw population-level conclusions.
