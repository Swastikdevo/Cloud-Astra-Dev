```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });
  const [filter, setFilter] = useState('');

  useEffect(() => {
    fetchCustomers();
  }, []);

  const fetchCustomers = async () => {
    const response = await fetch('/api/customers');
    const data = await response.json();
    setCustomers(data);
  };

  const handleInputChange = (e) => {
    setNewCustomer({ ...newCustomer, [e.target.name]: e.target.value });
  };

  const addCustomer = async () => {
    const response = await fetch('/api/customers', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newCustomer),
    });
    if (response.ok) {
      fetchCustomers();
      setNewCustomer({ name: '', email: '' });
    }
  };

  const filteredCustomers = customers.filter(customer => 
    customer.name.toLowerCase().includes(filter.toLowerCase())
  );

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
      <input 
        type="text" 
        value={filter} 
        onChange={(e) => setFilter(e.target.value)} 
        placeholder="Filter Customers" 
      />
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