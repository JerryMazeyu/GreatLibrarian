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
Cover of Administering Freedom: The State of Emancipation after the Freedmen's Bureau
Administering Freedom: The State of Emancipation after the Freedmen's Bureau
DALE KRETZ
Copyright Date: 2022
Published by: University of North Carolina Press
Pages: 424
https://www.jstor.org/stable/10.5149/9781469671048_kretz
Search for reviews of this book

Cite
Book Info
This is a preview page.
Login through your institution for access.
Table of Contents

Select all

Cite

Front Matter(pp. i-vi)
Front Matter(pp. i-vi)
https://www.jstor.org/stable/10.5149/9781469671048_kretz.1

Save

Cite

Table of Contents(pp. vii-viii)
Table of Contents(pp. vii-viii)
https://www.jstor.org/stable/10.5149/9781469671048_kretz.2

Save

Cite

List of Illustrations(pp. ix-xii)
List of Illustrations(pp. ix-xii)
https://www.jstor.org/stable/10.5149/9781469671048_kretz.3

Save

Cite

Introduction(pp. 1-13)
Introduction(pp. 1-13)
https://www.jstor.org/stable/10.5149/9781469671048_kretz.4
“This is a needle threader. I made it myself,” chuckled the old man of Pine Bluff. “Watch me thread a needle.” Nearly a century old by the late 1930s and feeling “like a poor old leaf left hangin’ to a tree,” William Baltimore still had enough energy to captivate his visitor with stories of ingenuity, hunger, and war. Covered in patchwork clothing stitched together himself, Baltimore spun tales of how he had once made a hacksaw from only a file, and a cotton scraper out of a piece of hardwood and a fragment of steel. He boasted he could build...


Save

Cite

CHAPTER ONE What Is Left of the Bureau(pp. 14-57)
CHAPTER ONE What Is Left of the Bureau(pp. 14-57)
https://www.jstor.org/stable/10.5149/9781469671048_kretz.5
This story begins with an ending. The year 1872 saw the termination of the Freedmen’s Bureau, a remarkable federal welfare agency, the first of its kind, designed to usher the newly emancipated into the free labor system while devoting special resources and attention to those who fell behind. Its closure came as no surprise. One only had to look at the increasingly halfhearted attempts to defend the temporary agency and the bipartisan assaults upon it to anticipate its eventual collapse. Or one could view the bureau not from the halls of national power but rather from its embattled outposts scattered...


CHAPTER TWO The Unfinished Freedmen’s Branch(pp. 58-99)
CHAPTER TWO The Unfinished Freedmen’s Branch(pp. 58-99)
https://www.jstor.org/stable/10.5149/9781469671048_kretz.6
The Freedmen’s Branch grew out of failure. Established in June 1872, the new agency assumed the old work of the Freedmen’s Bureau, relegated as it was in its final years to the management of hospitals and schools and the settlement of claims for bounties, back payments, and pensions in the emancipated South. The ostensibly minor task of settling claims consumed the working hours of dozens of agents in the bureau’s final days. Given the potentially radical founding directive of the Freedmen’s Bureau and its multivalent operations, the contracting sphere of bureau activity in the early 1870s has understandably led many to...


CHAPTER THREE Reconstructing the Pension Bureau(pp. 100-143)
CHAPTER THREE Reconstructing the Pension Bureau(pp. 100-143)
https://www.jstor.org/stable/10.5149/9781469671048_kretz.7
It was a matter of life and death for countless freedpeople. But earning a federal pension would require far more of Black claimants than their previous struggles for bounties, and for far longer. Their pension claims necessarily dragged issues of slavery, the Civil War, and emancipation into the public light well into the twentieth century, defining their primary engagement with the federal government for decades. Though much less than what newly freed men and women had hoped for in 1865, receiving a recurring stipend based on loyalty and service more nearly approximated the sort of compact they had envisioned at...


CHAPTER FOUR Of War and Theft(pp. 144-187)
CHAPTER FOUR Of War and Theft(pp. 144-187)
https://www.jstor.org/stable/10.5149/9781469671048_kretz.8
If the reconstruction of the Pension Bureau in the South proceeded slowly, as it did so, it exposed at every turn the intensely fraught challenges faced by formerly enslaved men and women as they made their claims in a federal bureaucracy maladjusted to accommodate them. As widows and mothers, freedwomen proved unexpectedly per sis tent in their efforts to secure bounties and pensions, forcing the bureau to make discretionary exceptions when it became clear that enforcing statutory equality was tantamount to excluding the vast majority of formerly enslaved heirs from their entitlements. Their cases provoked issues that had been central...


CHAPTER FIVE Some Measure of Justice(pp. 188-232)
CHAPTER FIVE Some Measure of Justice(pp. 188-232)
https://www.jstor.org/stable/10.5149/9781469671048_kretz.9
The Civil War’s casualty lists grew after 1865. Hundreds of thousands of soldiers carried wounds, ailments, and other traumas into their postwar lives, making recovery and reconstruction not only national tasks but intimate ones as well, as millions of ordinary Americans encountered and endured disability like never before. The task for many was finding a way to honor republican sacrifice without sacrificing republican honor, and with it the ideals of manly in dependence and productivity. Few veterans could dodge the prevailing Gilded Age antagonism toward disabled persons. Even those onlookers who maintained that “worthy” veterans deserved the nation’s material support...


CHAPTER SIX Pensions for All(pp. 233-281)
CHAPTER SIX Pensions for All(pp. 233-281)
https://www.jstor.org/stable/10.5149/9781469671048_kretz.10
It was said there was neither North nor South in the Pension Bureau. It knew only loyalty. This axiom was no less true in the 1890s than it had been at the time the Union pension system began. Legions of loyal Southerners from seceded states gave lie to the sectionalist charge commonly leveled against the bureau, none more so than the growing contingency of Black Southerners who lodged their pension claims at extraordinary rates, isolated in many areas as the lone federal beneficiaries.¹ Yet the flurry of pension activity in the South following the Disability Act of June 1890 developed alongside...


Conclusion(pp. 282-296)
Conclusion(pp. 282-296)
https://www.jstor.org/stable/10.5149/9781469671048_kretz.11
In 1904, only months after the demolition of the ex-slave pension movement, rumors circulated of plans to abolish the U.S. Pension Bureau as well. Such talk swirled around the reelection campaign of President Theodore Roosevelt, whose nomination was secured after the death of his primary challenger, Senator Mark Hanna, less than one year after the latter disavowed support for universal ex-slave pensions. The Black press worried that the reelected president would remove the Pension Bureau from the Department of the Interior and place it fully under the control of the adjutant general in the War Department, the office that once...


Epilogue(pp. 297-302)
Epilogue(pp. 297-302)
https://www.jstor.org/stable/10.5149/9781469671048_kretz.12
“A misery got me in the chest, right here, and it been with me all through life,” remarked the former slave Boston Blackwell to an interviewer in the late 1930s. Blackwell had in fact “filed for a pension on this ailment.” During the Civil War, Blackwell fled his captors to join the U.S. Army near Pine Bluff, Arkansas. “It was cold, frosty weather,” he recalled, and the journey took two days and nights filled with the sounds of “hounds a-howling,” their haunting echoes trailing Blackwell and his freedom-seeking comrades. At last they reached “the Yankee camp,” believing “all our troubles...


Acknowledgments(pp. 303-306)
Acknowledgments(pp. 303-306)
https://www.jstor.org/stable/10.5149/9781469671048_kretz.13

Notes(pp. 307-362)
Notes(pp. 307-362)
https://www.jstor.org/stable/10.5149/9781469671048_kretz.14

Bibliography(pp. 363-400)
Bibliography(pp. 363-400)
https://www.jstor.org/stable/10.5149/9781469671048_kretz.15

Index(pp. 401-412)
Index(pp. 401-412)
https://www.jstor.org/stable/10.5149/9781469671048_kretz.16
University of North Carolina Press logo
Front Matter
Download
XML
Table of Contents
Download
XML
List of Illustrations
Download
XML
Introduction
Download
XML
What Is Left of the Bureau
Download
XML
The Unfinished Freedmen’s Branch
Download
XML
Reconstructing the Pension Bureau
Download
XML
Of War and Theft
Download
XML
Some Measure of Justice
Download
XML
Pensions for All
Download
XML
Conclusion
Download
XML
Epilogue
Download
XML
Acknowledgments
Download
XML
Notes
Download
XML
Bibliography
Download
XML
Index
Download
XML
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

    