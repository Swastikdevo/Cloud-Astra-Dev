```javascript
import React, { useState } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  
  const addCustomer = () => {
    setCustomers([...customers, { id: Date.now(), name, email }]);
    setName('');
    setEmail('');
  };

  const removeCustomer = (id) => {
    setCustomers(customers.filter(customer => customer.id !== id));
  };

  return (
    <div>
      <h1>Customer Management System</h1>
      <input 
        type="text" 
        placeholder="Customer Name" 
        value={name} 
        onChange={(e) => setName(e.target.value)} 
      />
      <input 
        type="email" 
        placeholder="Customer Email" 
        value={email} 
        onChange={(e) => setEmail(e.target.value)} 
      />
      <button onClick={addCustomer}>Add Customer</button>
      <ul>
        {customers.map(customer => (
          <li key={customer.id}>
            {customer.name} - {customer.email} 
            <button onClick={() => removeCustomer(customer.id)}>Remove</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```