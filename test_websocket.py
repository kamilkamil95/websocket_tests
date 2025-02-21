import websockets
import json
import time

BINANCE_WS_URL = 'wss://stream.binance.com:9443/ws/btcusdt@trade'
MAX_LATENCY = 1.0

async def test_binance_websocket():
    try:
        async with websockets.connect(BINANCE_WS_URL) as websocket:
            print("Conntected to Binance websocket")

            received_prices = []
            latencies = []

            for _ in range(10):
                start_time= time.time()
                message = await websocket.recv()
                end_time = time.time()
                latency = end_time - start_time
                latencies.append(latency)

                data = json.loads(message)

                assert "s" in data,"Error: missing field 's' (symbol)"
                assert "p" in data,"Error: missing field 'p' (price)"
                assert "q" in data,"Error: missing field 'q' (quantity)"

                symbol = data['s']
                price = float(data['p'])
                quantity = float(data['q'])

                print(f"Trade received: {symbol}, Price: {price} USDT, Quantity: {quantity}, Latency: {latency:.3f} s")

                received_prices.append(price)
                assert price > 0, "Error: Invalid price received"
                assert latency < MAX_LATENCY, f'Warning: Latency {float(latency)} exceeds {MAX_LATENCY:.3f}'

            assert received_prices, "Error: No BTC/USDT prices received"

            avg_latency = sum(latencies) / len(latencies)

            print(f"Avg Websocket Latency: {avg_latency:.3f} s")

            print("Websocket test completed successfully")

    except Exception as e:
        print(f"Unexpected error while testing Websocket {e}")
    except websockets.exceptions.ConnectionClosed:
        print("Error: WebSocket connection was closed.")
