from datetime import datetime
import pandas as pd

class ExpenseTracker:


    def __init__(self, payer, receiver_count, amount, reason, timestamp = datetime.now().strftime("%B %d, %Y %H:%M")):
        self.timestamp = timestamp
        self.payer = payer
        self.receiver_count = receiver_count
        self.amount = amount
        self.reason = reason
        self.receivers = {}
        for i in range(1, receiver_count+1):
            receiver = input(f"Enter receiver number {i}:")
            self.receivers[receiver] = self.amount / self.receiver_count #To allocate money to each receiver after dividing
            
    def __str__(self):
        return "Transaction recorded successfully!"

    
    @staticmethod
    def record():
        transactions_df = pd.read_excel('ExpenseTracker.xlsx', sheet_name='transactions')
        dict = {"timestamp":[self.timestamp], "payer" : [self.payer], "receivers" : [self.receivers.keys()],
                "amount" : [self.amount], "reason" : [self.reason] }
        new_transactions_df = pd.DataFrame(dict)
        new_transactions_df['receivers'] = new_transactions_df['receivers'].apply(lambda x: tuple(x))
        
        final_transactions_df = pd.concat([transactions_df, new_transactions_df]).reset_index(drop=True)


        paid_by_df = pd.read_excel('ExpenseTracker.xlsx', sheet_name='paid_by')
        
        paid_by_dict = {"timestamp":[self.timestamp for _ in range(self.receiver_count)], 
                        "payer" : [self.payer for _ in range(self.receiver_count)], 
                        "receivers" : list(self.receivers.keys()),
                        "amount" : list(self.receivers.values()), 
                        "reason" : [self.reason for _ in range(self.receiver_count)] }
        
        new_paid_by_df = pd.DataFrame(paid_by_dict)
        final_paid_by_df = pd.concat([paid_by_df, new_paid_by_df]).reset_index(drop=True)


        balance_sheet = pd.read_excel('ExpenseTracker.xlsx', sheet_name='balance_sheet',index_col="payer")
        
        new_balance_sheet = self.paid_by().pivot_table(index="payer",
                                                   columns=("receivers"),
                                                   values="amount",
                                                   aggfunc="sum",
                                                   margins="True")
        final_balance_sheet = pd.concat([balance_sheet, new_balance_sheet]).reset_index(drop=True)


        with pd.ExcelWriter('ExpenseTracker.xlsx') as writer:
            obj.show().to_excel(writer, sheet_name='transactions', index=False)
            obj.paid_by().to_excel(writer, sheet_name='paid_by', index=False)
            obj.balance_sheet().to_excel(writer, sheet_name='balance_sheet')
        
    def show(self):

        return final_transactions_df
        

    def paid_by(self):

        return final_paid_by_df

    def balance_sheet(self):
        
        return final_balance_sheet

obj1 = ExpenseTracker("Rohan",3,450,"Movie")
print(obj1)
obj1.show()

obj2 = ExpenseTracker("Sid",2,30,"Train Ticket")
print(obj2)
obj2.show()

obj3 = ExpenseTracker("Rohan",2,20,"Juice")
print(obj3)
obj3.show()