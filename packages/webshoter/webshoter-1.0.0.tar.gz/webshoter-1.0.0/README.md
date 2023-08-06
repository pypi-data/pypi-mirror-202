# Screenshot Tool

This tool takes screenshots of websites and saves them to a specified output directory in PNG format. It uses a headless browser to render the website and take the screenshot.

## Installation

Before using the tool, make sure you have Python 3 installed on your system. You can download Python from the official website: https://www.python.org/downloads/

Once you have Python installed, you can install the `webshoter` package using pip:

```sh
pip install webshoter
```


## Usage

To take a screenshot of a single website, use the following command:
```sh
webshoter -u <url> -o <output_dir>
echo "<url>" | webshoter -o <output_dir>
```

To take a screenshot of a list of websites, use the following command:
```sh
cat urls.txt | webshoter -o <output_dir>
```


Replace `<url>` with the URL of the website you want to take a screenshot of, and `<output_dir>` with the directory where you want to save the screenshot.

To take screenshots of multiple websites at once, you can provide a list of URLs separated by newlines. For example:


## License

This tool is distributed under the MIT License. See the LICENSE file for more information.