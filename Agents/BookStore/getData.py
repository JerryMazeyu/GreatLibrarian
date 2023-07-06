from Utils import soft_mkdir, join, os
import pandas as pd


def extract_journal_information(text, subject, subsubject):
    """Extract information from the website https://www.jstor.org/journal/

    Args:
        text (str): Text copied from the website
        subject (str): Subject of the journal, e.g. "Area Studies"
        subsubject (str): Sub subject of the journal, e.g. "African American Studies"
    """
    res = {"TITLE": "", "PUBLISHED BY": "", "COVERAGE": "", "MOVING WALL": "", "ISSN":"", "EISSN": "", "SUBJECTS": "", "COLLECTIONS": "", "ABSTRACT": ""}
    sentences = text.split('\n')
    max_len = 0
    abstract = ''
    for (ind, content) in enumerate(sentences):
        if len(content) > max_len:
            max_len = len(content)
            abstract = content
        if content == 'Support':
            res["TITLE"] = sentences[ind+1]
        if content == 'PUBLISHED BY':
            res["PUBLISHED BY"] = sentences[ind+1]
        if content == 'COVERAGE':
            res["COVERAGE"] = sentences[ind+1]
        if content == 'MOVING WALL':
            res["MOVING WALL"] = sentences[ind+1]
        if content == 'ISSN':
            res["ISSN"] = sentences[ind+1]
        if content == 'EISSN':
            res["EISSN"] = sentences[ind+1]
        if content == 'SUBJECTS':
            res["SUBJECTS"] = sentences[ind+1] 
        if content == 'COLLECTIONS':
            res["COLLECTIONS"] = sentences[ind+1]   
        
        res["ABSTRACT"] = abstract
    return res



if __name__ == '__main__':
    data_root = "Agents/BookStore/RawData"
    subject = "Area Studies"
    subsubject = "African American Studies"
    text = """




Skip to Main Content
Have library access? Log in through your library
JSTOR Home
All Content
Images
Search journals, books, images, and primary sources

Register
Log in
Workspace
Search
Browse


Tools
About
Support
African American Review
SEARCH THE JOURNAL

This title is part of a longer publication history. The full run of this journal will be searched.

TITLE HISTORY
1992-2019
•
African American Review
1976-1991
•
Black American Literature Forum
1967-1976
•
Negro American Literature Forum
As the official publication of the Division on Black American Literature and Culture of the Modern Language Association, the quarterly journal African American Review promotes a lively exchange among writers and scholars in the arts, humanities, and social sciences who hold diverse perspectives on African American literature and culture. Between 1967 and 1976, the journal appeared under the title Negro American Literature Forum and for the next fifteen years was titled Black American Literature Forum. In 1992, African American Review changed its name for a third time and expanded its mission to include the study of a broader array of cultural formations. Currently, the journal prints essays on African American literature, theatre, film, the visual arts, and culture generally; interviews; poetry; fiction; and book reviews. AAR has received three American Literary Magazine Awards for Editorial Content in the 1990s.

All Issues
2010s
2019 (Vol. 52)
No. 4 Winter 2019 pp. 323-412
No. 3 Fall 2019 pp. 217-321
No. 2 Summer 2019 pp. 121-215
No. 1 Spring 2019 pp. 1-120
2018 (Vol. 51)
No. 4 Winter 2018 pp. 253-350
No. 3 Fall 2018 pp. 161-251
No. 2 Summer 2018 pp. 81-159
No. 1 Spring 2018 pp. 1-79
2017 (Vol. 50)
No. 4 Commemorative Issue: 50 Years of AAR Winter 2017 pp. 343-1124
No. 3 Fall 2017 pp. 251-341
No. 2 Special Issue: Blackness & Disability Summer 2017 pp. 93-250
No. 1 Spring 2017 pp. 1-91
2016 (Vol. 49)
No. 4 Winter 2016 pp. 297-404
No. 3 Fall 2016 pp. 179-296
No. 2 Summer 2016 pp. 75-177
No. 1 Spring 2016 pp. 1-73
2015 (Vol. 48)
No. 4 Winter 2015 pp. 393-487
No. 3 Special Issue: Delany Lately Fall 2015 pp. 225-392
No. 1/2 Spring/Summer 2015 pp. 1-224
2014 (Vol. 47)
No. 4 Winter 2014 pp. 447-598
No. 2/3 Summer/Fall 2014 pp. 231-446
No. 1 Spring 2014 pp. 1-229
2013 (Vol. 46)
No. 4 Special Issue: James Baldwin Winter 2013 pp. 559-803
No. 2/3 Summer/Fall 2013 pp. 201-558
No. 1 Special issue: Hip Hop and the Literary Spring 2013 pp. 1-200
2012 (Vol. 45)
No. 4 Winter 2012 pp. 495-686
No. 3 Special issue: On Black Performance Fall 2012 pp. 275-494
No. 1/2 Spring/Summer 2012 pp. 1-274
2011 (Vol. 44)
No. 4 Winter 2011 pp. 561-740
No. 3 Fall 2011 pp. 331-556
No. 1/2 Spring/Summer 2011 pp. 1-329
2000s
1990s
Journal Information
The Johns Hopkins University Press logo African American Review logo African American Review (St. Louis University) logo
cover of African American Review
PUBLISHED BY
The Johns Hopkins University Press on behalf of African American Review (St. Louis University)
Submissions
Journal Home Page
Subscribe
COVERAGE
1992-2019 (Vol. 26, No. 1 - Vol. 52, No. 4)
MOVING WALL
Learn more
3 years
ISSN
10624783
EISSN
19456182
SUBJECTS
Language & Literature, African American Studies, American Studies, Area Studies, Humanities
COLLECTIONS
Arts & Sciences I Collection, JSTOR Archival Journal & Primary Source Collection, JSTOR Essential Collection, Language & Literature Collection
Explore JSTOR
By Subject
By Title
Collections
Publisher
Advanced Search
Images
Data for Research
Get Access
Get Support
LibGuides
Research Basics
About JSTOR
Mission and History
What's in JSTOR
Get JSTOR
News
Webinars
JSTOR Labs
JSTOR Daily
Careers
Contact Us
For Librarians
For Publishers
JSTOR is part of ITHAKA, a not-for-profit organization helping the academic community use digital technologies to preserve the scholarly record and to advance research and teaching in sustainable ways.

©2000‍–2023 ITHAKA. All Rights Reserved. JSTOR®, the JSTOR logo, JPASS®, Artstor®, Reveal Digital™ and ITHAKA® are registered trademarks of ITHAKA.

Terms & Conditions of Use
Privacy Policy
Accessibility
Cookie Policy
Cookie Settings
选择语言



    """

    soft_mkdir(join(data_root, subject), soft=True)
    
    tar_csv_path = join(data_root, subject, f"{subsubject}.csv")
    if not os.path.exists(tar_csv_path):
        df = pd.DataFrame(columns=["TITLE", "PUBLISHED BY", "COVERAGE", "MOVING WALL", "ISSN", "EISSN", "SUBJECTS", "COLLECTIONS", "ABSTRACT"])
    else:
        df = pd.read_csv(tar_csv_path)
    
    journal_info = extract_journal_information(text, subject, subsubject)
    print(journal_info)
    df = df._append(journal_info, ignore_index=True)
    df.to_csv(tar_csv_path, index=False)

    