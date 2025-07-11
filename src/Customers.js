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
      .then(data => {
        setCustomers([...customers, data]);
        setNewCustomer({ name: '', email: '' });
      });
  };

  const handleChange = (e) => {
    setNewCustomer({ ...newCustomer, [e.target.name]: e.target.value });
  };

  return (
    <div>
      <h2>Customer Management</h2>
      <input
        type="text"
        name="name"
        value={newCustomer.name}
        onChange={handleChange}
        placeholder="Customer Name"
      />
      <input
        type="email"
        name="email"
        value={newCustomer.email}
        onChange={handleChange}
        placeholder="Customer Email"
      />
      <button onClick={addCustomer}>Add Customer</button>
      <ul>
        {customers.map(customer => (
          <li key={customer.id}>{customer.name} - {customer.email}</li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```