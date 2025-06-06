```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });

  useEffect(() => {
    fetch('/api/customers')
      .then(response => response.json())
      .then(data => setCustomers(data));
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewCustomer({ ...newCustomer, [name]: value });
  };

  const addCustomer = () => {
    fetch('/api/customers', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newCustomer),
    })
      .then(response => response.json())
      .then(data => {
        setCustomers([...customers, data]);
        setNewCustomer({ name: '', email: '' });
      });
  };

  const removeCustomer = (id) => {
    fetch(`/api/customers/${id}`, { method: 'DELETE' })
      .then(() => setCustomers(customers.filter(c => c.id !== id)));
  };

  return (
    <div>
      <h2>Customer Management</h2>
      <input 
        name="name" 
        value={newCustomer.name} 
        onChange={handleInputChange} 
        placeholder="Customer Name" 
      />
      <input 
        name="email" 
        value={newCustomer.email} 
        onChange={handleInputChange} 
        placeholder="Customer Email" 
      />
      <button onClick={addCustomer}>Add Customer</button>
      <ul>
        {customers.map(customer => (
          <li key={customer.id}>
            {customer.name} - {customer.email}
            <button onClick={() => removeCustomer(customer.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```