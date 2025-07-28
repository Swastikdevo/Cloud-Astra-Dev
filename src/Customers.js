```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [editingIndex, setEditingIndex] = useState(null);

  useEffect(() => {
    const storedCustomers = JSON.parse(localStorage.getItem('customers')) || [];
    setCustomers(storedCustomers);
  }, []);

  const addOrUpdateCustomer = () => {
    if (editingIndex !== null) {
      const updatedCustomers = customers.map((customer, index) =>
        index === editingIndex ? { name, email } : customer
      );
      setCustomers(updatedCustomers);
      localStorage.setItem('customers', JSON.stringify(updatedCustomers));
      setEditingIndex(null);
    } else {
      const newCustomer = { name, email };
      const updatedCustomers = [...customers, newCustomer];
      setCustomers(updatedCustomers);
      localStorage.setItem('customers', JSON.stringify(updatedCustomers));
    }
    setName('');
    setEmail('');
  };

  const editCustomer = index => {
    setName(customers[index].name);
    setEmail(customers[index].email);
    setEditingIndex(index);
  };

  const deleteCustomer = index => {
    const updatedCustomers = customers.filter((_, i) => i !== index);
    setCustomers(updatedCustomers);
    localStorage.setItem('customers', JSON.stringify(updatedCustomers));
  };

  return (
    <div>
      <h2>Customer Management</h2>
      <input
        type="text"
        value={name}
        onChange={e => setName(e.target.value)}
        placeholder="Customer Name"
      />
      <input
        type="email"
        value={email}
        onChange={e => setEmail(e.target.value)}
        placeholder="Customer Email"
      />
      <button onClick={addOrUpdateCustomer}>{editingIndex !== null ? 'Update' : 'Add'}</button>
      <ul>
        {customers.map((customer, index) => (
          <li key={index}>
            {customer.name} - {customer.email}
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