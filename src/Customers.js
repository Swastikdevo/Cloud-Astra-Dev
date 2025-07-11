```javascript
import React, { useState } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [newCustomer, setNewCustomer] = useState('');

  const addCustomer = () => {
    if (newCustomer.trim()) {
      setCustomers([...customers, newCustomer]);
      setNewCustomer('');
    }
  };

  const removeCustomer = (index) => {
    const updatedCustomers = customers.filter((_, i) => i !== index);
    setCustomers(updatedCustomers);
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
          <li key={index}>
            {customer}
            <button onClick={() => removeCustomer(index)}>Remove</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```