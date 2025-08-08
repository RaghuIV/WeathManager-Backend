from rest_framework.decorators import api_view
from rest_framework.response import Response
from collections import defaultdict
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .sample_data import portfolio_data, performance_data

@api_view(['GET'])
def portfolio_holdings(request):
    data = [
        {
            "symbol": "RELIANCE",
            "name": "Reliance Industries Ltd",
            "quantity": 50,
            "avgPrice": 2450.00,
            "currentPrice": 2680.50,
            "sector": "Energy",
            "marketCap": "Large",
            "value": 134025.00,
            "gainLoss": 11525.00,
            "gainLossPercent": 9.4
        }
    ]
    return Response(data)

@api_view(['GET'])
def portfolio_allocation(request):
    by_sector = defaultdict(float)
    by_market_cap = defaultdict(float)
    total_value = 0

    # Step 1: Calculate value per holding and accumulate sector/marketCap totals
    for stock in portfolio_data:
        quantity = stock["quantity"]
        current_price = stock["currentPrice"]
        value = quantity * current_price

        by_sector[stock["sector"]] += value
        by_market_cap[stock["marketCap"]] += value
        total_value += value

    # Step 2: Convert to desired format with percentage
    def format_allocation(allocation_dict):
        return {
            key: {
                "value": round(value, 2),
                "percentage": round((value / total_value) * 100, 1) if total_value else 0
            }
            for key, value in allocation_dict.items()
        }

    data = {
        "bySector": format_allocation(by_sector),
        "byMarketCap": format_allocation(by_market_cap)
    }

    return Response(data)


@api_view(['GET'])
def portfolio_performance(request):
    def calculate_returns(data):
        returns = {}
        latest = data[-1]
        for label, months_ago in [("1month", -1), ("3months", -2), ("1year", 0)]:
            try:
                for asset in ["portfolio", "nifty50", "gold"]:
                    current = latest[asset]
                    past = data[months_ago][asset]
                    change = ((current - past) / past) * 100 if past else 0
                    if asset not in returns:
                        returns[asset] = {}
                    returns[asset][label] = round(change, 1)
            except IndexError:
                continue
        return returns

    return Response({
        "timeline": performance_data,
        "returns": calculate_returns(performance_data)
    })


@api_view(['GET'])
def portfolio_summary(request):
    total_invested = 0
    total_value = 0
    performance_list = []

    for stock in portfolio_data:
        quantity = stock["quantity"]
        avg_price = stock["avgPrice"]
        current_price = stock["currentPrice"]
        invested = quantity * avg_price
        value = quantity * current_price
        gain_percent = ((current_price - avg_price) / avg_price) * 100 if avg_price else 0

        total_invested += invested
        total_value += value

        performance_list.append({
            "symbol": stock["symbol"],
            "name": stock["name"],
            "gainPercent": round(gain_percent, 2)
        })

    gain_loss = total_value - total_invested
    gain_loss_percent = (gain_loss / total_invested) * 100 if total_invested else 0

    # Get best/worst performer
    top = max(performance_list, key=lambda x: x["gainPercent"])
    worst = min(performance_list, key=lambda x: x["gainPercent"])

    # These can be static or computed
    diversification_score = 8.2
    risk_level = "Moderate"

    return Response({
        "totalValue": round(total_value, 2),
        "totalInvested": round(total_invested, 2),
        "totalGainLoss": round(gain_loss, 2),
        "totalGainLossPercent": round(gain_loss_percent, 2),
        "topPerformer": top,
        "worstPerformer": worst,
        "diversificationScore": diversification_score,
        "riskLevel": risk_level
    })
