```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchCustomers();
  }, []);

  const fetchCustomers = async () => {
    const response = await fetch('/api/customers');
    const data = await response.json();
    setCustomers(data);
  };

  const addCustomer = async () => {
    await fetch('/api/customers', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newCustomer),
    });
    setNewCustomer({ name: '', email: '' });
    fetchCustomers();
  };

  const filteredCustomers = customers.filter(customer => 
    customer.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div>
      <h1>Customer Management</h1>
      <input 
        type="text" 
        placeholder="Search customers" 
        value={searchTerm} 
        onChange={e => setSearchTerm(e.target.value)} 
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
        <button onClick={addCustomer}>Add Customer</button>
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