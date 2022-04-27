# import docx
# import datetime
# doc = docx.Document('1.docx')
# for par in doc.paragraphs:
#     print(par.text)
# s = doc.paragraphs[1].text.split()[1]
# s = [int(i) for i in s.split('.')[::-1]]
# start = datetime.datetime(s[0], s[1], s[2])
# for i in range(30):
#     start = start + datetime.timedelta(days=1)
#     doc.paragraphs[1].text = doc.paragraphs[1].text.split()[0] + start.strftime('%d.%m.%Y')
#     doc.save(start.strftime('%d-%m-%Y') + '.docx')
a = -3
print('sfasdvf %5.3f sdfasdv', a)