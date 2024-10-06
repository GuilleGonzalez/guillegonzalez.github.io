---
layout: default
title: Guillermo Gonzalez
date: 2024-05-30
author: Guillermo Gonzalez
description: Miscellaneous
---

# Certificates

Major:
- The <a href="https://www.coursera.org/professional-certificates/google-data-analytics" target="_blank">Google Data Analytics</a> Professional Certificate (<a href="https://www.coursera.org/account/accomplishments/professional-cert/6TRB876HY9VJ" target="_blank">My Certificate</a>)
- The <a href="https://www.coursera.org/specializations/machine-learning-introduction?" target="_blank">Machine Learning Specialization</a> by Stanford & DeepLearning.AI (<a href="https://www.coursera.org/account/accomplishments/specialization/ZYMFKE6U9UEF" target="_blank">My Certificate</a>)
- <a href="https://www.edx.org/learn/computer-science/harvard-university-cs50-s-introduction-to-computer-science" target="_blank">CS50</a> by Harvard University (<a href="https://cs50.harvard.edu/certificates/57f1fa00-9a0e-4b83-92ee-461b1ce3c93e" target="_blank">My Certificate</a>)  
- <a href="https://www.edx.org/learn/python/harvard-university-cs50-s-introduction-to-programming-with-python" target="_blank">CS50 Python</a>, CS50's Little Brother (<a href="https://certificates.cs50.io/7710c4f9-d379-434d-8f13-c4f07a705eee.pdf?size=letter" target="_blank">My Certificate</a>)

Miscellaneous:
- <a href="https://www.coursera.org/learn/learning-how-to-learn" target="_blank">Learning How to Learn</a> by Deep Teaching Solutions (<a href="https://www.coursera.org/account/accomplishments/verify/SUNAUPYDWGTY" target="_blank">My Certificate</a>)
- <a href="https://www.coursera.org/learn/the-science-of-well-being" target="_blank">The Science of Well Being</a> by Yale (<a href="https://www.coursera.org/account/accomplishments/verify/NL9NJMKB3F36" target="_blank">My Certificate</a>)
- <a href="https://www.coursera.org/learn/machine-learning-with-python?" target="_blank">Machine Learning with Python</a> by IBM (<a href="https://www.coursera.org/account/accomplishments/verify/5ZDBQVP42CGN" target="_blank">My Certificate</a>)
- <a href="https://www.coursera.org/learn/building-deep-learning-models-with-tensorflow?" target="_blank">Building Deep Learning Models with Tensorflow</a> by IBM (<a href="https://www.coursera.org/account/accomplishments/verify/ZGPJ4KAW5396" target="_blank">My Certificate</a>)

Part of the <a href="https://www.coursera.org/specializations/machine-learning-introduction?" target="_blank">Machine Learning Specialization</a>: 

1. <a href="https://www.coursera.org/learn/machine-learning?" target="_blank">Supervised Learning</a> (<a href="https://www.coursera.org/account/accomplishments/verify/F3LK5Z3Q5VBJ" target="_blank">My Certificate</a>)
2. <a href="https://www.coursera.org/learn/advanced-learning-algorithms?" target="_blank">Advanced Learning Algorithms</a> (<a href="https://www.coursera.org/account/accomplishments/verify/HPCZF6UNLNLT" target="_blank">My Certificate</a>)
3. <a href="https://www.coursera.org/learn/unsupervised-learning-recommenders-reinforcement-learning?" target="_blank">Unsupervised Learning</a> (<a href="https://www.coursera.org/account/accomplishments/verify/3DXHFP4S69YB" target="_blank">My Certificate</a>)

Part of the <a href="https://www.coursera.org/professional-certificates/google-data-analytics?" target="_blank">Google Data Analytics</a> Professional Certificate: 

1. <a href="https://www.coursera.org/learn/foundations-data?" target="_blank">Foundations: Data, Data, Everywhere</a> - Foundations (<a href="https://www.coursera.org/account/accomplishments/verify/RY38EVZAUAVU" target="_blank">My Certificate</a>)
2. <a href="https://www.coursera.org/learn/ask-questions-make-decisions?" target="_blank">Ask Questions to Make Data-Driven Decisions</a> - Ask (<a href="https://www.coursera.org/account/accomplishments/verify/5EHN2EB33CXW" target="_blank">My Certificate</a>)
3. <a href="https://www.coursera.org/learn/data-preparation?" target="_blank">Prepare Data for Exploration</a> - Prepare (<a href="https://www.coursera.org/account/accomplishments/verify/33SQCWNH86GP" target="_blank">My Certificate</a>)
4. <a href="https://www.coursera.org/learn/process-data?" target="_blank">Process Data from Dirty to Clean</a> - Process (<a href="https://www.coursera.org/account/accomplishments/verify/FD57HW7UMHNG" target="_blank">My Certificate</a>)
5. <a href="https://www.coursera.org/learn/analyze-data?" target="_blank">Analyze Data to Answer Questions</a> - Analyze (<a href="https://www.coursera.org/account/accomplishments/verify/VF2NDDVSVYE9" target="_blank">My Certificate</a>)
6. <a href="https://www.coursera.org/learn/visualize-data?" target="_blank">Share Data Through the Art of Visualization</a> - Share (<a href="https://www.coursera.org/account/accomplishments/verify/SZR5V5LZECV4" target="_blank">My Certificate</a>)
7. <a href="https://www.coursera.org/learn/data-analysis-r?" target="_blank">Data Analysis with R Programming</a> - Act (<a href="https://www.coursera.org/account/accomplishments/verify/WJFEXPLBDFN2" target="_blank">My Certificate</a>)
8. <a href="https://www.coursera.org/learn/google-data-analytics-capstone?" target="_blank">Google Data Analytics Capstone</a> - Capstone (<a href="https://www.coursera.org/account/accomplishments/verify/MH2MRKYMMGAG" target="_blank">My Certificate</a>)

<br>
<br>

---

Title: WebPage Jekyll Naming Notes

# Customizing WebPage Titles for Markdown GitHub Pages (Jekyll)

To exclude the default top link header and take full control of your web page title:

Set your chosen title in both the head of the Markdown files and the `_config.yml`. Ensure that the title is exactly the same in both locations and that your GitHub Repository has **No** descrption.

As the top metadata of your Markdown Files:
```
---
title: ExampleTitle
---
```
In your `_config.yml` file:
```
title: ExampleTitle
```
*For both, replace "ExampleTitle" with your own chosen title (spaces are allowed).*

---

### Info:

The default "project_name" is the GitHub repository's name. You can modify "project_name" in `_config.yml` using the "title" keyword.

The "sub_name" is derived from the Markdown file's "title" metadata property, if present. If not present, "sub_name" defaults to the first h1 or h2 heading on the Markdown page. If neither a h1 nor a h2 is found, "sub_name" is not included in the title.

#### General Format:

- "{sub_name} | {project_name}" when "sub_name" exists and is different than "project_name".
- "{project_name} | {repo_description}" when the current GitHub repository has a description, and when there is no "sub_name" or when "sub_name" is the same as "project_name."
- "{project_name}" in the specific case where the GitHub repository has no description, and when there is no "sub_name" or when "sub_name" is the same as "project_name." This is also the only case where their will not be the link header at the top of the page.

**Note:** Regular content, repository commit messages, markdown metadata descriptions, and yml description do not impact the page's title.

**Disclaimer:** These are just my findings as of 11/24/2023. I did not test every possible case nor do I know how long this method will work. - But trying this is worth a shot as I have spent many hours trying to figure it all out.