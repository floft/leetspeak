leetspeak
=========
Years ago I started working on [Garot Bot
2.0](http://floft.net/wiki/Garot_Bot.html). Well, that project was enormous and
never completed. However, as part of the project I wanted to have a LeetSpeak
to English translator. This multi-threaded Python 3 converter/translator
deciphers your messages using probability of word usage taken from the [Project
Gutenberg](http://www.gutenberg.org/) from all the possibilities it can
generate. I have yet to see any translator that works in as many cases as this
one.

Using
-----
 1. Install python3.
 1. Download
    [gutenburg_small.txt](http://floft.net/uploads/gutenburg_small.txt) to
    *data/*
 1. Run: ``python3 leet.py --demo`` to test or ``python3 leet.py [-e] "Your Message"``
    to decode (by default) or encode a message.

Note that it will run slower the first time while it generates the .pickle
files. Also note that I'm not at all fond of my coding style that I used back
then. This was one of my first major Python projects.

License
-------
The words lists are from */usr/share/dict*, which I believe is from,
[aspell](ftp://ftp.gnu.org/gnu/aspell/dict/0index.html) under GPL2. I would say
where *stopwords_en.txt* came from, but I think that's a combination of many
sites and my own thoughts. As for slang, it's from [No
Slang](http://www.noslang.com/dictionary/), and I don't see a license.  The
*gutenberg_small.txt* file is obviously from Gutenberg.  All of my code, as
always, is under the [ISC license](http://floft.net/uploads/isc-license.txt).
