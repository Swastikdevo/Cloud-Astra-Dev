```javascript
import React, { useState, useEffect } from 'react';

const CustomerForm = ({ onSubmit }) => {
  const [formData, setFormData] = useState({ name: '', email: '', phone: '' });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
    setFormData({ name: '', email: '', phone: '' });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" name="name" placeholder="Name" value={formData.name} onChange={handleChange} required />
      <input type="email" name="email" placeholder="Email" value={formData.email} onChange={handleChange} required />
      <input type="tel" name="phone" placeholder="Phone" value={formData.phone} onChange={handleChange} required />
      <button type="submit">Add Customer</button>
    </form>
  );
};

const CustomerList = ({ customers, onDelete }) => {
  return (
    <ul>
      {customers.map((customer, index) => (
        <li key={index}>
          {customer.name} - {customer.email} - {customer.phone}
          <button onClick={() => onDelete(index)}>Delete</button>
        </li>
      ))}
    </ul>
  );
};

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);

  const addCustomer = (customer) => {
    setCustomers([...customers, customer]);
  };

  const deleteCustomer = (index) => {
    const newCustomers = customers.filter((_, i) => i !== index);
    setCustomers(newCustomers);
  };

  return (
    <div>
      <h1>Customer Management</h1>
      <CustomerForm onSubmit={addCustomer} />
      <CustomerList customers={customers} onDelete={deleteCustomer} />
    </div>
  );
};

export default CustomerManagement;
```