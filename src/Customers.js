```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });
  const [editingIndex, setEditingIndex] = useState(null);

  useEffect(() => {
    const savedCustomers = JSON.parse(localStorage.getItem('customers')) || [];
    setCustomers(savedCustomers);
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewCustomer({ ...newCustomer, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (editingIndex !== null) {
      const updatedCustomers = customers.map((customer, index) =>
        index === editingIndex ? newCustomer : customer
      );
      setCustomers(updatedCustomers);
      setEditingIndex(null);
    } else {
      setCustomers([...customers, newCustomer]);
    }
    setNewCustomer({ name: '', email: '' });
  };

  const handleEdit = (index) => {
    setNewCustomer(customers[index]);
    setEditingIndex(index);
  };

  const handleDelete = (index) => {
    const filteredCustomers = customers.filter((_, i) => i !== index);
    setCustomers(filteredCustomers);
  };

  useEffect(() => {
    localStorage.setItem('customers', JSON.stringify(customers));
  }, [customers]);

  return (
    <div>
      <h1>Customer Management</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="name"
          value={newCustomer.name}
          onChange={handleInputChange}
          placeholder="Customer Name"
          required
        />
        <input
          type="email"
          name="email"
          value={newCustomer.email}
          onChange={handleInputChange}
          placeholder="Customer Email"
          required
        />
        <button type="submit">{editingIndex !== null ? 'Update' : 'Add'}</button>
      </form>
      <ul>
        {customers.map((customer, index) => (
          <li key={index}>
            {customer.name} - {customer.email}
            <button onClick={() => handleEdit(index)}>Edit</button>
            <button onClick={() => handleDelete(index)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```