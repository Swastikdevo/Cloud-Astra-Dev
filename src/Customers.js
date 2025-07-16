```javascript
import React, { useState } from 'react';

const CustomerForm = ({ onSubmit }) => {
  const [customer, setCustomer] = useState({ name: '', email: '', phone: '' });
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    setCustomer({ ...customer, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(customer);
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

const CustomerList = ({ customers }) => (
  <ul>
    {customers.map((customer, index) => (
      <li key={index}>{customer.name} - {customer.email} - {customer.phone}</li>
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
      <CustomerForm onSubmit={addCustomer} />
      <CustomerList customers={customers} />
    </div>
  );
};

export default CustomerManagement;
```