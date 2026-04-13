import gettext
import locale

locale = locale.setlocale(locale.LC_ALL, locale.getlocale())
'''
translation = gettext.translation("wordcount", 'po', fallback=True)
_, ngettext = translation.gettext, translation.ngettext
'''
transcode = gettext.translation("wordcount", 'po', fallback=True)
transtext = gettext.translation("wordcount2", 'po', fallback=True)
ngettext = transcode.ngettext
ngettext2 = transtext.ngettext

s = input()
words = s.split()
N = len(words)
print(ngettext("Entered {} word", "Entered {} words", N).format(N))
print(ngettext2("Entered {} word", "Entered {} words", N).format(N))
