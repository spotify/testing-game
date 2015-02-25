# testing-game
A pointless project I did to showcase the fact that I wrote more tests than anyone else. It counts the number of iOS and Android tests in a current working directory within a git repository, and the percentage of the tests each developer writes.

## LICENSE
[Apache 2](http://www.apache.org/licenses/LICENSE-2.0)

## BACKGROUND
This script was made to "gameify" testing at Spotify for cultural purposes, and to show off my testing skills.

## HOW IT WORKS
The script uses the current working directory to find files it could possibly read (such as .m, .mm and .java) and performs a git blame on these files in order to match tests written to the developers that wrote them. The owner of the method name of the test is considered the developer that wrote that.

## USAGE
Run "python testing-game.py" in the repository of your choosing.

## CONTRIBUTION
Contributions are welcomed, have a look at the [CONTRIBUTING.md](https://github.com/spotify/testing-game/blob/master/CONTRIBUTING.md) document for more information.

## CREDITS
* Will Sackfield
* Adam Price
