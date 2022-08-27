[![Binance Community API](https://github.com/davidpinhas/cryptoview/blob/master/static/images/CryptoView.png)](https://github.com/davidpinhas)
# CryptoView
A personal dashboard for your Binance wallet, using Binance API.
For the full [Binance API documentation](https://python-binance.readthedocs.io/en/latest/binance.html).

### Prerequisites
- Create Binance API keys using the [official documentation](https://www.binance.com/en/support/faq/360002502072).
- Export API keys:
```bash
export BINANCE_API="$API"
export BINANCE_SECRET="$SECRET"
```

## Quick Start
### Run Flask Application
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install cryptoview.

```bash
git clone https://github.com/davidpinhas/cryptoview.git
cd cryptoview
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
flask run
```
Test application:
```bash
curl http://127.0.0.1:5000
```

### Run Docker Container

```bash
sudo docker build -t cryptoview:1.0.0 .
sudo docker run -p 5001:5001 --restart unless-stopped -it -d --name cryptoview \
-e BINANCE_API=<BINANCE_API> -e BINANCE_SECRET=<BINANCE_SECRET> cryptoview:1.0.0
```

Test application:
```bash
curl http://127.0.0.1:5001
```

### Helm Deployment
#TODO

## Contribution
- Give a star :star:
- Feel free to Fork and Clone :beers:
- Check my [issues](https://github.com/davidpinhas/cryptoview/issues) or create a [new issue](https://github.com/davidpinhas/cryptoview/issues/new) and give me a PR with your bugfix or improvement after. I appreciate any help! ❤️

## License
[MIT](https://choosealicense.com/licenses/mit/)
