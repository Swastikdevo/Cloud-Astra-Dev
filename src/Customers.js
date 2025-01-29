```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });

  useEffect(() => {
    // Fetch initial customer data
    const fetchCustomers = async () => {
      const response = await fetch('/api/customers');
      const data = await response.json();
      setCustomers(data);
    };
    fetchCustomers();
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewCustomer((prev) => ({ ...prev, [name]: value }));
  };

  const handleAddCustomer = async () => {
    const response = await fetch('/api/customers', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newCustomer),
    });
    const addedCustomer = await response.json();
    setCustomers((prev) => [...prev, addedCustomer]);
    setNewCustomer({ name: '', email: '' });
  };

  const handleDeleteCustomer = async (id) => {
    await fetch(`/api/customers/${id}`, { method: 'DELETE' });
    setCustomers((prev) => prev.filter((c) => c.id !== id));
  };

  return (
    <div>
      <h2>Customer Management</h2>
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
      <button onClick={handleAddCustomer}>Add Customer</button>
      <ul>
        {customers.map((customer) => (
          <li key={customer.id}>
            {customer.name} - {customer.email}
            <button onClick={() => handleDeleteCustomer(customer.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```