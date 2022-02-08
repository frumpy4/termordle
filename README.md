# termordle
a terminal based wordle clone in python

python 3.6+ is required

![preview](https://cdn.discordapp.com/attachments/147067727947759616/940467445645340692/unknown.png)

## running
```
git clone https://github.com/frumpy4/termordle.git
cd termordle
python termordle.py
```

## options
these can also be viewed with `termordle.py --help`

`--colorblind` `-cb` colorblind mode, changes green to orange and yellow to blue

![colorblind](https://cdn.discordapp.com/attachments/147067727947759616/940471802868670515/unknown.png)

`--daily` `-d` daily wordle, this is the same as official wordle. the default mode is random

`--hard` hard mode, selects from all valid words instead of just daily words. can also be combined with daily

`--allow-all` `-a` allow any 5 character string for guesses

`--no-emoji` `-q` don't print emoji output at the end

`--tries` `-t` select number of tries

`--word` `-w` select word, must be 5 characters