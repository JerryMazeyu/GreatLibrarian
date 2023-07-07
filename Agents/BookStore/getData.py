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
Black History Bulletin
SEARCH THE JOURNAL

This title is part of a longer publication history. The full run of this journal will be searched.

TITLE HISTORY
2002-2019
•
Black History Bulletin
1937-2001
•
Negro History Bulletin
The Black History Bulletin is dedicated to enhancing teaching and learning in the areas of history. Its aim is to publish, generate, and disseminate peer-reviewed information about African Americans in U. S. history, the African Diaspora generally, and the peoples of Africa. Its purpose is to inform the knowledge base for the professional praxis of secondary educators through articles that are grounded in theory, yet supported by practice. The Black History Bulletin welcomes articles on all aspects of Black history, especially those written with a focus on: (1) middle school U.S. history; (2) high school U.S. history; (3) teacher preparation U.S. history methods.
All Issues
2010s
2019 (Vol. 82)
No. 2 African Americans and the Vote Fall 2019 pp. 4-38
No. 1 Race, Revolution & Resistance Spring 2019 pp. 4-34
2018 (Vol. 81)
No. 2 Black Migrations Fall 2018 pp. 1-33
No. 1 QUILTED HISTORIES: THE THREADS OF COUNTER NARRATIVES Spring 2018 pp. 1-34
2017 (Vol. 80)
No. 2 AFRICAN AMERICANS IN TIMES OF WAR Fall 2017 pp. 1-34
No. 1 POETRY, PROSE AND MUSIC: THE LYRICAL VOICE OF BLACK ARTS MOVEMENTS Spring 2017 pp. 1-34
2016 (Vol. 79)
No. 2 THE CRISIS IN BLACK EDUCATION Fall 2016 pp. 1-34
No. 1 YOUTH EMPOWERMENT: HOPE, ACTION, AND FREEDOM Spring 2016 pp. 1-34
2015 (Vol. 78)
No. 2 HALLOWED GROUNDS: SITES OF AFRICAN AMERICAN MEMORIES Fall 2015 pp. 1-34
No. 1 SOCIAL JUSTICE: EVOLUTION OR REVOLUTION Spring 2015 pp. 1-31
2014 (Vol. 77)
No. 2 A CENTURY OF BLACK LIFE, HISTORY, AND CULTURE Fall 2014 pp. 1-33
No. 1 THE IMPACT OF MEDIA ON SCHOLAR IDENTITY DEVELOPMENT Spring 2014 pp. 1-33
2013 (Vol. 76)
No. 2 Theme: "CIVIL RIGHTS IN AMERICA" SUMMER / FALL 2013 pp. 1-34
No. 1 Theme: "FRAMING TECHNOLOGY THROUGH THE LENS OF HISTORY" SPRING 2013 pp. 1-34
2012 (Vol. 75)
No. 2 Theme: "At the Crossroads of Freedom and Equality: The Emancipation Proclamation and the March on Washington" Fall 2012 pp. 1-34
No. 1 Theme: "Taking a Look Back to Broaden the Lens of Literacy" Table of Contents Winter / Spring 2012 pp. 1-34
2011 (Vol. 74)
No. 2 Theme: "Black Women in American Culture and History" Summer/Fall 2011 pp. 1-35
No. 1 Theme: "The Influence of African Americans on Popular Culture" Winter/Spring 2011 pp. 1-33
2010 (Vol. 73)
No. 2 Theme: "African Americans and the Civil War" Summer/Fall 2010 pp. 1-35
No. 1 Theme: "Young, Gifted, & Black: Gifted Education in Today's Schools Winter/Spring 2010 pp. 1-35
2000s
Journal Information
Association for the Study of African American Life and History logo
cover of Black History Bulletin
PUBLISHED BY
Association for the Study of African American Life and History
COVERAGE
2002-2019 (Vol. 65, No. 1/2 - Vol. 82, No. 2)
MOVING WALL
Learn more
3 years
ISSN
19386656
EISSN
21534810
SUBJECTS
History, African American Studies, History, Area Studies
COLLECTIONS
Arts & Sciences XV Collection, JSTOR Archival Journal & Primary Source Collection
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

    