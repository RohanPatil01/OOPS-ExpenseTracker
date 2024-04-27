import pandas as pd
from datetime import datetime

class ExpenseTracker:
    
    def __init__(self, payer, receiver_count, amount, reason, timestamp=None):
        
        if timestamp is None:
            timestamp = datetime.now().strftime("%B %d, %Y %H:%M")
        self.timestamp = timestamp
        self.payer = payer
        self.receiver_count = receiver_count
        self.amount = amount
        self.reason = reason
        self.receivers = []
        for i in range(1, receiver_count+1):
            receiver = input(f"Enter receiver number {i}:")
            self.receivers.append(receiver)
            
        self.__record_transactions()
        self.__record_paid_by()
        self.__record_balance_sheet()
            
    def __str__(self):
        return "Transaction recorded successfully!"
        
    def __record_transactions(self):
        data = {
            "timestamp": [self.timestamp],
            "payer": [self.payer],
            "receivers": [self.receivers],
            "amount": [self.amount],
            "reason": [self.reason]
        }
        self.new_transactions_df = pd.DataFrame(data)        

    def __record_paid_by(self):
        self.paid_by_df = self.new_transactions_df.copy()
        self.paid_by_df = self.paid_by_df.explode('receivers')
        self.paid_by_df['amount'] = self.amount / len(self.receivers)

    def __record_balance_sheet(self):
        self.balance_sheet_df = self.paid_by_df.pivot_table(
                                    index="payer",
                                    columns=("receivers"),
                                    values="amount",
                                    aggfunc="sum",
                                    margins=True
                            )

    def show_transactions(self):
        return self.new_transactions_df

    def show_paid_by(self):
        return self.paid_by_df

    def show_balance_sheet(self):
        return self.balance_sheet_df