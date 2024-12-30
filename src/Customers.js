```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [newCustomer, setNewCustomer] = useState('');

  const fetchCustomers = async () => {
    const response = await fetch('/api/customers');
    const data = await response.json();
    setCustomers(data);
  };

  const handleAddCustomer = () => {
    setCustomers([...customers, { name: newCustomer, id: Date.now() }]);
    setNewCustomer('');
  };

  useEffect(() => {
    fetchCustomers();
  }, []);

  return (
    <div>
      <h1>Customer Management</h1>
      <input
        type="text"
        value={newCustomer}
        onChange={(e) => setNewCustomer(e.target.value)}
        placeholder="Add new customer"
      />
      <button onClick={handleAddCustomer}>Add Customer</button>
      <ul>
        {customers.map((customer) => (
          <li key={customer.id}>{customer.name}</li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```