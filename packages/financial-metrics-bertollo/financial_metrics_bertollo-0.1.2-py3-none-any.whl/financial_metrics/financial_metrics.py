class FinancialMetrics:
    def __init__(self, revenue, costs):
        self.revenue = revenue
        self.costs = costs

    def net_profit(self):
        return self.revenue - self.costs

    def roi(self):
        if self.costs == 0:
            return 0
        return (self.net_profit() / self.costs) * 100
