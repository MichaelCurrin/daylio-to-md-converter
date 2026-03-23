# Daylio to MD Converter
> Convert a Daylio CSV export to a folder of Markdown files with frontmatter and notes in the body


This CSV tool will create one Markdown file per entry in the output folder and print the
unique activities list to the console. This is ideal if you want to migrate Daylio content to Obsidian.

Not supported - scales in Daylio.


## Setup and run

Install Python.

Install with pip:

```sh
$ pip install git+https://github.com/MichaelCurrin/daylio-to-md-converter
```

## Usage

```sh
daylio2md --help
```

```sh
daylio2md INPUT_CSV OUTPUT_DIR
```

## Development

Clone the repository and install dependencies using Poetry:

```bash
git clone https://github.com/MichaelCurrin/daylio-to-md-converter.git
cd daylio-to-md-converter
make install
```

```sh
poetry run python -m daylio2md TYPE INPUT_CSV OUTPUT_DIR
```

Show available commands:

```sh
make help
```

Test using the demo:

```sh
make demo
```


## Related projects

- [MichaelCurrin/daylio-csv-parser](https://github.com/MichaelCurrin/daylio-csv-parser)
- [MichaelCurrin/remente-to-md-converter](https://github.com/MichaelCurrin/remente-to-md-converter)


## License

Licenses under [MIT](/LICENSE) by [MichaelCurrin](https://github.com/MichaelCurrin/).
