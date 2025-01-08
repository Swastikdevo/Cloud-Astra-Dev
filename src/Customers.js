```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
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

  const addCustomer = () => {
    const updatedCustomers = [...customers, { name: newCustomer }];
    setCustomers(updatedCustomers);
    setNewCustomer('');
  };

  return (
    <div>
      <h1>Customer Management</h1>
      <input 
        type="text" 
        value={newCustomer} 
        onChange={(e) => setNewCustomer(e.target.value)} 
        placeholder="Add new customer"
      />
      <button onClick={addCustomer}>Add Customer</button>
      <ul>
        {customers.map((customer, index) => (
          <li key={index}>{customer.name}</li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```