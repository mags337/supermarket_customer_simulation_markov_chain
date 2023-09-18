# Writing a Supermarket class
from datetime import datetime

class Supermarket:
    
    def __init__(self, time, name = "LIDL"):
        '''
        initialize:
        1. customers list with all the active customers (!= "checkout")
        2. name of the Supermarket
        3. amount of custumers entering the supermarket. random number between 0 and 5.
        4. total time of observation in minutes
        5. customer number before store opens = 0
        6. create dataframe with the colums: time, customer_no, location
        '''
        self.customers_list = []
        self.name = name

        self.customers_in = np.arange(random.randint(0,5))
        self.observation_time = np.arange(30)                      
        self.initial_time = time  
                                     
        self.customer_no = 0
        self.df_doc = pd.DataFrame(columns = ["time", "customer_no", "location"])

    def add_customer(self):
        ''' 
        add new customers entering the store the the customers list and give them a number
        '''
        for i in self.customers_in:
            self.customer_no +=1
            cust = Customer(self.customer_no)
            self.customers_list.append(cust)

                
    def customer_state_update(self, probs):
        self.initial_time += pd.DateOffset(minutes = 1)
        for i in self.customers_list:
            i.next_state(probs)

    def rm_customer(self):
        '''
        remove the customers from the customers list, if they have already reached the "checkout" area
        '''
        for i in self.customers_list:
            if i.state == "checkout":
                self.customers_list.remove(i)
    
    def update_minutes(self, probs):
        '''
        Over the length of the observation time (here 20 minutes), update the information every minute of the:
        1. current customer state
        2. add the customer to the customer list
        3. print all customers with the current time and id in CSV format into a dataframe
        4. remove all customers from the customer list, if the have already reached the "checkout" area
        '''
        for i in self.observation_time:
            self.customer_state_update(probs)
            self.add_customer()
            self.print_customers()
            self.rm_customer()

    def print_customers(self):
        """print all customers with the current time and id in CSV format into a dataframe. 
        """
        for i in self.customers_list:
            new_series = pd.Series({"time": self.initial_time, "customer_no": i.id, "location": i.state})
            self.df_doc = pd.concat([self.df_doc, new_series.to_frame().T], ignore_index=True)

    def simulation(self, probs):
        '''
        1. adds first customers to the store
        2. save the first customers in the dataframe
        3. updates the customers every minute and adds them to the dataframe. If customers are in "checkout", they will be removed from the customers list
        4. print all customers with the current time and id in CSV format into the dataframe.
        5. save all the updates in a csv file
        '''
        store.add_customer() 
        store.print_customers() 
        store.update_minutes(probs) 
        store.print_customers()
        self.df_doc.to_csv("supermarket_simulation.csv", index=False) 
        print(store.df_doc)

store = Supermarket(datetime.now())
store.simulation(probs)