# testing-game
The “testing-game” project counts the number of iOS and Android tests in a current working directory within a git repository. This is then used to show the percentage of tests each contributing developer has written.

## LICENSE
The project is licensed under [Apache 2.0](http://www.apache.org/licenses/LICENSE-2.0).

## BACKGROUND
This script was made to “gameify” testing at Spotify for cultural purposes :smiley:

## HOW IT WORKS
The script uses the current working directory to find files it could possibly read (such as .m, .mm and .java) and performs a git blame on these files in order to match tests written to the developers that wrote them. The owner of the method name of the test is considered the developer that wrote that.

## USAGE
Run the script in a repository of your choosing:

```shell
python testing-game.py
```

## CONTRIBUTION
Contributions are welcomed, have a look at the [CONTRIBUTING.md](https://github.com/spotify/testing-game/blob/master/CONTRIBUTING.md) document for more information.

## CREDITS
* Will Sackfield
* Adam Price
