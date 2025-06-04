```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });
  
  useEffect(() => {
    fetch('/api/customers')
      .then(response => response.json())
      .then(data => setCustomers(data));
  }, []);

  const addCustomer = () => {
    fetch('/api/customers', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newCustomer),
    })
      .then(response => response.json())
      .then(data => setCustomers([...customers, data]))
      .finally(() => setNewCustomer({ name: '', email: '' }));
  };

  return (
    <div>
      <h2>Customer Management</h2>
      <ul>
        {customers.map(customer => (
          <li key={customer.id}>{customer.name} - {customer.email}</li>
        ))}
      </ul>
      <input
        type="text"
        placeholder="Name"
        value={newCustomer.name}
        onChange={e => setNewCustomer({ ...newCustomer, name: e.target.value })}
      />
      <input
        type="email"
        placeholder="Email"
        value={newCustomer.email}
        onChange={e => setNewCustomer({ ...newCustomer, email: e.target.value })}
      />
      <button onClick={addCustomer}>Add Customer</button>
    </div>
  );
};

export default CustomerManagement;
```