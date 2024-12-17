```javascript
import React, { useState } from 'react';

const Customers = () => {
  const [customers, setCustomers] = useState([]);
  const [name, setName] = useState('');
  const [editIndex, setEditIndex] = useState(-1);

  const addCustomer = () => {
    if (name.trim()) {
      if (editIndex >= 0) {
        const updatedCustomers = customers.map((customer, index) => 
          index === editIndex ? name : customer
        );
        setCustomers(updatedCustomers);
        setEditIndex(-1);
      } else {
        setCustomers([...customers, name]);
      }
      setName('');
    }
  };

  const editCustomer = (index) => {
    setName(customers[index]);
    setEditIndex(index);
  };

  const deleteCustomer = (index) => {
    setCustomers(customers.filter((_, i) => i !== index));
  };

  const resetList = () => {
    setCustomers([]);
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
      <button onClick={resetList}>Reset List</button>
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

export default Customers;
```