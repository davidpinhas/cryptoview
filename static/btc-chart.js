var chart = LightweightCharts.createChart(document.getElementById('btc_chart'), {
	width: 710,
	height: 350,
	
	layout: {
		backgroundColor: '#000000',
		textColor: 'rgba(255, 255, 255, 0.9)',
	},
	grid: {
		vertLines: {
			color: 'rgba(197, 203, 206, 0.5)',
		},
		horzLines: {
			color: 'rgba(197, 203, 206, 0.5)',
		},
	},
	crosshair: {
		mode: LightweightCharts.CrosshairMode.Normal,
	},
	priceScale: {
		borderColor: 'rgba(197, 203, 206, 0.8)',
	},
	timeScale: {
		borderColor: 'rgba(197, 203, 206, 0.8)',
		timeVisible: true,
		secondsVisible: false,
	},
});

var btcCandleSeries = chart.addCandlestickSeries({
	upColor: '#00ff00',
	downColor: '#ff0000', 
	borderDownColor: 'rgba(255, 144, 0, 1)',
	borderUpColor: 'rgba(255, 144, 0, 1)',
	wickDownColor: 'rgba(255, 144, 0, 1)',
	wickUpColor: 'rgba(255, 144, 0, 1)',
});

fetch('http://0.0.0.0:5001/btc_history')
	.then((r) => r.json())
	.then((response) => {
		console.log(response)

		btcCandleSeries.setData(response);
	})


var btcBinanceSocket = new WebSocket("wss://stream.binance.com:9443/ws/btcusdt@kline_1m");

btcBinanceSocket.onmessage = function (event) {	
	var message = JSON.parse(event.data);

	var candlestick = message.k;

	console.log(candlestick)

	btcCandleSeries.update({
		time: candlestick.t / 1000,
		open: candlestick.o,
		high: candlestick.h,
		low: candlestick.l,
		close: candlestick.c
	})
}