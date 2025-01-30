```javascript
import React, { useState } from 'react';

const CustomerForm = ({ onSave }) => {
  const [customer, setCustomer] = useState({ name: '', email: '', phone: '' });

  const handleChange = (e) => {
    setCustomer({ ...customer, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(customer);
    setCustomer({ name: '', email: '', phone: '' });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" name="name" value={customer.name} onChange={handleChange} placeholder="Name" required />
      <input type="email" name="email" value={customer.email} onChange={handleChange} placeholder="Email" required />
      <input type="tel" name="phone" value={customer.phone} onChange={handleChange} placeholder="Phone" required />
      <button type="submit">Add Customer</button>
    </form>
  );
};

const CustomerList = ({ customers }) => {
  return (
    <ul>
      {customers.map((customer, index) => (
        <li key={index}>{customer.name} - {customer.email} - {customer.phone}</li>
      ))}
    </ul>
  );
};

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);

  const addCustomer = (newCustomer) => {
    setCustomers([...customers, newCustomer]);
  };

  return (
    <div>
      <h1>Customer Management</h1>
      <CustomerForm onSave={addCustomer} />
      <CustomerList customers={customers} />
    </div>
  );
};

export default CustomerManagement;
```