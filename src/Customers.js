```javascript
import React, { useState, useEffect } from 'react';

const CustomerManager = () => {
  const [customers, setCustomers] = useState([]);
  const [newCustomer, setNewCustomer] = useState('');
  const [isEditing, setIsEditing] = useState(false);
  const [editIndex, setEditIndex] = useState(null);

  useEffect(() => {
    const savedCustomers = JSON.parse(localStorage.getItem('customers')) || [];
    setCustomers(savedCustomers);
  }, []);

  const addCustomer = () => {
    if (newCustomer.trim()) {
      setCustomers([...customers, newCustomer]);
      localStorage.setItem('customers', JSON.stringify([...customers, newCustomer]));
      setNewCustomer('');
    }
  };

  const editCustomer = (index) => {
    setNewCustomer(customers[index]);
    setIsEditing(true);
    setEditIndex(index);
  };

  const updateCustomer = () => {
    const updatedCustomers = [...customers];
    updatedCustomers[editIndex] = newCustomer;
    setCustomers(updatedCustomers);
    localStorage.setItem('customers', JSON.stringify(updatedCustomers));
    setNewCustomer('');
    setIsEditing(false);
    setEditIndex(null);
  };

  const deleteCustomer = (index) => {
    const updatedCustomers = customers.filter((_, i) => i !== index);
    setCustomers(updatedCustomers);
    localStorage.setItem('customers', JSON.stringify(updatedCustomers));
  };

  return (
    <div>
      <h2>Customer Management</h2>
      <input
        type="text"
        value={newCustomer}
        onChange={(e) => setNewCustomer(e.target.value)}
      />
      <button onClick={isEditing ? updateCustomer : addCustomer}>
        {isEditing ? 'Update' : 'Add'} Customer
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

export default CustomerManager;
```