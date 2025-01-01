```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });

  const fetchCustomers = async () => {
    const response = await fetch('/api/customers');
    const data = await response.json();
    setCustomers(data);
  };

  useEffect(() => {
    fetchCustomers();
  }, []);

  const addCustomer = async () => {
    await fetch('/api/customers', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newCustomer),
    });
    setNewCustomer({ name: '', email: '' });
    fetchCustomers();
  };

  return (
    <div>
      <h1>Customer Management</h1>
      <form onSubmit={(e) => { e.preventDefault(); addCustomer(); }}>
        <input
          type="text"
          value={newCustomer.name}
          placeholder="Customer Name"
          onChange={(e) => setNewCustomer({ ...newCustomer, name: e.target.value })}
        />
        <input
          type="email"
          value={newCustomer.email}
          placeholder="Customer Email"
          onChange={(e) => setNewCustomer({ ...newCustomer, email: e.target.value })}
        />
        <button type="submit">Add Customer</button>
      </form>
      <ul>
        {customers.map((customer) => (
          <li key={customer.id}>{customer.name} - {customer.email}</li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```