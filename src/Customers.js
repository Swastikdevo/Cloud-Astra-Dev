```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [customerName, setCustomerName] = useState('');
  
  useEffect(() => {
    fetch('/api/customers')
      .then(response => response.json())
      .then(data => setCustomers(data));
  }, []);
  
  const addCustomer = () => {
    const newCustomer = { name: customerName };
    fetch('/api/customers', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newCustomer)
    })
    .then(response => response.json())
    .then(data => {
      setCustomers([...customers, data]);
      setCustomerName('');
    });
  };

  const deleteCustomer = (id) => {
    fetch(`/api/customers/${id}`, { method: 'DELETE' })
      .then(() => setCustomers(customers.filter(customer => customer.id !== id)));
  };

  return (
    <div>
      <h1>Customer Management</h1>
      <input 
        type="text" 
        value={customerName} 
        onChange={(e) => setCustomerName(e.target.value)}
        placeholder="Enter customer name" 
      />
      <button onClick={addCustomer}>Add Customer</button>
      <ul>
        {customers.map(customer => (
          <li key={customer.id}>
            {customer.name}
            <button onClick={() => deleteCustomer(customer.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```