```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [filter, setFilter] = useState('');
  const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });

  useEffect(() => {
    const fetchCustomers = async () => {
      const response = await fetch('/api/customers');
      const data = await response.json();
      setCustomers(data);
    };
    fetchCustomers();
  }, []);

  const addCustomer = async () => {
    const response = await fetch('/api/customers', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newCustomer),
    });
    const data = await response.json();
    setCustomers([...customers, data]);
    setNewCustomer({ name: '', email: '' });
  };

  const handleChange = (e) => setNewCustomer({ ...newCustomer, [e.target.name]: e.target.value });

  const filteredCustomers = customers.filter(customer =>
    customer.name.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <div>
      <input
        type="text"
        placeholder="Filter customers"
        value={filter}
        onChange={(e) => setFilter(e.target.value)}
      />
      <ul>
        {filteredCustomers.map(customer => (
          <li key={customer.id}>{customer.name} - {customer.email}</li>
        ))}
      </ul>
      <input
        type="text"
        name="name"
        placeholder="Customer Name"
        value={newCustomer.name}
        onChange={handleChange}
      />
      <input
        type="email"
        name="email"
        placeholder="Customer Email"
        value={newCustomer.email}
        onChange={handleChange}
      />
      <button onClick={addCustomer}>Add Customer</button>
    </div>
  );
};

export default CustomerManagement;
```