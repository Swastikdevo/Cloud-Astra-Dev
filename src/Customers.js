```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [status, setStatus] = useState('active');

  useEffect(() => {
    fetch('/api/customers')
      .then(response => response.json())
      .then(data => setCustomers(data));
  }, []);

  const addCustomer = () => {
    const newCustomer = { name, email, status };
    fetch('/api/customers', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newCustomer),
    })
      .then(response => response.json())
      .then(data => setCustomers(prev => [...prev, data]));
    setName('');
    setEmail('');
  };

  const deleteCustomer = (id) => {
    fetch(`/api/customers/${id}`, {
      method: 'DELETE',
    }).then(() => setCustomers(customers.filter(customer => customer.id !== id)));
  };

  return (
    <div>
      <h1>Customer Management</h1>
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
      <select value={status} onChange={(e) => setStatus(e.target.value)}>
        <option value="active">Active</option>
        <option value="inactive">Inactive</option>
      </select>
      <button onClick={addCustomer}>Add Customer</button>
      <ul>
        {customers.map(customer => (
          <li key={customer.id}>
            {customer.name} - {customer.email} - {customer.status}
            <button onClick={() => deleteCustomer(customer.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```