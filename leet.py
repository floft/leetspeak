import sys
import argparse
import string
from LeetSpeak import LeetSpeak
from multiprocessing import cpu_count


parser = argparse.ArgumentParser(prog='leet',
    description='Translate from Leet to and from English')
parser.add_argument('-p', action='store', dest='threads',
    type=int, default=cpu_count(),
    help="Max number of threads") 
parser.add_argument('-e', action='store_true', dest='encode',
    default=False, help='Encode instead of decoding input')
parser.add_argument('--demo', action='store_true', dest='demo',
    default=False, help='Run a demo')
parser.add_argument('text', action='store',
    nargs='*', default='', help='Input String');

args = parser.parse_args(sys.argv[1:])
text=' '.join(args.text)

if not text:
    parser.print_help()
else:
    l=LeetSpeak(args.threads)

    # Just run some tests
    if args.demo:
        phrases = [
            # "four score and seven years ago our fathers brought forth upon this continent a new nation conceived in liberty and dedicated to the proposition that all men are created equal",
            "ph0uR 5c0r3 4ND 53V3N y34R5 490 0uR Ph4th3R5 8R0u9hT ph0rtH uP0N tH15 K0Nt1n3nt 4 n3w n4T10n K0nC31V3d 1n L183RTY 4Nd D3D1c4t3D t0 t3H pR0P051t10N th@ 4LL m3N R CR34T3d 3qU4L",
            "|>|-|0U.- 5(0.-3 4nd 53\\/3n \\-/34.-z 460 0U.- |>|-|47|-|3.-z 8.-0u6|-|7 |>|-|0.-7|-| U|>0N 7|-|1Z |<0N71N3N7 4 n3\\|/ n4710n |<0n(31\\/3d 1n l183.-7\\-/ 4nd D3d1(473D 70 73|-| |>.-0|>051710N 7|-|@ 4|_|_ |\\/|3N .- (.-3473D 3|<\\|/4l",
            "|=0|_|r sc0r3 |\\| s3\\/3|\\| '/34r2 460 0|_|r |=47#3r2 br0|_|6#7 |=0r7# |_|p0|\\| d12 c0|\\|71|\\|3|\\|7 @ |\\|3\\/\\/ |\\|4710|\\| c0|\\|c31\\/3d 1|\\| |_1b3r7'/ |\\| d3d1c473d 2 73# pr0p0s1710|\\| d47 4|_|_ d00d2 12 cr3473d 3q|_|4|_",
            # "the stage is set it is the first noel",                                
            "7H3 57493 1z 537 17 1z 7H3 F1r57 n03l",
            "73}{ 57463 12 537 17 12 73}{ |>}{1.-57 |\\|03|_",
            # "the quick brown fox jumped over the lazy dog",
            "7h3 Qu1ck 8R0Wn pH0X JuMp3D 0v3r 7H3 L42Y d09",
            "73|-| /<\\|/|(/< 8R0\\|/|\\| |>|-|0X _||_||\\/||>3D 0\\/3r 73|-| |_42`/ D09",
            # "hello how are you"
            "h3LL0 h0w R j00",
            "|-|3|_|_o |-|o\\|/ .- _|OO",
            # letters
            "R",
            "4",
            "th@",
            # More fun
            "7h15 15 4 v3ry b451c f0rm 0f 31i73, 0nly 1nv0lv1ng numb3r 5ub5717u710n",
            "7|-|3 [,]|_|1(|< |3|20\\\\/\\\\/|\\\\| |=0>< ]|_|/\\\\/\\\\|?5 0\\\\/3|2 7|-|3 |_42`/ [)09",
            "+h3 []\\[][-*7 ci1]vaye~([-|> |=oh|~/V\\ ()]= 7[-e-1- 1/\\/see()|^1*{}1^/_\\-l-[-$ |^^|3y35z17el_1|ncjes, cic|^0~'/.\\\\es, l_et']['eI2 /-\\6ci/\\/|}[]{\\}(\\/)e]\\[-1- /_\\|\\|l] [ze9l_@(e|\\/|e//-l- \\^/i-l-aych //\\_/^^b[-|~2 0} 2ai|\\/||1/\\1^ 2oh|_|//\\\\//d$",
        ]

        print("Test Output")
            
        for phrase in phrases:
            print("Input:",phrase)
            #leet=l.ConvertToLeet(phrase)
            #print("Leet:",leet)
            print("Output:",l.ConvertFromLeet(phrase))
            print()
    else:
        if args.encode == True:
            print(l.ConvertToLeet(text))
        else:
            print(l.ConvertFromLeet(text))
