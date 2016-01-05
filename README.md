# :star: The Testing Game 1.0 :star:

Welcome to the Testing Game! A simple script that counts the number of Objective-C, Java, C++ or python unit tests in the current working directory within a git repository, and showcases a ranking based on the percentage each developer has written.

**Example output:**

```shell
Total Tests: 2694
-------------------------------------------
1. Ellie Goulding , 659 (24.46%)
2. Bruno Mars, 255 (9.47%)
3. Ed Sheeran, 250 (9.28%)
4. Sam Smith, 199 (7.39%)
5. Calvin Harris, 147 (5.46%)

```

## Background

This script was made to “gameify” testing at Spotify and to continue encouraging Test-Driven Development. 

## How It Works

The script uses the current working directory to find files it could possibly read (such as `.m`, `.mm` and `.java` files) and performs a `git blame` on these files in order to match tests written to the developers that wrote them. 
The owner of the method name of the test is considered the developer that wrote it.

## Dependencies

* [python 2.7.10](https://www.python.org/downloads/release/python-2710/) (for running the script)
* [git 2.6.1](https://git-scm.com/) (for finding the blame information for a given file)

The script should run on any operating system containing these two dependencies.

## Usage

1. Run the Python setup.py from this repository:

    ```shell
    > python setup.py install
    ```

2. Run  the testing game script from your repository (or subdirectory):

    ```shell
    > testinggame
    ```

3. Mention that you write most unit units of your project on every meeting (no, don’t do that).


## Contribution

Yes please! Contributions are always welcomed, have a look at the [CONTRIBUTING.md](https://github.com/spotify/testing-game/blob/master/CONTRIBUTING.md) document for more information.

## Credits

See [the project’s contributors](https://github.com/spotify/testing-game/graphs/contributors) page.

## License

This repository is licensed under an [Apache 2](http://www.apache.org/licenses/LICENSE-2.0) license. 
