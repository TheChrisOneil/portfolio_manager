# To run: python -m pytest app/src/flink/test_portfolio_calculator.py
# Note: Make sure to run the test from the root directory of the project
# cd /Users/thechrisoneil/software/kafka/portfolio_manager

import json
from .portfolio_recalculator import recalculate_portfolio, process_transactions


def test_recalculate_portfolio():
    # Sample transaction and portfolio state
    transaction = {"user_id": "1", "stock": "AAPL", "quantity": 10}
    portfolios = {}

    # Recalculate portfolio
    updated_portfolio = recalculate_portfolio(transaction, portfolios)

    # Verify
    assert updated_portfolio == {"1": {"AAPL": 10}}
    print("recalculate_portfolio passed!")

def test_process_transactions():
    # Sample input
    transaction_json = json.dumps({"user_id": "2", "stock": "GOOGL", "quantity": 5})
    portfolios = {}

    # Process transaction
    result = process_transactions(transaction_json, portfolios)

    # Verify
    assert json.loads(result) == {"2": {"GOOGL": 5}}
    print("process_transactions passed!")

if __name__ == "__main__":
    test_recalculate_portfolio()
    test_process_transactions()
