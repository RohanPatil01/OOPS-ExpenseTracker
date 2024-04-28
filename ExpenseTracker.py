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
        self.__record_settlement()
        self.__optimize_settlement()
        
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
            
    def __record_settlement(self):
        settlement_data = []
        grouped = self.final_paid_by_df.groupby(['payer', 'receivers'])
        for (payer, receiver), group in grouped:
            if payer != receiver:
                amount_owed = group['amount'].sum()
                settlement_data.append({'Name': payer, "Who'll pay": receiver, 'Amount': amount_owed})
                
        self.settlement_df = pd.DataFrame(settlement_data)
        

    def __optimize_settlement(self):
        amount = list(self.settlement_df["Amount"])
        payers = list(self.settlement_df["Name"])
        receivers = list(self.settlement_df["Who'll pay"])
    
        pairs = []
        for i, payer in enumerate(payers):
            for j, receiver in enumerate(receivers):
                if i == j:
                    pairs.append([payer, receiver])
    
        similar_pairs_indices = []
        for i, pair1 in enumerate(pairs):
            for j, pair2 in enumerate(pairs):
                if i < j and set(pair1) == set(pair2):
                    similar_pairs_indices.append((i, j))
    
        for i in similar_pairs_indices:
            if amount[i[0]] < amount[i[1]]:
                amount[i[1]] -= amount[i[0]]
                amount[i[0]] = 0
            elif amount[i[0]] == amount[i[1]]:
                amount[i[0]] = 0
                amount[i[1]] = 0
            else:
                amount[i[0]] -= amount[i[1]]
                amount[i[1]] = 0
    
        optimized_settlement_data = ({'Name': payers, "Who'll pay": receivers, 'Amount': amount})
  
    
        self.optimized_settlement_df = pd.DataFrame(optimized_settlement_data)

        with pd.ExcelWriter('ExpenseTracker.xlsx') as writer:
            self.final_transactions_df.to_excel(writer, sheet_name='Transactions', index=False)
            self.final_paid_by_df.to_excel(writer, sheet_name='PaidBy', index=False)
            self.balance_sheet_df.to_excel(writer, sheet_name='BalanceSheet', index=True)
            self.settlement_df.to_excel(writer, sheet_name='Settlement', index=False)
            self.optimized_settlement_df.to_excel(writer, sheet_name='OptimizedSettlement', index=False)
    

    def show_transaction(self):
        return self.current_transactions_df

    def show_paid_by(self):
        return self.current_paid_by_df

    def show_balance_sheet(self):
        return self.balance_sheet_df

    def show_settlement(self):
        return self.settlement_df
        
    def show_history(self):
        return self.final_transactions_df
        
    def show_paid_by_history(self):
        return self.final_paid_by_df