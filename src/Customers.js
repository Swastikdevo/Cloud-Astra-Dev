```javascript
import React, { useState, useEffect } from 'react';

const CustomerManager = () => {
  const [customers, setCustomers] = useState([]);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  
  const fetchCustomers = async () => {
    const response = await fetch('/api/customers');
    const data = await response.json();
    setCustomers(data);
  };

  const addCustomer = async () => {
    const newCustomer = { name, email };
    await fetch('/api/customers', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newCustomer),
    });
    fetchCustomers();
    setName('');
    setEmail('');
  };

  useEffect(() => {
    fetchCustomers();
  }, []);

  return (
    <div>
      <h2>Customer Management</h2>
      <input 
        type="text" 
        placeholder="Name" 
        value={name} 
        onChange={(e) => setName(e.target.value)} 
      />
      <input 
        type="email" 
        placeholder="Email" 
        value={email} 
        onChange={(e) => setEmail(e.target.value)} 
      />
      <button onClick={addCustomer}>Add Customer</button>
      <ul>
        {customers.map((customer) => (
          <li key={customer.id}>{customer.name} - {customer.email}</li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManager;
```