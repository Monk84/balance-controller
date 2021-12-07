import const
from dataManager import DataManager
from depositBalance import DepositBalance
from notification import Notification
from paymentsBalance import PaymentsBalance
from regularOperation import RegularOperation
from regularOperationType import RegularOperationType
from datetime import date, timedelta, datetime
from notification import Notification

DB = DataManager()


class BusinessEntity:
    # regularOperations = []
    # regularOperationTypes = [] -- why?

    def __init__(self):
        # getting operation types
        self.regularOperationTypes = []
        all_types = DB.get_operation_types()
        for op_type in all_types:
            # we do not use op_type in RegularOperationType __init__
            new_op_type = RegularOperationType(op_type["name"], const.REG_OP_STATUS_ACTIVE)
            if not op_type["active"]:
                new_op_type.delete()
            self.regularOperationTypes.append(new_op_type)

        # getting active regular operations
        self.regularOperations = []
        active_operations = DB.get_active_regular_operations()
        for operation in active_operations:
            # searching for RegularOperationType
            for op_type in self.regularOperationTypes:
                if op_type.name == operation["reg_op_type"]:
                    # building dates and RegularOperation
                    period = timedelta(days=float(operation["period"]))   # IMPORTANT FORMAT OF TIMEDELTA
                    notification_period = timedelta(days=operation["notification_period"]) # IMPORTANT FORMAT OF TIMEDELTA
                    start_date = date(
                        year=int(operation["start_date"][:4]),
                        month=int(operation["start_date"][5:7]),
                        day=int(operation["start_date"][8:]))
                    new_reg_op = RegularOperation(operation["name"], op_type, operation["payment_amount"], period, notification_period, start_date)
                    self.regularOperations.append({"id": operation["id"], "operation": new_reg_op})

        # getting current balances on init
        cur_dep_balance = DB.get_deposit_balance()
        self.deposit_balance = DepositBalance(cur_dep_balance)
        cur_paym_balance = DB.get_paymenst_balance()
        self.payments_balance = PaymentBalance(cur_paym_balance)

    def add_regular_operation(self, name, reg_op_type, payment_amount, period, notification_period, start_date):
        new_reg = RegularOperation(name, reg_op_type, payment_amount, period, notification_period, start_date)
        if not isinstance(new_reg, RegularOperation):
            return
        new_id = DB.add_regular_operation(new_reg)
        self.regularOperations.append({"id": new_id, "operation": new_reg})

    def change_regular_operation(self, operation_id, name, reg_op_type, payment_amount, period, notification_period):
        for operation in self.regularOperations:
            if operation["id"] == operation_id:
                operation["operation"].update(name, reg_op_type, payment_amount, period, notification_period)
                DB.change_regular_operation(operation)
                return

    def remove_regular_operation(self, selected_id):
        for op in self.regularOperations:
            if op["id"] == selected_id:
                operation["operation"].delete()
                DB.remove_regular_operation(op)
                self.regularOperations.pop(i)
                return True
        return False

    def change_deposit_balance(self, new_balance=0):
        if not isinstance(new_balance, int):
            raise TypeError("PaymentBalance: expected int for new_limit")
            return
        self.deposit_balance.balance.set_balance(new_balance)
        DB.change_deposit_balance(new_balance)

    def form_statistics_by_period(self, tag, start_date, end_date):
        if not isinstance(tag, str):
            raise TypeError("form_statistics_by_period(): expected str for tag")
            return
        if not isinstance(start_date, str):
            raise TypeError("form_statistics_by_period(): expected str for start_date")
            return
        if not isinstance(end_date, str):
            raise TypeError("form_statistics_by_period(): expected str for end_date")
            return
        history = DB.get_operations_history_by_operation_type(tag, start_date, end_date)
        total_income = 0
        total_spend = 0
        for operation in history:
            if operation.price < 0:
                total_spend += operation.price
            else:
                total_income += operation.price
        return {"total_income": total_income, "total_spend": total_spend, "start_date": start_date, "end_date": end_date}

    def add_regular_operation_type(self, name):
        # search for exists op types(even deleted)
        for op_type in self.regularOperationTypes:
            if op_type.name == name:
                # found exist one
                op_type.add()
                DB.activate_operation_type(op_type)
                return
        # adding a new one
        new_type = RegularOperationType(name, True)
        if not isinstance(new_type, RegularOperationType):
            return
        self.regularOperationTypes.append(new_type)
        DB.add_operation_type(new_type)
        return
        
    
    def remove_regular_operation_type(self, name):
        # search for exists op types(even deleted)
        for op_type in self.regularOperationTypes:
            if op_type.name == name:
                # found exist one
                op_type.delete()
                DB.deactivate_operation_type(op_type)
                return
        # adding a new one
        new_type = RegularOperationType(name, True)
        if not isinstance(new_type, RegularOperationType):
            return
        self.regularOperationTypes.append(new_type)
        DB.add_operation_type(new_type)
        return
    
    def send_notification(self, notification_format, notification_type):
        current_notify = Notification(notification_format, notification_type)
        if current_notify != "":
            return { "message" : current_notify}
        else:
            raise ValueError("Check notification format and data")

    #TODO после обсуждения оставить одну из фунок

    def get_period_of_operations(self):
        return [number for number in range(1, 32)]
    
    # -----------#
    # def get_period_of_operations_modes(self):
    #     """
    #     Get list of available peroiod settings. Ex., 'period: 1, day: 2021.12.12' in month mode means that every 
    #     month in the 12 day of the month
    #     """
    #     # TODO настройки платежей не сохраняем же в бд?
    #     # TODO в конструкторе операций период - это промежуток в количестве дней между оплатой. В месяце мб 28/29/30/31 день
    #     # -> может сместиться дата платежа, что мб критично для некоторых видов. Как тогда считать платеж? 
    #     mode = {}
    #     mode["day_mode"] = {"period": 1, "day": datetime.now()} # TODO какой формат времени будем использовать?
    #     mode["week_mode"] = {"period": 1, "day": datetime.now()} 
    #     mode["month_mode"] = {"period": 1, "day": datetime.now()} 
    #     mode["year_mode"] = {"period": 1, "day": datetime.now()} 
    #     return mode
    # -----------#
        
    # TODO обработать выбор параметра периодичности == сохранить в базу, обновить объект класса 
    # или это обновить стейт приложения на фронте ? 
    def set_period_of_operations(self, current_regular_operation_id, new_period):
        index = None
        for i in range(len(self.regularOperations)):
            if self.regularOperations[i]["id"] == current_regular_operation_id:
                index = i
                break
        
        if not index:
            raise ValueError("set_period_of_operations() can't find operation with such id")
       
        if isinstance(new_period, int): #TODO на чем условимся: что передаем: как строку или как инт сразу?
                if new_period <= 0:
                   raise TypeError("set_period_of_operations() needs positive integer value of the period") 
        try:
            if str(new_period).isdigit():
                if new_period <= 0:
                   raise TypeError("set_period_of_operations() needs positive integer value of the period") 
                new_period = int(new_period)
        except Exception as err:
            print(err)
            raise TypeError("set_period_of_operations() invalid period format") 

        try:
            self.regularOperations[index].update(period=new_period)
        except:
            raise ValueError("set_period_of_operations() can't update value of the period in the object RegularOperation")
        
        try:
            DB.change_regular_operation({"id": self.regularOperations[index]["id"], "operation": self.regularOperations[index]})
        except Exception as err:
            raise ValueError("set_period_of_operations() can't update value of the period in the db")
        return {"message": "Successfully update period"}


    # -----------#
    # def set_period_of_operations_with_mode(self, current_regular_operation, new_period, mode):
    #     if not isinstance(current_regular_operation, RegularOperation):
    #         return {"message": False}
    #     if mode =="day_mode":
    #         if isinstance(new_period, int): #TODO на чем условимся: что передаем: как строку или как инт сразу?
    #                 if new_period <= 0:
    #                     return {"message": "Set positive period"} #TODO как обрабатываем исключения и ошибки? 
    #         try:
    #             if str(new_period).isdigit():
    #                 if new_period <= 0:
    #                     return {"message": "Set positive period"} #TODO как обрабатываем исключения и ошибки? 
    #                 new_period = int(new_period)
    #         except TypeError as err:
    #             return {"message": err}
    #         current_regular_operation.update(period=new_period)
    #         return True
    #     # TODO а тут непонятно. так как тогда обращаться к дате совершения операции и чекать эта неделя или следующая или нет..... ?
    #     if mode =="week_mode":
    #         pass
    #     if mode =="month_mode":
    #         pass
    #     if mode =="year_mode":
    #         pass        
    # -----------#


    def get_operation_types(self):
        return DB.get_operation_types()


    def set_operation_type(self, operation_id, type):
        index = None 
        for i in range(len(self.regularOperations)):
            if self.regularOperations[i]["id"] == operation_id:
                index = i
                break
        
        if not index:
            raise ValueError("set_operation_type() can't find such operation")
        
        try:
            self.regularOperations[index].update(reg_op_type=type)
        except Exception:
            raise ValueError("set_operation_type() can't update type in the RegularOperation object")
        
        try:
           DB.change_regular_operation({"id": self.regularOperations[index]["id"], "operation": self.regularOperations[index]})
        except Exception:
            raise ValueError("set_operation_type() can't update type in the the database")
        return {"message": "Successfully update type"}


    def get_notifications_settings(self, operation_id):
        index = None
        for i in range(len(self.regularOperations)):
            if self.regularOperations[i]["id"] == operation_id:
                index = i
                break
        
        if not index:
            raise ValueError("set_operation_type() can't find such operation")
        
        operation = self.regularOperations[index].get()
        return { 
            'period': operation.period,
            'notification_period': operation.notification_period,
            'start_date': operation.start_date
        }
    

    # TODO параметры те? 
    def update_notification_settings(self, operation_id, period= None, notification_period = None):
        index = None
        for i in range(len(self.regularOperations)):
            if self.regularOperations[i]["id"] == operation_id:
                index = i
                break
        
        if not index:
            raise ValueError("set_operation_type() can't find such operation")
        
        try:
            self.regularOperations[index].update(period=period, notification_period=notification_period)
        except:
            raise ValueError("update_notification_settings(): can't update RegularOperation notification settings")
        
        try:
           DB.change_regular_operation({"id": self.regularOperations[index]["id"], "operation": self.regularOperations[index]})
        except Exception:
            raise ValueError("set_operation_type() can't update notification settings in the the database")
        
        return {"message": "Successfully update notification settings"}
    

    def execute_operation(self, operation):
        self.deposit_balance = self.deposit_balance - operation.payment_amount
        try:
            DB.change_deposit_balance(self.deposit_balance)
        except:
            raise ValueError("execute_operation() can't update deposit balance")
        return {"message": "Successfully updated deposit balance"}
    
    # TODO надо ли сравнивать со значением в бд на всякий случай?
    def get_balance(self):
        return self.deposit_balance

    def show_operations(self):
        ops_to_sort = []
        today = datetime.date.today()
        for op in self.regularOperations:
            op_attrs = op['operation'].get()
            start_date = op_attrs['start_date']
            period = op_attrs['period']
            i = 0
            while today > start_date + period * i:
                i += 1
            ops_to_sort += [(today - (start_date + period * (i - 1)).days, op)]
        return sorted(ops_to_sort, key=lambda x : x[1])
    
    def set_payments_limit(self, new_limit=None, new_period=None):
        self.payments_balance.update(new_limit, new_period)
    
    def set_balance_limit(self, new_limit=None, new_period=None):
        self.deposit_balance.update(new_limit, new_period)
    
    def daily_check(self):
        if self.deposit_balance.apply_reg_ops(self.regularOperations):
            print(self.deposit_balance.get_notification().get_notification())
        DB.set_deposit_balance(self.deposit_balance.get_balance())
        
        if self.payments_balance.apply_reg_ops(self.regularOperations):
            print(self.payments_balance.get_notification().get_notification())
        DB.set_payments_balance(self.payments_balance.get_balance())

    def secret_menu_recovery(self, operations_to_recover):
        for op in operations_to_recover:
            DB.activate_regular_operation(op)
            op.add()
    
    # TODO как отозвать операции? где функи
    # TODO в базе должна храниться дата последнего совершения операции.. чекнуть