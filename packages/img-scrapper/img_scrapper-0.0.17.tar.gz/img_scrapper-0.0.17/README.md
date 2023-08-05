<div align="center">
  <img src="https://raw.githubusercontent.com/vatshgaurav/img_scrapper/dev-1/logo/img_scrapper_logo.png"><br>
</div>

# img_scrapper

A Python package to scrape and download images from Google search using
BeautifulSoup and Requests libraries.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install
img_scrapper.

```sh
#PyPi
pip install img-scrapper
```


## Usage

```python
from img_scrapper import get_original_images

images = get_original_images('Spotify', download=False)
```


* The script will display the first image it finds in the search
results. If you want to download the image, set download=True in the
get_original_images function call.

* The downloaded images will be saved in the Bs4_Img directory.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

This project is licensed under the MIT License - see the
[LICENSE.md](https://github.com/vatshgaurav/img_scrapper/blob/main/LICENSE) file for details.
