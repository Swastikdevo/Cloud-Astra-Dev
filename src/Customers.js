```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
  const [customers, setCustomers] = useState([]);
  const [newCustomer, setNewCustomer] = useState('');

  useEffect(() => {
    const fetchCustomers = async () => {
      const response = await fetch('/api/customers');
      const data = await response.json();
      setCustomers(data);
    };
    fetchCustomers();
  }, []);

  const handleAddCustomer = async () => {
    const response = await fetch('/api/customers', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: newCustomer }),
    });
    const addedCustomer = await response.json();
    setCustomers([...customers, addedCustomer]);
    setNewCustomer('');
  };

  const handleDeleteCustomer = async (id) => {
    await fetch(`/api/customers/${id}`, { method: 'DELETE' });
    setCustomers(customers.filter(customer => customer.id !== id));
  };

  return (
    <div>
      <h2>Customer Management</h2>
      <input 
        type="text" 
        value={newCustomer} 
        onChange={(e) => setNewCustomer(e.target.value)} 
        placeholder="Add new customer" 
      />
      <button onClick={handleAddCustomer}>Add</button>
      <ul>
        {customers.map(customer => (
          <li key={customer.id}>
            {customer.name} <button onClick={() => handleDeleteCustomer(customer.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerList;
```