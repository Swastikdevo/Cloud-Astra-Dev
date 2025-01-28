```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });

  useEffect(() => {
    const fetchCustomers = async () => {
      const response = await fetch('/api/customers');
      const data = await response.json();
      setCustomers(data);
    };
    fetchCustomers();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch('/api/customers', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newCustomer),
    });
    const addedCustomer = await response.json();
    setCustomers([...customers, addedCustomer]);
    setNewCustomer({ name: '', email: '' });
  };

  return (
    <div>
      <h2>Customer List</h2>
      <ul>
        {customers.map((customer) => (
          <li key={customer.id}>{customer.name} - {customer.email}</li>
        ))}
      </ul>
      <form onSubmit={handleSubmit}>
        <input 
          type="text" 
          placeholder="Customer Name" 
          value={newCustomer.name} 
          onChange={(e) => setNewCustomer({ ...newCustomer, name: e.target.value })} 
          required 
        />
        <input 
          type="email" 
          placeholder="Customer Email" 
          value={newCustomer.email} 
          onChange={(e) => setNewCustomer({ ...newCustomer, email: e.target.value })} 
          required 
        />
        <button type="submit">Add Customer</button>
      </form>
    </div>
  );
};

export default CustomerManagement;
```