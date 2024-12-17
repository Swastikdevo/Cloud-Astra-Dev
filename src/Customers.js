```javascript
import React, { useState } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [name, setName] = useState('');
  const [editIndex, setEditIndex] = useState(-1);

  const addCustomer = () => {
    if (!name) return;
    const updatedCustomers = [...customers];
    if (editIndex >= 0) {
      updatedCustomers[editIndex] = name;
      setEditIndex(-1);
    } else {
      updatedCustomers.push(name);
    }
    setCustomers(updatedCustomers);
    setName('');
  };

  const editCustomer = (index) => {
    setName(customers[index]);
    setEditIndex(index);
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
        value={name} 
        onChange={(e) => setName(e.target.value)} 
        placeholder="Customer Name" 
      />
      <button onClick={addCustomer}>{editIndex >= 0 ? 'Update' : 'Add'} Customer</button>
      <ul>
        {customers.map((customer, index) => (
          <li key={index}>
            {customer} 
            <button onClick={() => editCustomer(index)}>Edit</button>
            <button onClick={() => deleteCustomer(index)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```