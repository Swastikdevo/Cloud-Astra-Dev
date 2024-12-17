```javascript
import React, { useState } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [name, setName] = useState('');
  const [editingIndex, setEditingIndex] = useState(null);

  const addCustomer = () => {
    if (name) {
      setCustomers([...customers, name]);
      setName('');
    }
  };

  const editCustomer = (index) => {
    setName(customers[index]);
    setEditingIndex(index);
  };

  const updateCustomer = () => {
    const updatedCustomers = customers.map((customer, index) =>
      index === editingIndex ? name : customer
    );
    setCustomers(updatedCustomers);
    setName('');
    setEditingIndex(null);
  };

  const deleteCustomer = (index) => {
    setCustomers(customers.filter((_, i) => i !== index));
  };

  return (
    <div>
      <h2>Customer Management</h2>
      <input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Enter customer name"
      />
      <button onClick={editingIndex !== null ? updateCustomer : addCustomer}>
        {editingIndex !== null ? 'Update Customer' : 'Add Customer'}
      </button>
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