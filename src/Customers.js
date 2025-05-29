```javascript
import React, { useState } from 'react';

const CustomerList = () => {
  const [customers, setCustomers] = useState([]);
  const [newCustomer, setNewCustomer] = useState('');

  const addCustomer = () => {
    setCustomers([...customers, newCustomer]);
    setNewCustomer('');
  };

  const deleteCustomer = (index) => {
    const updatedCustomers = customers.filter((_, i) => i !== index);
    setCustomers(updatedCustomers);
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
      <button onClick={addCustomer}>Add</button>
      <ul>
        {customers.map((customer, index) => (
          <li key={index}>
            {customer} <button onClick={() => deleteCustomer(index)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerList;
```