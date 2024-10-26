from financial_metrics1.metrics import calculate_net_profit, calculate_roi

def main_menu():
    revenue = float(input("Введите доходы: "))
    costs = float(input("Введите расходы: "))

    net_profit = calculate_net_profit(revenue, costs)
    roi = calculate_roi(net_profit, costs)

    print(f"Чистая прибыль: {net_profit:.2f} руб.")
    print(f"ROI: {roi:.2f}%")

if __name__ == "__main__":
    main_menu()