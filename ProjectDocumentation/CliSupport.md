## CLI Support (How it works)

#### Main Objective
- Have an way for the user to get more options to work with the project with CLI Commands and arguments using the `argparse` library from python.

#### `argparse` Library (My Learning)
- Standard library module for implementing basic CLI applications. 

- The program defines what arguments it requires, and `argparse` will figure out how to parse those out of `sys.argv`. The argparse module can also generate help and usage messages and issue errors.

- The `argparse` is built around an instance of `argparse.ArgumentParser`. It is a container for argument specifications and has options that apply to the parser as a whole.

```python
    parser = argparse.ArgumentParser(prog='Program Name',description='What the program does',...)
```

- The `ArgumentParser.add.argument()` method attaches individual argument specifications to the parser. It supports a lot of different values.
```python
    parser.add_argument('filename')           # positional argument
    parser.add_argument('-c', '--count')      # option that takes a value
    parser.add_argument('-v', '--verbose',
                        action='store_true')  # on/off flag
```

##### Argument Parser Objects
- `prog` - The name of the program 
- `usage` - The string describing the program usage
- `description` - Text to display before the argument help
- `epilog` - Text to display after the argument help
- ... There is more I will add them If I use them


```bash
    # How it should work Main Idea
    python scanner.py https://github.com   # Only URL works normally
    python scanner.py https://github.com --timeout X or -t X # Works with the URL with the possibility of adding a custom Timeout 
    python scanner.py https://github.com --rawHeaders or -r # Shows the full header of the chosen website
    python scanner.py --help # Create the help argument to explain the commands on the terminal
```