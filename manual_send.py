from transport import Transport

delivery=[
    {'id': 163455889317807, 'transport': 'SFTP', 'host': 'localhost', 'login': 'reporter', 'password': 'reporter', 'port': 22, 'remote_dir': '/database/home/reporter/f9pcr/spool/Humana/HumanaXMLtestDir', 'remote_file': '/database/home/reporter/f9pcr/spool/Humana/HumanaXMLtestDir/Jenna Amos_9_27_2021_11_30_30 AM_300000071048242.xml', 'key': None, 'file': 'Jenna Amos_9_27_2021_11_30_30 AM_300000071048242.xml', 'spool_file': '/Users/apetrov/LearnPython/projects/mail2ftp/spool/163455889317807/Jenna Amos_9_27_2021_11_30_30 AM_300000071048242.xml', 'spool': '/Users/apetrov/LearnPython/projects/mail2ftp/spool/163455889317807', 'local': False},
    {'id': 163455889317807, 'transport': 'SFTP', 'host': 'localhost', 'login': 'reporter', 'password': 'reporter', 'port': 22, 'remote_dir': '/database/home/reporter/f9pcr/spool/Humana/HumanaXMLtestDir', 'remote_file': '/database/home/reporter/f9pcr/spool/Humana/HumanaXMLtestDir/Alecia Burnett_9_27_2021_11_32_07 AM_300000071048246.xml', 'key': None, 'file': 'Alecia Burnett_9_27_2021_11_32_07 AM_300000071048246.xml', 'spool_file': '/Users/apetrov/LearnPython/projects/mail2ftp/spool/163455889317807/Alecia Burnett_9_27_2021_11_32_07 AM_300000071048246.xml', 'spool': '/Users/apetrov/LearnPython/projects/mail2ftp/spool/163455889317807', 'local': False}, 
    {'id': 163455889317807, 'transport': 'SFTP', 'host': 'localhost', 'login': 'reporter', 'password': 'reporter', 'port': 22, 'remote_dir': '/database/home/reporter/f9pcr/spool/Humana/HumanaXMLtestDir', 'remote_file': '/database/home/reporter/f9pcr/spool/Humana/HumanaXMLtestDir/Jenna Amos_9_27_2021_11_38_00 AM_300000071048252.xml', 'key': None, 'file': 'Jenna Amos_9_27_2021_11_38_00 AM_300000071048252.xml', 'spool_file': '/Users/apetrov/LearnPython/projects/mail2ftp/spool/163455889317807/Jenna Amos_9_27_2021_11_38_00 AM_300000071048252.xml', 'spool': '/Users/apetrov/LearnPython/projects/mail2ftp/spool/163455889317807', 'local': False}
    ]


cnx=Transport(delivery)
print(cnx.put())
#cnx.put()

