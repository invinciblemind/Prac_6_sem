import gettext
import locale
from . import PATH



locale = locale.setlocale(locale.LC_ALL, locale.getlocale())

transcode = gettext.translation("wordcount", PATH, fallback=True)
# transtext = gettext.translation("wordcount2", PATH, fallback=True)
ngettext = transcode.ngettext
# ngettext2 = transtext.ngettext

s = input()
words = s.split()
N = len(words)
print(ngettext("Entered {} word", "Entered {} words", N).format(N))
# print(ngettext2("Entered {} word", "Entered {} words", N).format(N))
