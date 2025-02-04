```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
  const [customers, setCustomers] = useState([]);
  const [newCustomer, setNewCustomer] = useState("");

  useEffect(() => {
    fetchCustomers();
  }, []);

  const fetchCustomers = async () => {
    const response = await fetch('/api/customers');
    const data = await response.json();
    setCustomers(data);
  };

  const addCustomer = async () => {
    const response = await fetch('/api/customers', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: newCustomer }),
    });
    const addedCustomer = await response.json();
    setCustomers([...customers, addedCustomer]);
    setNewCustomer("");
  };

  const removeCustomer = async (id) => {
    await fetch(`/api/customers/${id}`, { method: 'DELETE' });
    setCustomers(customers.filter(customer => customer.id !== id));
  };

  return (
    <div>
      <h1>Customer Management</h1>
      <input 
        type="text" 
        value={newCustomer} 
        onChange={(e) => setNewCustomer(e.target.value)} 
        placeholder="Add New Customer"
      />
      <button onClick={addCustomer}>Add</button>
      <ul>
        {customers.map(customer => (
          <li key={customer.id}>
            {customer.name} <button onClick={() => removeCustomer(customer.id)}>Remove</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerList;
```