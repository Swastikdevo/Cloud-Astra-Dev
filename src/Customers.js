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

  const deleteCustomer = (id) => {
    setCustomers(customers.filter(customer => customer.id !== id));
  };

  return (
    <div>
      <h2>Customer Management</h2>
      <input 
        type="text" 
        value={name} 
        placeholder="Customer Name" 
        onChange={(e) => setName(e.target.value)} 
      />
      <input 
        type="email" 
        value={email} 
        placeholder="Customer Email" 
        onChange={(e) => setEmail(e.target.value)} 
      />
      <button onClick={addCustomer}>Add Customer</button>
      <ul>
        {customers.map(customer => (
          <li key={customer.id}>
            {customer.name} - {customer.email} 
            <button onClick={() => deleteCustomer(customer.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```