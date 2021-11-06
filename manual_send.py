from transport_new import Transport
from transport.SFTP import Sftp
from common import get_path, get_utc_timestamp, get_delivery_params

PATH = get_path()

# delivery=[
#     {'id': 163455889317807, 'transport': 'SFTP', 'host': 'pcr005.scl.five9.com', 'login': 'reporter', 'password': 'reporter', 'port': 22, 'remote_dir': '/database/home/reporter/f9pcr/spool/Humana/HumanaXMLtestDir', 'remote_file': '/database/home/reporter/f9pcr/spool/Humana/HumanaXMLtestDir/Jenna Amos_9_27_2021_11_30_30 AM_300000071048242.xml', 'key': None, 'file': 'Jenna Amos_9_27_2021_11_30_30 AM_300000071048242.xml', 'spool_file': '/Users/apetrov/LearnPython/projects/mail2ftp/spool/163455889317807/Jenna Amos_9_27_2021_11_30_30 AM_300000071048242.xml', 'spool': '/Users/apetrov/LearnPython/projects/mail2ftp/spool/163455889317807', 'local': False},
#     {'id': 163455889317807, 'transport': 'SFTP', 'host': 'pcr005.scl.five9.com', 'login': 'reporter', 'password': 'reporter', 'port': 22, 'remote_dir': '/database/home/reporter/f9pcr/spool/Humana/HumanaXMLtestDir', 'remote_file': '/database/home/reporter/f9pcr/spool/Humana/HumanaXMLtestDir/Alecia Burnett_9_27_2021_11_32_07 AM_300000071048246.xml', 'key': None, 'file': 'Alecia Burnett_9_27_2021_11_32_07 AM_300000071048246.xml', 'spool_file': '/Users/apetrov/LearnPython/projects/mail2ftp/spool/163455889317807/Alecia Burnett_9_27_2021_11_32_07 AM_300000071048246.xml', 'spool': '/Users/apetrov/LearnPython/projects/mail2ftp/spool/163455889317807', 'local': False}, 
#     {'id': 163455889317807, 'transport': 'SFTP', 'host': 'pcr005.scl.five9.com', 'login': 'reporter', 'password': 'reporter', 'port': 22, 'remote_dir': '/database/home/reporter/f9pcr/spool/Humana/HumanaXMLtestDir', 'remote_file': '/database/home/reporter/f9pcr/spool/Humana/HumanaXMLtestDir/Jenna Amos_9_27_2021_11_38_00 AM_300000071048252.xml', 'key': None, 'file': 'Jenna Amos_9_27_2021_11_38_00 AM_300000071048252.xml', 'spool_file': '/Users/apetrov/LearnPython/projects/mail2ftp/spool/163455889317807/Jenna Amos_9_27_2021_11_38_00 AM_300000071048252.xml', 'spool': '/Users/apetrov/LearnPython/projects/mail2ftp/spool/163455889317807', 'local': False}
#     ]

# print (PATH)
# cnx=Transport(delivery)
# print(cnx.put())

delivery_ftp=[
    {'id': 163455889317807, 'transport': 'FTP', 'host': 'ftp.dlptest.com', 'login': 'dlpuser', 'password': 'rNrKYTX9g7z3RgJRmxWuGHbeu', 'port': 21, 'remote_dir': '/', 'remote_file': '/Jenna Amos_9_27_2021_11_30_30 AM_300000071048242.xml', 'key': None, 'file': 'Jenna Amos_9_27_2021_11_30_30 AM_300000071048242.xml', 'spool_file': '/Users/apetrov/LearnPython/projects/mail2ftp/spool/163455889317807/Jenna Amos_9_27_2021_11_30_30 AM_300000071048242.xml', 'spool': '/Users/apetrov/LearnPython/projects/mail2ftp/spool/163455889317807', 'local': False, 'options':{'TLS': False}},
    {'id': 163455889317807, 'transport': 'FTP', 'host': 'ftp.dlptest.com', 'login': 'dlpuser', 'password': 'rNrKYTX9g7z3RgJRmxWuGHbeu', 'port': 21, 'remote_dir': '/', 'remote_file': '/Alecia Burnett_9_27_2021_11_32_07 AM_300000071048246.xml', 'key': None, 'file': 'Alecia Burnett_9_27_2021_11_32_07 AM_300000071048246.xml', 'spool_file': '/Users/apetrov/LearnPython/projects/mail2ftp/spool/163455889317807/Alecia Burnett_9_27_2021_11_32_07 AM_300000071048246.xml', 'spool': '/Users/apetrov/LearnPython/projects/mail2ftp/spool/163455889317807', 'local': False, 'options':{'TLS':False}}, 
    {'id': 163455889317807, 'transport': 'FTP', 'host': 'ftp.dlptest.com', 'login': 'dlpuser', 'password': 'rNrKYTX9g7z3RgJRmxWuGHbeu', 'port': 21, 'remote_dir': '/', 'remote_file': '/Jenna Amos_9_27_2021_11_38_00 AM_300000071048252.xml', 'key': None, 'file': 'Jenna Amos_9_27_2021_11_38_00 AM_300000071048252.xml', 'spool_file': '/Users/apetrov/LearnPython/projects/mail2ftp/spool/163455889317807/Jenna Amos_9_27_2021_11_38_00 AM_300000071048252.xml', 'spool': '/Users/apetrov/LearnPython/projects/mail2ftp/spool/163455889317807', 'local': False, 'options':{'TLS':False}}
    ]
cnx=Transport(delivery_ftp)
print(cnx.put())