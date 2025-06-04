```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });
  const [filter, setFilter] = useState('');

  useEffect(() => {
    fetch('/api/customers')
      .then(response => response.json())
      .then(data => setCustomers(data));
  }, []);

  const handleAddCustomer = () => {
    const customerData = { ...newCustomer };
    fetch('/api/customers', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(customerData),
    })
      .then(response => response.json())
      .then(data => {
        setCustomers([...customers, data]);
        setNewCustomer({ name: '', email: '' });
      });
  };

  const filteredCustomers = customers.filter(customer =>
    customer.name.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <div>
      <h1>Customer Management</h1>
      <input
        type="text"
        placeholder="Filter by name"
        value={filter}
        onChange={e => setFilter(e.target.value)}
      />
      <div>
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
        <button onClick={handleAddCustomer}>Add Customer</button>
      </div>
      <ul>
        {filteredCustomers.map(customer => (
          <li key={customer.id}>{customer.name} - {customer.email}</li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```