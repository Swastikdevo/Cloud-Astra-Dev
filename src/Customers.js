```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [search, setSearch] = useState('');

  useEffect(() => {
    fetch('/api/customers')
      .then(response => response.json())
      .then(data => setCustomers(data));
  }, []);

  const addCustomer = () => {
    const newCustomer = { name, email };
    fetch('/api/customers', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newCustomer),
    }).then(() => {
      setCustomers([...customers, newCustomer]);
      setName('');
      setEmail('');
    });
  };

  const filteredCustomers = customers.filter(customer =>
    customer.name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div>
      <h1>Customer Management</h1>
      <input
        type="text"
        placeholder="Search customers"
        value={search}
        onChange={e => setSearch(e.target.value)}
      />
      <div>
        <input
          type="text"
          placeholder="Name"
          value={name}
          onChange={e => setName(e.target.value)}
        />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={e => setEmail(e.target.value)}
        />
        <button onClick={addCustomer}>Add Customer</button>
      </div>
      <ul>
        {filteredCustomers.map((customer, index) => (
          <li key={index}>{customer.name} - {customer.email}</li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```