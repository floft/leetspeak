leetspeak
=========
Years ago I started working on [Garot Bot
2.0](http://floft.net/wiki/Scripts/Archives/Garot_Bot.html). Well, that project was enormous and
never completed. However, as part of the project I wanted to have a LeetSpeak
to English translator. This multi-threaded Python 3 converter/translator
deciphers your messages using probability of word usage taken from the [Project
Gutenberg](http://www.gutenberg.org/) from all the possibilities it can
generate. I have yet to see any translator that works in as many cases as this
one.

Using
-----
 1. Install python3.
 1. Run: ``python3 leet.py --demo`` to test or ``python3 leet.py [-e] "Your Message"``
    to decode (by default) or encode a message.

Notes
-----
 * It will run slower the first time while it generates the .pickle files.
 * This program decodes better than encodes since encoding just randomly choses
   characters, which does not look at all like normal leet.
 * The program ignores all punctuation. How does it know if that period is part
   of the leet or is a period?
 * I'm not fond of the coding style I used back then. This was one of my first
   major Python projects.

Example
-------
Some things work.

     [garrett leetspeak]$ python3 leet.py -e "How are you doing today mother?"
     )-(ω\_1_/ /\|2ə \j()/_/ [)¤ai/|/gee -l-¤l]/-\-/ /|/|{}-l-[-]€[z?

     [garrett leetspeak]$ python3 leet.py ")-(ω\_1_/ /\|2ə \j()/_/ [)¤ai/|/gee -l-¤l]/-\-/ /|/|{}-l-[-]€[z?"
     how are you doing today mother

And some things don't. Note that Github was not a common word a few hundred
years ago.

     [garrett leetspeak]$ python3 leet.py -e "This is a test for Github."
     '][']-[eyeš 3y35 /-\ +e$-1- |=0® (_+l†}-{yuu|3.

     [garrett leetspeak]$ python3 leet.py "'][']-[eyeš 3y35 /-\ +e$-1- |=0® (_+l†}-{yuu|3."
     this is a tehiubhig for

License
-------
The words lists are from */usr/share/dict*, which I believe is from
[aspell](ftp://ftp.gnu.org/gnu/aspell/dict/0index.html), under GPL2. I would
say where *stopwords_en.txt* came from, but I think that's a combination of
many sites and my own thoughts. As for slang, it's from [No
Slang](http://www.noslang.com/dictionary/), and I don't see a license. The
*gutenberg_small.txt* file is obviously from Gutenberg; although, I have since
lost the script to generated it (hence why I just provide the file here). The
*phonetics.py* file is from [AdvaS Advanced
Search](http://sourceforge.net/projects/advas/) and is GPL. All of my code, as
always, is under the [ISC license](http://floft.net/files/isc-license.txt).
