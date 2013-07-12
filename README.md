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
