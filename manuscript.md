---
title: Flood Risk Prediction
keywords:
- Monthly Rainfall
- Flood Probability
- Prediction Model
- Climate Change
- Data Analysis
lang: en-US
date-meta: '2024-10-03'
author-meta:
- Shayan Bafandkar
- Sofia Frenk
- Supreme Pandey
- Brandy Diggs-McGee
header-includes: |
  <!--
  Manubot generated metadata rendered from header-includes-template.html.
  Suggest improvements at https://github.com/manubot/manubot/blob/main/manubot/process/header-includes-template.html
  -->
  <meta name="dc.format" content="text/html" />
  <meta property="og:type" content="article" />
  <meta name="dc.title" content="Flood Risk Prediction" />
  <meta name="citation_title" content="Flood Risk Prediction" />
  <meta property="og:title" content="Flood Risk Prediction" />
  <meta property="twitter:title" content="Flood Risk Prediction" />
  <meta name="dc.date" content="2024-10-03" />
  <meta name="citation_publication_date" content="2024-10-03" />
  <meta property="article:published_time" content="2024-10-03" />
  <meta name="dc.modified" content="2024-10-03T18:49:34+00:00" />
  <meta property="article:modified_time" content="2024-10-03T18:49:34+00:00" />
  <meta name="dc.language" content="en-US" />
  <meta name="citation_language" content="en-US" />
  <meta name="dc.relation.ispartof" content="Manubot" />
  <meta name="dc.publisher" content="Manubot" />
  <meta name="citation_journal_title" content="Manubot" />
  <meta name="citation_technical_report_institution" content="Manubot" />
  <meta name="citation_author" content="Shayan Bafandkar" />
  <meta name="citation_author_institution" content="Department of Civil &amp; Environmental Engineering, University of Illinois Urbana-Champaign" />
  <meta name="citation_author_orcid" content="0009-0009-8172-5751" />
  <meta name="citation_author" content="Sofia Frenk" />
  <meta name="citation_author_institution" content="Department of Civil &amp; Environmental Engineering, University of Illinois Urbana-Champaign" />
  <meta name="citation_author_orcid" content="0009-0001-8099-4900" />
  <meta name="citation_author" content="Supreme Pandey" />
  <meta name="citation_author_institution" content="Department of Civil and Environmental Engineering, University of illinois Urbana-Champaign" />
  <meta name="citation_author_orcid" content="0000-0003-0775-6313" />
  <meta name="citation_author" content="Brandy Diggs-McGee" />
  <meta name="citation_author_institution" content="Department of Civil &amp; Environmental Engineering, University of Illinois Urbana-Champaign" />
  <meta name="citation_author_institution" content="USACE ERDC CERL" />
  <meta name="citation_author_orcid" content="0000-0003-2052-0946" />
  <link rel="canonical" href="https://uiceds.github.io/project-triples/" />
  <meta property="og:url" content="https://uiceds.github.io/project-triples/" />
  <meta property="twitter:url" content="https://uiceds.github.io/project-triples/" />
  <meta name="citation_fulltext_html_url" content="https://uiceds.github.io/project-triples/" />
  <meta name="citation_pdf_url" content="https://uiceds.github.io/project-triples/manuscript.pdf" />
  <link rel="alternate" type="application/pdf" href="https://uiceds.github.io/project-triples/manuscript.pdf" />
  <link rel="alternate" type="text/html" href="https://uiceds.github.io/project-triples/v/084fd6fb289e9f17ee510140a0c5b91e5b1e4f9b/" />
  <meta name="manubot_html_url_versioned" content="https://uiceds.github.io/project-triples/v/084fd6fb289e9f17ee510140a0c5b91e5b1e4f9b/" />
  <meta name="manubot_pdf_url_versioned" content="https://uiceds.github.io/project-triples/v/084fd6fb289e9f17ee510140a0c5b91e5b1e4f9b/manuscript.pdf" />
  <meta property="og:type" content="article" />
  <meta property="twitter:card" content="summary_large_image" />
  <link rel="icon" type="image/png" sizes="192x192" href="https://manubot.org/favicon-192x192.png" />
  <link rel="mask-icon" href="https://manubot.org/safari-pinned-tab.svg" color="#ad1457" />
  <meta name="theme-color" content="#ad1457" />
  <!-- end Manubot generated metadata -->
bibliography:
- content/manual-references.json
manubot-output-bibliography: output/references.json
manubot-output-citekeys: output/citations.tsv
manubot-requests-cache-path: ci/cache/requests-cache
manubot-clear-requests-cache: false
...






<small><em>
This manuscript
([permalink](https://uiceds.github.io/project-triples/v/084fd6fb289e9f17ee510140a0c5b91e5b1e4f9b/))
was automatically generated
from [uiceds/project-triples@084fd6f](https://github.com/uiceds/project-triples/tree/084fd6fb289e9f17ee510140a0c5b91e5b1e4f9b)
on October 3, 2024.
</em></small>



## Authors



+ **Shayan Bafandkar**
  <br>
    ![ORCID icon](images/orcid.svg){.inline_icon width=16 height=16}
    [0009-0009-8172-5751](https://orcid.org/0009-0009-8172-5751)
    · ![GitHub icon](images/github.svg){.inline_icon width=16 height=16}
    [sbafan](https://github.com/sbafan)
    <br>
  <small>
     Department of Civil & Environmental Engineering, University of Illinois Urbana-Champaign
  </small>

+ **Sofia Frenk**
  ^[✉](#correspondence)^<br>
    ![ORCID icon](images/orcid.svg){.inline_icon width=16 height=16}
    [0009-0001-8099-4900](https://orcid.org/0009-0001-8099-4900)
    · ![GitHub icon](images/github.svg){.inline_icon width=16 height=16}
    [sofia-frenk](https://github.com/sofia-frenk)
    <br>
  <small>
     Department of Civil & Environmental Engineering, University of Illinois Urbana-Champaign
  </small>

+ **Supreme Pandey**
  <br>
    ![ORCID icon](images/orcid.svg){.inline_icon width=16 height=16}
    [0000-0003-0775-6313](https://orcid.org/0000-0003-0775-6313)
    · ![GitHub icon](images/github.svg){.inline_icon width=16 height=16}
    [supremepandey](https://github.com/supremepandey)
    <br>
  <small>
     Department of Civil and Environmental Engineering, University of illinois Urbana-Champaign
  </small>

+ **Brandy Diggs-McGee**
  <br>
    ![ORCID icon](images/orcid.svg){.inline_icon width=16 height=16}
    [0000-0003-2052-0946](https://orcid.org/0000-0003-2052-0946)
    · ![GitHub icon](images/github.svg){.inline_icon width=16 height=16}
    [iloveheat](https://github.com/iloveheat)
    <br>
  <small>
     Department of Civil & Environmental Engineering, University of Illinois Urbana-Champaign; USACE ERDC CERL
  </small>


::: {#correspondence}
✉ — Correspondence possible via [GitHub Issues](https://github.com/uiceds/project-triples/issues)
or email to
Sofia Frenk \<sofiaf6@illinois.edu\>.


:::


## Abstract
Our project aims to develop a machine learning model in Julia to predict the likelihood of floods based on the monthly and annual rainfall in Kerala, a flood-prone subdivision in India. Leveraging a publicly available dataset, we will analyze historical rainfall patterns and develop a robust regression model to estimate flood probabilities. This model has the potential to be a valuable tool for for policymakers, disaster management authorities, and local communities, providing timely insights to improve flood preparedness and mitigation strategies.
The motivation behind this project lies in the increasing frequency and severity of floods, exacerbated by climate change and rapid urbanization. Kerala, in particular, has experienced devastating floods in recent years, making accurate flood prediction models critical for risk management. Our machine learning approach will incorporate rainfall data and the use of advanced regression techniques, allowing for a flexible and reliable flood forecasting tool.
Employing machine learning techniques, we aim to develop a model that can adapt to changing weather patterns, offering a flexible and reliable flood forecasting tool. Ultimately, our aim is to contribute to the development of more effective flood prediction and management systems, minimizing the human, infrastructural, and environmental losses caused by floods.


## Dataset Description 
  - Source: 
  This dataset can be found on Kaggle, at this link: https://www.kaggle.com/code/mukulthakur177/flood-prediction-model. 
  It was generated to help build a predictive model for flood occurrences using meteorological and environmental factors.
  - Format: The dataset is in CSV format, which is commonly used for tabular data storage. Each row represents a specific data point, with columns detailing various features that might impact flood conditions.
  - Contents: 
    The columns of the dataset cover parameters typically used to forecast flood situations, and the dataset serves as a basis for training machine learning models in flood prediction.
    More specifically, the dataset includes the following columns:
    1) Monthly Rainfall (mm): Represents the amount of rainfall in millimeters. This is a key factor in flood prediction models.
    2) Yearly Rainfall (mm): Represents the total amount of rainfall in a year in millimeters, ie, a summation of all monthly rainfall.
    3) Flood (0/1): A binary indicator where '0' signifies no flood, and '1' indicates a flood event.

## Proposal
Our team plans to use the Kaggle flood prediction dataset to develop a machine learning model in Julia that predicts the likelihood of floods in Kerala, India. 
We will analyze the historical monthly rainfall, total annual rainfall, and ocurrance of flooding (boolean yes/no) data in the dataset to identify patterns correlated with flood occurrences. 
By applying regression techniques, we aim to create a model that estimates flood probabilities accurately, providing a valuable tool for disaster management authorities and local communities.

The motivation behind this project stems from the increasing frequency of floods due to climate change, particularly in Kerala. 
Accurate prediction models are crucial for improving flood preparedness and risk mitigation strategies. 
Our model will offer timely insights, ultimately contributing to reducing the human, infrastructural, and environmental losses caused by floods in this region.

## References {.page_break_before}

<!-- Explicitly insert bibliography here -->
<div id="refs"></div>

