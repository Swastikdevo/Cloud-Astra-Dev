```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [filter, setFilter] = useState('');
  const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });
  
  useEffect(() => {
    fetchCustomers();
  }, []);

  const fetchCustomers = async () => {
    const response = await fetch('/api/customers');
    const data = await response.json();
    setCustomers(data);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewCustomer((prev) => ({ ...prev, [name]: value }));
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
    customer.name.toLowerCase().includes(filter.toLowerCase()));

  return (
    <div>
      <h2>Customer Management</h2>
      <input 
        type="text" 
        placeholder="Filter by name" 
        value={filter}
        onChange={(e) => setFilter(e.target.value)}
      />
      <h3>Add New Customer</h3>
      <input 
        name="name" 
        placeholder="Name" 
        value={newCustomer.name} 
        onChange={handleInputChange} 
      />
      <input 
        name="email" 
        placeholder="Email" 
        value={newCustomer.email} 
        onChange={handleInputChange} 
      />
      <button onClick={addCustomer}>Add Customer</button>
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