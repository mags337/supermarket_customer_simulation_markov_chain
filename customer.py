# Writing a customer class
import random

class Customer:
    
    def __init__(self, id, state="entrance"):
        self.state = state 
        self.id = id
 
    def __repr__(self):
        return f'<Customer is at {self.state}>'

    def next_state(self, transition_matrix_probs):
        state_probs = transition_matrix_probs[self.state]
        self.state = random.choices(['spices', 'drinks', 'fruit', 'dairy', 'checkout'], weights = state_probs)[0]
        return f'The customer in going to the {self.state} aile'

cust1 = Customer(1)

print(cust1)
print(cust1.next_state(probs))