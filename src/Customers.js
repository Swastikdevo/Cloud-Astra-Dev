```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });

  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch('/api/customers');
      const data = await response.json();
      setCustomers(data);
    };
    fetchData();
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

  const handleInputChange = (e) => {
    setNewCustomer({ ...newCustomer, [e.target.name]: e.target.value });
  };

  return (
    <div>
      <h1>Customer Management</h1>
      <input 
        type="text" 
        name="name" 
        value={newCustomer.name} 
        onChange={handleInputChange} 
        placeholder="Customer Name" 
      />
      <input 
        type="email" 
        name="email" 
        value={newCustomer.email} 
        onChange={handleInputChange} 
        placeholder="Customer Email" 
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

export default CustomerManagement;
```