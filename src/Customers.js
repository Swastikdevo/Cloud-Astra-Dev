```javascript
import React, { useState, useEffect } from 'react';

const CustomerForm = ({ onAddCustomer }) => {
  const [customer, setCustomer] = useState({ name: '', email: '' });

  const handleChange = (e) => {
    setCustomer({ ...customer, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onAddCustomer(customer);
    setCustomer({ name: '', email: '' });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input name="name" placeholder="Name" value={customer.name} onChange={handleChange} required />
      <input name="email" placeholder="Email" value={customer.email} onChange={handleChange} required />
      <button type="submit">Add Customer</button>
    </form>
  );
};

const CustomerList = ({ customers }) => (
  <ul>
    {customers.map((customer, index) => (
      <li key={index}>{customer.name} - {customer.email}</li>
    ))}
  </ul>
);

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);

  const addCustomer = (customer) => {
    setCustomers([...customers, customer]);
  };

  return (
    <div>
      <h1>Customer Management</h1>
      <CustomerForm onAddCustomer={addCustomer} />
      <CustomerList customers={customers} />
    </div>
  );
};

export default CustomerManagement;
```