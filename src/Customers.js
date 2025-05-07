```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });
  const [error, setError] = useState("");

  useEffect(() => {
    fetchCustomers();
  }, []);

  const fetchCustomers = async () => {
    try {
      const response = await fetch('/api/customers');
      const data = await response.json();
      setCustomers(data);
    } catch (err) {
      console.error('Error fetching customers:', err);
    }
  };

  const addCustomer = async () => {
    if (!newCustomer.name || !newCustomer.email) {
      setError("Name and email are required");
      return;
    }
    setError("");
    
    const response = await fetch('/api/customers', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newCustomer),
    });
    
    if (response.ok) {
      fetchCustomers();
      setNewCustomer({ name: '', email: '' });
    }
  };

  return (
    <div>
      <h1>Customer Management</h1>
      <input 
        type="text"
        placeholder="Name"
        value={newCustomer.name}
        onChange={(e) => setNewCustomer({...newCustomer, name: e.target.value})}
      />
      <input 
        type="email"
        placeholder="Email"
        value={newCustomer.email}
        onChange={(e) => setNewCustomer({...newCustomer, email: e.target.value})}
      />
      <button onClick={addCustomer}>Add Customer</button>
      {error && <div style={{color: 'red'}}>{error}</div>}
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