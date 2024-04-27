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
        self.current_transactions_df = pd.DataFrame(data)  

        try:
            old_transactions_df = pd.read_excel('ExpenseTracker.xlsx', sheet_name='Transactions')
        except:
            old_transactions_df = None
                
        self.final_transactions_df = pd.concat([old_transactions_df, self.current_transactions_df]).reset_index(drop=True)
        

    def __record_paid_by(self):
        
        self.current_paid_by_df = self.current_transactions_df.explode('receivers')
        self.current_paid_by_df['amount'] = self.amount / len(self.receivers)

        try:
            old_paid_by_df = pd.read_excel('ExpenseTracker.xlsx', sheet_name='PaidBy')
        except:
            old_paid_by_df = None
                
        self.final_paid_by_df = pd.concat([old_paid_by_df, self.current_paid_by_df]).reset_index(drop=True)
        
        
    def __record_balance_sheet(self):
        self.balance_sheet_df = self.final_paid_by_df.pivot_table(
                                    index="payer",
                                    columns=("receivers"),
                                    values="amount",
                                    aggfunc="sum",
                                    margins=True
                            )
        
        with pd.ExcelWriter('ExpenseTracker.xlsx') as writer:
            self.final_transactions_df.to_excel(writer, sheet_name='Transactions', index=False)
            self.final_paid_by_df.to_excel(writer, sheet_name='PaidBy', index=False)
            self.balance_sheet_df.to_excel(writer, sheet_name='BalanceSheet', index=True)
            
        

    def show_transactions(self):
        return self.current_transactions_df

    def show_paid_by(self):
        return self.current_paid_by_df

    def show_balance_sheet(self):
        return self.balance_sheet_df

    def show_history(self):
        return self.final_transactions_df
        
    def show_paid_by_history(self):
        return self.final_paid_by_df