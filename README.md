[![Binance Community API](https://cdn.discordapp.com/attachments/569865969120575519/718166995354255370/binance-api-black.png)](https://dev.binance.vision/)
# CryptoView
A personal dashboard for your Binance wallet, using Binance API.
For the full [Binance API documentation](https://python-binance.readthedocs.io/en/latest/binance.html).

## Installation
### Python Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install cryptoview.

```bash
git clone https://github.com/davidpinhas/cryptoview.git
cd cryptoview
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
flask run
```

### Docker Installation

```bash
sudo docker build -t cryptoview:1.0.0 .
sudo docker run -p 5000:5000 --restart unless-stopped -it -d --name cryptoview \
-e BINANCE_API=<BINANCE_API> -e BINANCE_SECRET=<BINANCE_SECRET> cryptoview:1.0.0
```

## Usage

Application should be available on [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## Contribution
- Give a star :star:
- Feel free to Fork and Clone :beers:
- Check my [issues](https://github.com/davidpinhas/cryptoview/issues) or create a [new issue](https://github.com/davidpinhas/cryptoview/issues/new) and give me a PR with your bugfix or improvement after. I appreciate any help! ❤️

## License
[MIT](https://choosealicense.com/licenses/mit/)